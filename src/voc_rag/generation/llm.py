"""Cliente do LLM (Gemini via google-genai) com saída estruturada.

Três cuidados de engenharia:
  * saída em JSON validada por Pydantic: a resposta tem campos verificáveis
    (insights, ids das evidências), não texto livre;
  * cache em disco por hash da chamada: a avaliação é reproduzível e
    re-executar não gasta cota do plano gratuito;
  * retry com backoff e intervalo mínimo entre chamadas (limite de RPM).
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

from voc_rag.config import CACHE_DIR, get_settings

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMIndisponivel(RuntimeError):
    """Sem chave configurada ou API fora do ar após as tentativas."""


@dataclass
class Uso:
    chamadas: int = 0
    chamadas_cache: int = 0
    tokens_entrada: int = 0
    tokens_saida: int = 0
    segundos: float = 0.0
    por_etapa: dict = field(default_factory=dict)

    def registra(self, etapa: str, tin: int, tout: int, seg: float, cache: bool) -> None:
        if cache:
            self.chamadas_cache += 1
        else:
            self.chamadas += 1
            self.tokens_entrada += tin
            self.tokens_saida += tout
            self.segundos += seg
        e = self.por_etapa.setdefault(
            etapa, {"chamadas": 0, "tokens_entrada": 0, "tokens_saida": 0}
        )
        e["chamadas"] += 1
        e["tokens_entrada"] += tin
        e["tokens_saida"] += tout


def _thinking_config(model: str, nivel: str):
    from google.genai import types

    if model.startswith("gemini-3"):
        return types.ThinkingConfig(thinking_level="low" if nivel == "baixo" else "high")
    if "flash" in model:
        return types.ThinkingConfig(thinking_budget=0 if nivel == "baixo" else 1024)
    return types.ThinkingConfig(thinking_budget=128 if nivel == "baixo" else 1024)


class LLMClient:
    def __init__(
        self,
        model: str | None = None,
        cache_dir: Path = CACHE_DIR / "llm",
        rpm: float | None = None,
        usar_cache: bool = True,
    ):
        cfg = get_settings()
        self.model = model or cfg.llm_model
        self.cache_dir = cache_dir
        self.usar_cache = usar_cache
        self.min_intervalo = 60.0 / float(rpm or os.getenv("VOC_LLM_RPM", "10"))
        self._ultimo = 0.0
        self._client = None
        self._api_key = cfg.gemini_api_key
        self.uso = Uso()

    @property
    def client(self):
        if self._client is None:
            if not self._api_key:
                raise LLMIndisponivel("GEMINI_API_KEY não configurada no .env")
            from google import genai

            self._client = genai.Client(api_key=self._api_key)
        return self._client

    # ------------------------------------------------------------------ cache
    def _chave(self, payload: dict) -> str:
        bruto = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(bruto.encode("utf-8")).hexdigest()

    def _le_cache(self, chave: str) -> dict | None:
        p = self.cache_dir / chave[:2] / f"{chave}.json"
        if self.usar_cache and p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
        return None

    def _grava_cache(self, chave: str, dado: dict) -> None:
        p = self.cache_dir / chave[:2] / f"{chave}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(dado, ensure_ascii=False), encoding="utf-8")

    # ---------------------------------------------------------------- chamada
    def _espera_rpm(self) -> None:
        falta = self.min_intervalo - (time.monotonic() - self._ultimo)
        if falta > 0:
            time.sleep(falta)
        self._ultimo = time.monotonic()

    def _chama(self, system: str, prompt: str, schema: type[BaseModel] | None,
               temperatura: float, pensamento: str) -> tuple[str, int, int]:
        from google.genai import errors, types

        config = types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperatura,
            thinking_config=_thinking_config(self.model, pensamento),
            seed=42,
        )
        if schema is not None:
            config.response_mime_type = "application/json"
            config.response_json_schema = schema.model_json_schema()

        espera = 5.0
        for tentativa in range(6):
            self._espera_rpm()
            try:
                resp = self.client.models.generate_content(
                    model=self.model, contents=prompt, config=config
                )
                um = resp.usage_metadata
                tin = (um.prompt_token_count or 0) if um else 0
                tout = (um.candidates_token_count or 0) if um else 0
                return resp.text or "", tin, tout
            except errors.APIError as e:
                transitorio = e.code in (429, 500, 502, 503, 504)
                if not transitorio or tentativa == 5:
                    raise LLMIndisponivel(f"Gemini falhou ({e.code}): {e}") from e
                log.warning("Gemini %s, nova tentativa em %.0fs", e.code, espera)
                time.sleep(espera)
                espera = min(espera * 2, 90)
        raise LLMIndisponivel("Gemini indisponível")

    def generate(
        self,
        system: str,
        prompt: str,
        schema: type[T],
        etapa: str,
        temperatura: float = 0.0,
        pensamento: str = "baixo",
    ) -> T:
        payload = {
            "model": self.model, "system": system, "prompt": prompt,
            "schema": schema.model_json_schema(), "temperatura": temperatura,
            "pensamento": pensamento,
        }
        chave = self._chave(payload)
        cache = self._le_cache(chave)
        if cache is not None:
            self.uso.registra(etapa, cache["tin"], cache["tout"], 0.0, cache=True)
            return schema.model_validate_json(cache["texto"])

        t0 = time.monotonic()
        texto, tin, tout = self._chama(system, prompt, schema, temperatura, pensamento)
        seg = time.monotonic() - t0
        obj = schema.model_validate_json(texto)
        self._grava_cache(chave, {"texto": texto, "tin": tin, "tout": tout, "segundos": seg})
        self.uso.registra(etapa, tin, tout, seg, cache=False)
        return obj
