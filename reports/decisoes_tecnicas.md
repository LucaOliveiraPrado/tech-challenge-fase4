# Registro de Decisões Técnicas

> Cada decisão relevante do projeto, com o problema, as alternativas consideradas, a escolha e
> a evidência que a sustenta. Complementa o README (visão geral) e os notebooks (onde as
> evidências são produzidas). Números citados vêm dos arquivos em `reports/` gerados pelo
> próprio pipeline.

---

## Base de conhecimento

### D1: Uma avaliação = um documento, sem chunking

**Problema:** definir a unidade de recuperação e de citação.
**Alternativas:** (a) uma avaliação por documento; (b) chunks de tamanho fixo; (c) agrupar
avaliações por pedido ou produto.
**Decisão:** (a). Os comentários são curtos (mediana de 9 palavras, máximo de 47; notebook 01),
então não há o que quebrar, e a avaliação é a unidade natural de evidência que o gestor quer
ver citada. Agrupar por produto misturaria vozes diferentes numa citação só.
**Evidência:** `reports/base_conhecimento.json` (`palavras_por_documento`).

### D2: Só avaliações com texto viram documento

**Problema:** 57.742 das 98.410 avaliações não têm mensagem.
**Decisão:** avaliação sem texto útil fica em `reviews.parquet` (estatísticas de nota) e não
entra no índice: não há conteúdo a recuperar. Títulos sem mensagem (1.656 casos) viram
documento, porque o título sozinho às vezes é a opinião ("Não recebi").

### D3: Uma linha por `review_id`

**Problema:** 789 `review_id` aparecem ligados a mais de um pedido na fonte, com o mesmo texto.
**Decisão:** manter uma ocorrência (ordem determinística por `order_id`) e registrar
`n_pedidos_review`. Contar a mesma opinião duas vezes inflaria frequências e duplicaria
evidências.

### D4: Duas representações do texto

**Decisão:** `clean_text` preserva acentos, caixa e pontuação (vai para o embedding, para o
LLM e para a tela: o cliente é citado como escreveu); `normalize_key` (minúsculas, sem acento,
sem pontuação) serve só para deduplicação. Quebras de linha, tabulações e caracteres de
controle viram espaço; entidades HTML são decodificadas. Título e mensagem são fundidos, e o
título só entra quando acrescenta informação (muitas vezes repete a mensagem).

### D5: Tratamento de ausentes, campo a campo

| Campo | Situação | Tratamento |
|---|---|---|
| Mensagem | 57.742 ausentes + 186 só com pontuação/números | não vira documento (D2) |
| Título | 86.891 ausentes | usa só a mensagem |
| Categoria | produto sem categoria ou pedido sem itens | `sem_categoria` (não descarta) |
| Data de entrega | pedido não entregue ou cancelado | `entrega_status` = `nao_entregue` / `cancelado`; `atraso_dias` nulo |
| Período | compra sem data | usa a data da avaliação |

**Por que não descartar:** os casos ausentes são justamente os mais críticos (pedido sem itens
é quase sempre cancelado; notebook 01, seção 6).

### D6: Textos repetidos ficam no índice e saem do contexto

**Problema:** 8.426 documentos repetem textos de outros ("ótimo", "muito bom", "não recebi o
produto").
**Decisão:** cada repetição é um cliente diferente e conta para frequência, então fica no
índice. Na montagem do contexto, textos idênticos entram uma vez, com a anotação "texto idêntico
em N avaliações", para não gastar o contexto do LLM com a mesma frase.

### D7: Metadados por documento

**Decisão:** `nota`, `sentimento`, `ano_mes` (AAAAMM inteiro, permite intervalo no `where`),
`entrega_status`, `atraso_dias`, `tempo_entrega_dias`, `categoria` (do item de maior valor) e
`categorias` (todas), `uf`, `regiao`, `pagamento`. Todos escalares, como o Chroma exige.
**Evidência de valor:** a situação da entrega separa 9% de avaliações negativas (no prazo) de
62% (atrasado) e 76% (não entregue) (notebook 01, seção 5); o ganho dos filtros na recuperação
está na D18 e no notebook 03.

## Indexação e recuperação

### D8: Embedding `BAAI/bge-m3`, local

**Alternativas:** `paraphrase-multilingual-MiniLM-L12-v2` (118M), `multilingual-e5-base`
(278M), `bge-m3` (568M), API de embeddings do Gemini.
**Decisão:** `bge-m3`, escolhido por experimento, com a mesma configuração para os três modelos
locais (consulta reescrita, só busca vetorial; notebook 03):

| Modelo | P@10 | nDCG@10 |
|---|---|---|
| paraphrase-multilingual-MiniLM-L12-v2 | 0,704 | 0,713 |
| multilingual-e5-base | 0,711 | 0,735 |
| **bge-m3** | **0,800** | **0,817** |

Local e não via API: indexar ~42 mil documentos sem limite de requisições, custo zero e vetores
reproduzíveis por qualquer avaliador (105 s na GPU; roda em CPU, mais devagar).

### D9: ChromaDB + BM25 (busca híbrida)

**Decisão:** ChromaDB persistente (embutido, sem servidor, HNSW com cosseno e filtro de
metadado na própria consulta) para a busca semântica; BM25 (`bm25s`, stemming Snowball em
português, acentos removidos) para termos exatos ("correios", "nota fiscal", "lacrado").
**Detalhe que importa:** as negações (`não`, `nunca`, `nem`, `sem`, `só`, `ainda`) **não** estão
nas stopwords: "não chegou" e "chegou" são opiniões opostas.
**Evidência:** na pergunta do notebook 02 (sistema final, uma consulta), dos 80 candidatos 31
vieram só do BM25, 32 só do vetor e 17 dos dois índices: as duas buscas trazem conjuntos bem
diferentes e a fusão aproveita os dois. Na média da avaliação o BM25 é neutro quando há uma consulta só (P@10 0,800 só vetor
contra 0,804 híbrido) e ajuda quando há várias consultas (0,750 contra 0,775): ele ancora a
busca nos termos literais quando as consultas vetoriais se dispersam. Fica no sistema final pelo
custo desprezível (milissegundos) e pela robustez a termos exatos.

### D10: Transformação da pergunta por LLM

**Problema:** a pergunta do gestor é analítica ("quais reclamações aparecem com maior
frequência?"), o documento é coloquial ("comprei dia 10 e até hoje nada").
**Decisão:** uma chamada estruturada (JSON validado por Pydantic) produz escopo, tipo
(panorama/tema/evidência), polaridade, filtros explícitos, consulta reescrita no vocabulário do
cliente, 2 a 3 variações (multi-query) e uma avaliação hipotética (HyDE).
**Regra de fidelidade:** as variações não podem generalizar o assunto. Sem ela, "entregas por
drone" virava "entrega rápida drone" e recuperava elogios genéricos de entrega com relevância
0,99.
**Evidência:** a reescrita é o maior ganho isolado do projeto: P@10 de **0,607 → 0,800** e
nDCG@10 de 0,664 → 0,817 (pergunta crua contra consulta reescrita, mesma busca vetorial). No
espaço vetorial, o cosseno médio com 200 reclamações de entrega sobe de 0,51 para 0,70
(notebook 02). Já **multi-query e HyDE pioraram** a média (P@10 0,800 → 0,750): mesmo com a
regra de fidelidade, as variações puxam temas vizinhos. Por isso o sistema final usa só a
consulta reescrita; as variações e a avaliação hipotética continuam implementadas, medidas e
desligadas por padrão (`usar_alternativas`, `usar_hyde`).

### D11: Fusão por RRF (k = 60)

**Problema:** cosseno e BM25 estão em escalas diferentes e não comparáveis.
**Decisão:** Reciprocal Rank Fusion, que soma 1/(k + posição) de cada lista e usa só a posição.
k = 60 é o valor padrão da literatura; o documento que aparece em várias listas (várias
consultas, dois índices) sobe.

### D12: Reranker cross-encoder como porteiro, não como ordenador

**Hipótese inicial:** `BAAI/bge-reranker-v2-m3` reordenaria os 80 primeiros da fusão e
melhoraria a precisão do topo.
**Primeiro achado:** o cross-encoder precisa ser pontuado contra a **consulta reescrita**, não
contra a pergunta original. Para "O que os clientes relatam sobre problemas relacionados à
entrega?", o escore mediano dos 80 candidatos foi **0,002** contra a pergunta analítica e
**0,87** contra a reescrita (notebook 02): o modelo foi treinado em pares
pergunta→trecho-que-responde, e nenhuma avaliação "responde" literalmente a uma pergunta sobre o
que os clientes dizem.
**Segundo achado (a avaliação refutou a hipótese):** mesmo assim, ordenar pelo reranker
**piorou** a recuperação em todas as variantes testadas:

| Ordenação (mesmas candidatas) | P@10 |
|---|---|
| fusão RRF, sem reranker | 0,775 |
| reranker, maior escore entre as consultas | 0,707 |
| reranker contra a consulta principal | 0,757 |
| reranker pela média das consultas | 0,661 |

A análise pergunta a pergunta mostra o mecanismo: o cross-encoder confunde temas vizinhos.
Numa pergunta sobre **embalagem** ele põe "Produto veio quebrado" no topo com 1,00; numa sobre
**qualidade de móveis**, idem. O vetor com a consulta reescrita mantém o assunto exato.
**Decisão:** a ordem final é a da fusão RRF; o reranker continua no pipeline como **porteiro de
relevância** (D13), papel em que a sobreposição temática é tolerável. Resultado no sistema
completo: P@10 0,857 (ordem do reranker) → **0,939** (ordem RRF, reranker como porteiro).

### D13: Limiar do porteiro escolhido pelo papel de abstenção

**Evidência:** sobre 1.539 pares julgados, o escore do reranker tem AUC 0,727 contra o juiz, e a
precisão das evidências é quase plana entre limiares (0,84 em 0,05; 0,85 em 0,30; 0,87 em 0,90),
enquanto o recall cai de 0,95 para 0,48. Ou seja: o limiar não serve para filtrar evidência; o
que ele faz bem é identificar perguntas sem evidência. Com qualquer limiar entre 0,1 e 0,5, a
recuperação barra 3 das 5 perguntas sem evidência analisadas (criptomoeda, painel solar,
retirada em loja) e **nenhuma** das 28 respondíveis.
**Decisão:** limiar 0,30 (meio da faixa segura; recall 0,86) e mínimo de 3 evidências acima dele;
abaixo disso o sistema mostra o que encontrou e não generaliza.
**Limite conhecido:** o reranker é tolerante à sobreposição de palavras: "entregas feitas por
drone" tem candidatos com 0,998 porque falam de "entrega". Por isso a decisão fina de suficiência
fica com o LLM (D15).

### D14: Seleção do contexto: deduplicação + MMR

**Decisão:** entre as relevantes, deduplicação de texto (D6) e Maximal Marginal Relevance
(λ = 0,75) para preferir evidências que acrescentam algo novo. Contexto de 15 evidências em
perguntas de tema/evidência e 30 em panorama (comentários curtos: 30 evidências cabem em ~1.500
tokens).

## Geração e abstenção

### D15: Abstenção em três camadas

| Camada | Onde | Barra | Exemplo real |
|---|---|---|---|
| Escopo | análise da pergunta | fora da base, conhecimento externo, *prompt injection* | "Qual foi o faturamento da Olist em 2018?" |
| Relevância | reranker + limiar | nenhuma evidência acima do limiar; menos de 3 relevantes | "Quais reclamações existem sobre pagamento com criptomoedas?" (máximo 0,00) |
| Suficiência | geração | evidências tocam o tema mas não respondem | "O que os clientes acharam das entregas feitas por drone?" (evidências só sobre entrega comum) |

**Por que três:** cada camada é mais cara e mais fina que a anterior. Abster cedo economiza
chamadas; abster tarde pega o que o limiar numérico não vê.
**Evidência:** nas 40 perguntas da avaliação, **40 de 40** decisões entre responder e abster
foram corretas: as 28 respondíveis foram respondidas e as 12 que deviam ser recusadas foram, cada
uma pela camada esperada: 7 por escopo (incluindo a *prompt injection* e "iPhone 15", posterior à
base), 2 por falta de evidência relevante (criptomoeda, painel solar), 1 por evidência
insuficiente (retirada em loja física) e 2 pela geração (drone, cashback), em que a recuperação
trouxe avaliações sobre "entrega" e "dinheiro de volta" e o LLM reconheceu que elas não tratam do
assunto perguntado (`reports/avaliacao_geracao.json`).

### D16: Saída estruturada e citações verificadas por código

**Decisão:** o LLM devolve JSON (`resumo`, `insights[{titulo, descricao, evidencias}]`,
`limitacoes`, `suficiente`). O código remove ids inexistentes, aceita os formatos `[R1]`,
`[R1, R2]` e `[R1; R2]`, normaliza para `[R1][R2]` e descarta insight sem evidência válida. Cada
insight mostra o apoio ("apoio: 16 de 30 evidências") e cada `[R#]` leva a um `review_id` real.
**Por que:** rastreabilidade não pode depender de o modelo obedecer ao prompt.
**Evidência:** 635 citações nas respostas geradas, **100% válidas**; 84 insights, nenhum
descartado por falta de evidência. A auditoria do juiz (modelo diferente do gerador) julgou 78
dos 84 insights como **sustentados** e 6 como parciais (escore 0,96). Os parciais têm a mesma
causa: o modelo anexa marcas `[R#]` a um percentual que vem do quadro de frequências, e o juiz lê
isso como extrapolação da amostra para a base. A correção natural (proibir citação ao lado de
números do quadro) fica registrada como evolução.
**Controle de qualidade de idioma:** o modelo "lite" às vezes escreve sem acentos (5 de 30
respostas na primeira rodada). Um detector de termos comuns sem acento ("nao", "sao",
"avaliacoes"...) dispara uma segunda geração com reforço explícito no prompt; as respostas
afetadas foram corrigidas sem tocar nas demais.

### D17: Quadro de frequências por classificador de aspectos

**Problema:** top-k não conta; "o que aparece com maior frequência" pede contagem na base.
**Alternativas:** (a) contar só na amostra recuperada; (b) rotular todas as 42 mil avaliações com
LLM; (c) rotular uma amostra com LLM e generalizar com um classificador.
**Decisão:** (c). 3.000 avaliações rotuladas pelo LLM (amostra estratificada por nota) treinam
uma regressão logística one-vs-rest sobre [embedding + nota]; teste em 600 rótulos nunca vistos:
micro-F1 0,789, macro-F1 0,744 (`reports/metricas_aspectos.json`). Custo fixo de 60 chamadas,
independente do tamanho da base. A contagem usa Adjusted Classify and Count (Forman, 2008) com
taxas de erro ponderadas pela distribuição real de notas, e é apresentada como ordem de
grandeza.
**Limite:** aspectos raros (elogio ao atendimento, embalagem) têm F1 baixo (0,42 e 0,60).

## Metadados (desafio adicional)

### D18: Metadados como filtro dentro do banco vetorial

**Decisão:** filtros explícitos da pergunta (nota, categoria, período, entrega, UF, região)
viram cláusula `where` no Chroma e máscara no BM25 (a mesma definição gera as duas, com teste
de equivalência). A polaridade vira filtro implícito de nota (problemas: nota ≤ 3; elogios:
nota ≥ 4) quando a pergunta não fixa nota; o campo `sentimentos` que o LLM às vezes preenche é
descartado para não estreitar o recorte duas vezes.
**Como os metadados melhoram a recuperação:** sem filtro, a busca vetorial acha o **tema** certo
fora do **recorte** pedido (reclamação de móveis numa pergunta sobre cama, mesa e banho; nota 4
numa pergunta sobre nota 1), e essas avaliações ocupam vagas do contexto. Com o filtro dentro da
consulta, o recorte é respeitado por construção e as vagas vão para evidências do recorte.
Os metadados também entram no **contexto** de cada evidência (nota, atraso em dias, categoria),
o que deixa o LLM interpretar "demorou" à luz de um pedido 12 dias atrasado.
**Evidência:** nas 8 perguntas com recorte, julgadas com os metadados visíveis para o juiz:

| Perguntas com recorte | P@10 | Conformidade ao recorte (top-10) |
|---|---|---|
| sem filtros (A4) | 0,188 | 25,0% |
| com filtros e polaridade (A5) | 0,725 | 88,7% |
| sistema final (filtros + ordem RRF) | **0,850** | **91,2%** |

A conformidade não chega a 100% porque o filtro aplicado é o que a análise da pergunta extraiu:
quando o LLM erra um campo (ex.: deixa de marcar a situação da entrega), o recorte fica mais
largo que o pedido. A taxa de extração correta está na avaliação de geração (D15).

## Infraestrutura

### D19: Modelos de linguagem

**Restrição real:** o projeto roda no **plano gratuito** da API do Gemini, que limita os modelos
"flash" a **20 requisições por dia por modelo** (descoberto quando a cota do `gemini-3.5-flash`
esgotou no primeiro dia: `GenerateRequestsPerDayPerProjectPerModel-FreeTier = 20`). Os modelos
"lite" têm cota bem maior. Os modelos 2.5 não estão disponíveis para contas novas (404) e o
`gemini-3.1-pro` não tem cota gratuita.
**Decisão:** papéis separados por modelo, com fallback automático:

| Papel | Modelo | Fallback | Por quê |
|---|---|---|---|
| Análise da pergunta e geração | `gemini-3.5-flash-lite` | `gemini-3.1-flash-lite` | cota diária compatível com uso e avaliação; JSON estável e ~2 s na análise |
| Rotulagem de aspectos | `gemini-3.5-flash-lite` | n/a | tarefa simples em lote |
| Juiz da avaliação | `gemini-3.6-flash` | `gemini-3.7-flash`, `gemini-3.8-flash` | modelo diferente (e mais forte) que o gerador, reduz autoaprovação |

**Engenharia em torno da cota:** 429 de cota **diária** falha rápido (não adianta repetir) e passa
ao próximo modelo da lista; 429 por minuto e 503 fazem retry com backoff; cache em disco por hash
da chamada (reexecutar a avaliação não gasta cota) registrando qual modelo respondeu; julgamentos
em lote (80 avaliações por chamada de relevância, 3 respostas por chamada de fidelidade); a
avaliação **aborta** se alguma análise cair no modo degradado sem LLM, para não medir um sistema
diferente do real. Temperatura 0 e semente fixa em todas as chamadas.

### D20: Frequências descrevem quem comentou

**Evidência:** 77% das avaliações nota 1 têm comentário, contra cerca de 35% das notas 4 e 5; a
nota 1 é 11% da base e 21% dos comentários (notebook 01, seção 2).
**Decisão:** todo número apresentado é relativo ao recorte de **comentários**, e o sistema diz
isso. O prompt proíbe extrapolar a amostra recuperada para a base.

## Avaliação

### D21: Pooling + LLM-juiz diferente do gerador

**Problema:** não há rótulo de relevância para 42 mil documentos.
**Decisão:** protocolo de pooling (TREC): a união dos top-10 de todas as configurações, mais os
contextos finais e uma amostra ao longo do ranking, forma o conjunto julgado (3.251 pares); o
juiz atribui relevância 0/1/2 com critério escrito à mão por pergunta; julgamentos versionados em
`eval/julgamentos_relevancia.csv`, com o modelo que julgou cada par. Fidelidade dos insights
auditada pelo juiz contra as evidências citadas.
**Correção durante o projeto:** a primeira rodada julgava só o texto. Nas perguntas com recorte
("reclamações do Nordeste", "elogios em beleza e saúde"), o juiz não tinha como saber a região
ou a categoria e zerava avaliações corretas. Nessas 8 perguntas ele passou a ver os metadados de
cada avaliação, e os julgamentos foram refeitos.
**Juízes efetivos:** a cota gratuita dos modelos "flash" acabou no meio da avaliação; 2.742 pares
foram julgados pelo `gemini-3.1-flash-lite`, 292 pelo `gemini-3.8-flash` e 217 pelo
`gemini-3.7-flash`. Como todo o pool de uma pergunta é julgado pelo mesmo modelo, a comparação
entre configurações usa a mesma régua dentro de cada pergunta.
**Concordância entre juízes:** 6 perguntas (626 pares) rejulgadas pelo `gemini-3.5-flash`:
concordância exata de 90,4% na escala 0/1/2 (kappa ponderado 0,887) e de 96,0% na decisão
"evidência clara", a usada na P@10 (kappa 0,916). Kappa acima de 0,8 é concordância quase
perfeita: o juiz de reserva mede o mesmo que um modelo "flash"
(`reports/concordancia_juizes.json`).
**Limite:** os juízes são LLMs e podem compartilhar vieses; não houve dupla anotação humana em
escala.

### D22: Reprodutibilidade

`uv` com `uv.lock` (Python 3.12), torch CUDA no Windows/Linux com fallback para CPU, dataset
baixado do Kaggle por `kagglehub` (sem login), embeddings em cache alinhados por `review_id`,
semente 42, cache das chamadas ao LLM e rótulos/julgamentos versionados.
