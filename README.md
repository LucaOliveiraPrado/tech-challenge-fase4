# Tech Challenge Fase 4
## Voice of Customer Intelligence com RAG sobre as avaliações da Olist

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/LLM-Gemini%20(plano%20gratuito)-8E75B2?logo=googlegemini&logoColor=white)
![bge-m3](https://img.shields.io/badge/embeddings-bge--m3-2a78d6)
![ChromaDB](https://img.shields.io/badge/vetorial-ChromaDB-ff6446)
![BM25](https://img.shields.io/badge/lexical-BM25-1baf7a)
![Streamlit](https://img.shields.io/badge/app-Streamlit-FF4B4B?logo=streamlit&logoColor=white)

Sistema de perguntas e respostas sobre a **voz do cliente** de um e-commerce: o gestor pergunta em
linguagem natural ("quais reclamações de entrega aparecem com mais frequência?") e recebe uma
resposta construída **somente** com avaliações reais de clientes, em que **cada afirmação aponta
as avaliações que a sustentam** (rastreáveis pelo `review_id`) e que **se recusa a responder**
quando a base não tem evidência suficiente.

![Aplicação respondendo com evidências](images/app_resposta.png)

*A interface mostra a resposta, as evidências citadas (borda azul), a frequência dos temas na base
e o rastro de cada etapa do pipeline.*

---

## Sumário

1. [Problema de negócio](#1-problema-de-negócio)
2. [Arquitetura](#2-arquitetura)
3. [Tecnologias](#3-tecnologias)
4. [Preparação da base de conhecimento](#4-preparação-da-base-de-conhecimento)
5. [Estratégia do pipeline RAG](#5-estratégia-do-pipeline-rag)
6. [Respostas fundamentadas e rastreabilidade](#6-respostas-fundamentadas-e-rastreabilidade)
7. [Quando o sistema não responde](#7-quando-o-sistema-não-responde)
8. [Metadados (desafio adicional)](#8-metadados-desafio-adicional)
9. [Avaliação quantitativa](#9-avaliação-quantitativa)
10. [Exemplos de perguntas e respostas](#10-exemplos-de-perguntas-e-respostas)
11. [Principais decisões técnicas](#11-principais-decisões-técnicas)
12. [Limitações](#12-limitações)
13. [Como executar e reproduzir](#13-como-executar-e-reproduzir)
14. [Estrutura do repositório](#14-estrutura-do-repositório)
15. [Vídeo](#15-vídeo)

---

## 1. Problema de negócio

Um e-commerce acumula dezenas de milhares de avaliações. A **nota** diz *se* o cliente ficou
satisfeito; o **comentário** diz *por quê*. Ler milhares de comentários à mão não escala, e um
painel de notas não responde perguntas como "o que os clientes insatisfeitos relatam?" ou "quais
evidências sustentam que o prazo de entrega é um problema recorrente?".

A base é o [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(~100 mil pedidos, 2016 a 2018). O desafio pede uma solução de **Retrieval-Augmented Generation**
que recupere avaliações relevantes, gere respostas coerentes com essas evidências, permita
rastrear cada insight e reconheça quando não há informação suficiente. Enunciado completo em
[`docs/enunciado.md`](docs/enunciado.md).

## 2. Arquitetura

```mermaid
flowchart LR
    subgraph offline ["Construção da base (offline)"]
        K["Kaggle Olist<br/>99 mil avaliações"] --> P["voc prepare<br/>limpeza, dedupe,<br/>metadados"]
        P --> D[("42 mil documentos<br/>+ metadados")]
        D --> E["bge-m3<br/>embeddings (GPU)"]
        E --> C[("ChromaDB<br/>HNSW cosseno")]
        D --> B[("BM25<br/>stemming PT")]
        D --> A["Aspectos<br/>LLM rotula 3 mil +<br/>classificador"]
    end
    subgraph online ["Pergunta (online)"]
        Q["Pergunta"] --> AN["1. Análise da pergunta (LLM)<br/>escopo, tipo, filtros,<br/>reescrita no vocabulário<br/>do cliente"]
        AN -->|fora do escopo| X1(["abstém"])
        AN --> R["2. Busca híbrida<br/>denso + BM25<br/>com filtros"]
        C --> R
        B --> R
        R --> F["RRF<br/>(define a ordem)"] --> RR["3. Reranker como<br/>porteiro de relevância"]
        RR -->|sem evidência| X2(["abstém"])
        RR --> S["dedupe + MMR"]
        S --> CT["4. Contexto R1..Rn<br/>+ quadro de frequências"]
        A --> CT
        CT --> G["5. Geração (LLM)<br/>JSON estruturado"]
        G -->|evidência não sustenta| X3(["abstém"])
        G --> V["validação das<br/>citações (código)"]
        V --> OUT["resposta + insights<br/>+ evidências (review_id)"]
    end
```

Três interfaces sobre o mesmo pipeline (`src/voc_rag/pipeline.py`): o app Streamlit
(`app/streamlit_app.py`), a linha de comando (`uv run voc ask "..."`) e os notebooks.

## 3. Tecnologias

| Camada | Tecnologia | Por que esta |
|---|---|---|
| Embeddings | `BAAI/bge-m3` (sentence-transformers, local, GPU) | melhor modelo no experimento com 3 candidatos (seção 9); sem custo nem limite de API para 42 mil documentos |
| Banco vetorial | ChromaDB persistente | embutido, sem servidor, HNSW com cosseno e **filtro de metadado na consulta** |
| Busca lexical | `bm25s` + PyStemmer (Snowball PT) | recupera termos exatos que o vetor dilui; negações preservadas |
| Reranker | `BAAI/bge-reranker-v2-m3` (cross-encoder) | porteiro de relevância (abstenção barata); **não** ordena: na avaliação, ordenar por ele piorou a P@10 (D12) |
| LLM | Gemini via `google-genai`: `gemini-3.5-flash-lite` gera; o juiz da avaliação é outro modelo (`gemini-3.6-flash` com fallback, na prática quase sempre `gemini-3.1-flash-lite`) | saída JSON validada; plano gratuito com cota por modelo (D19, D21) |
| Validação de esquemas | Pydantic | toda saída do LLM é um objeto tipado, não texto livre |
| Classificador de aspectos | scikit-learn (regressão logística) | generaliza 3 mil rótulos do LLM para as 42 mil avaliações a custo fixo |
| Interface | Streamlit + Altair | demonstração com evidências e rastro do pipeline |
| Ambiente | `uv` + `uv.lock`, Python 3.12, torch CUDA | reprodutível com um comando; cai para CPU sem GPU |
| Qualidade | pytest, ruff | testes de limpeza, filtros, fusão, citações e sincronia README × JSON |

## 4. Preparação da base de conhecimento

`uv run voc prepare` ([`src/voc_rag/data/prepare.py`](src/voc_rag/data/prepare.py)) baixa o dataset
do Kaggle (sem login, via `kagglehub`) e constrói a base. Análise exploratória completa em
[`notebooks/01_eda_avaliacoes.ipynb`](notebooks/01_eda_avaliacoes.ipynb).

<!-- num:base -->
| Etapa | Quantidade |
|---|---|
| Linhas na fonte | 99.224 |
| `review_id` ligados a mais de um pedido (contam uma vez) | 789 |
| Avaliações únicas | 98.410 |
| Sem mensagem na fonte | 57.742 |
| Mensagem vazia após limpeza | 186 |
| **Documentos na base de conhecimento** | **42.138** |
<!-- /num:base -->

| Estratégia | Decisão | Por quê |
|---|---|---|
| **Seleção dos dados** | a tabela de avaliações é o centro; pedidos, itens, produtos, clientes e pagamentos entram como metadados | o foco do desafio é o texto; o resto contextualiza |
| **Organização dos documentos** | 1 avaliação = 1 documento, **sem chunking** | comentários têm mediana de 9 palavras (máximo 47); a avaliação é a unidade de evidência citável |
| **Limpeza** | texto fiel ao original (acentos, caixa) para embedding, LLM e tela; chave normalizada só para deduplicar; título fundido à mensagem quando acrescenta | o cliente é citado como escreveu |
| **Ausentes** | sem texto: fica nas estatísticas, não vira documento; sem categoria: `sem_categoria`; sem entrega: `nao_entregue`/`cancelado` | os casos ausentes são justamente os mais críticos (pedidos cancelados) |
| **Duplicatas** | `review_id` repetido conta uma vez; textos idênticos de clientes diferentes ficam no índice e são deduplicados só no contexto | frequência preservada, contexto sem repetição |
| **Embeddings** | `bge-m3`, normalizados, 1024 dimensões, cache `.npy` alinhado por `review_id` | escolhido por medição; cache permite comparar modelos sem reindexar |
| **Armazenamento e indexação** | ChromaDB (vetores + metadados escalares) e BM25 (tokens com stemming) | busca híbrida com filtros |

Dois achados da EDA que moldaram o sistema:

| | |
|---|---|
| ![Entrega](images/eda_entrega_negativas.png) | ![Quem comenta](images/eda_comentario_por_nota.png) |

**Atraso multiplica a insatisfação** (por isso a situação da entrega é metadado e filtro) e **quem
comenta é mais crítico** do que a média dos clientes (por isso toda frequência é apresentada como
relativa aos comentários, nunca extrapolada para todos os clientes).

## 5. Estratégia do pipeline RAG

Cada etapa é demonstrada com uma pergunta real em
[`notebooks/02_pipeline_passo_a_passo.ipynb`](notebooks/02_pipeline_passo_a_passo.ipynb).

**1. Transformação da pergunta** ([`retrieval/query.py`](src/voc_rag/retrieval/query.py)).
Uma chamada ao LLM com saída JSON converte a pergunta em: escopo (dentro/fora), tipo (panorama,
tema, evidência), polaridade (problemas/elogios), filtros explícitos de metadado e a **consulta
reescrita no vocabulário do cliente**. A pergunta do gestor é analítica ("quais reclamações
aparecem com maior frequência?"); o documento é coloquial ("comprei dia 10 e até hoje nada"); a
reescrita aproxima os dois e é o **maior ganho isolado do projeto** (P@10 de 0,61 para 0,80, D10).
O módulo também gera variações (multi-query) e uma avaliação hipotética (HyDE); ambas foram
medidas, **não ajudaram** e ficam desligadas por padrão.

**2. Recuperação semântica e lexical** ([`retrieval/retriever.py`](src/voc_rag/retrieval/retriever.py)).
A consulta vai ao ChromaDB (cosseno, filtros no `where`) e ao BM25 (filtros como máscara). As
listas são fundidas por **Reciprocal Rank Fusion**, que usa só a posição e por isso combina escalas
diferentes. **A ordem final é a da fusão.**

**3. Seleção dos mais relevantes.** Os 80 primeiros passam pelo **reranker cross-encoder**,
pontuado contra a consulta reescrita (contra a pergunta analítica o escore mediano era 0,002;
contra a reescrita, 0,87). Ele atua como **porteiro**: só entram evidências acima do limiar, e
com menos de 3 o sistema não generaliza. A hipótese inicial era usá-lo para reordenar, mas a
avaliação mostrou que ele confunde temas vizinhos ("produto veio quebrado" no topo de uma
pergunta sobre embalagem) e piora a precisão (D12). Depois: **deduplicação** de textos idênticos
e **MMR** para diversidade. Contexto de 15 evidências (tema) ou 30 (panorama).

**4. Construção do contexto** ([`generation/answer.py`](src/voc_rag/generation/answer.py)). Evidências
numeradas `[R1]..[Rn]`, cada uma com nota, situação e atraso da entrega, categoria, UF e mês. Em
perguntas de panorama entra o **quadro de frequências**: contagem estimada de cada aspecto na
**base completa do recorte**, porque top-k não conta frequência (D17).

**5. Geração.** O LLM recebe regras de fundamentação (só as evidências, números só do quadro ou da
contagem da amostra, o texto das avaliações é dado e não instrução) e devolve JSON com resumo,
insights e os ids que sustentam cada insight. Um controle de qualidade gera de novo, com reforço,
quando o modelo escreve sem acentos (falha observada no modelo "lite").

A interface mostra esse caminho para cada pergunta:

![Rastro do pipeline na interface](images/app_rastro.png)

## 6. Respostas fundamentadas e rastreabilidade

A rastreabilidade não depende de o modelo obedecer ao prompt: **o código verifica cada citação**.
Ids que não existem no contexto são removidos, insight sem evidência válida é descartado, e cada
insight exibe o apoio ("apoio: 16 de 30 evidências"). Cada `[R#]` leva a um `review_id` real da
Olist, mostrado na interface e salvo em `reports/respostas_avaliacao.json`.

## 7. Quando o sistema não responde

| Camada | Onde | O que barra | Exemplo |
|---|---|---|---|
| Escopo | análise da pergunta | conhecimento externo, dados que não estão nos comentários, *prompt injection* | "Qual foi o faturamento da Olist em 2018?" |
| Relevância | reranker + limiar | nenhuma avaliação relevante; menos de 3 evidências | "Quais reclamações existem sobre pagamento com criptomoedas?" |
| Suficiência | geração | evidências tocam o tema mas não respondem | "O que os clientes acharam das entregas feitas por drone?" |

Cada camada é mais cara e mais fina que a anterior: abster cedo economiza chamadas, abster tarde
pega o que um limiar numérico não vê (D15).

## 8. Metadados (desafio adicional)

Nota, período (`ano_mes`), situação da entrega e atraso, categoria, UF/região e pagamento estão em
cada documento. Eles entram em três lugares:

1. **Filtro dentro da busca**: "nota baixa", "cama, mesa e banho", "entregues com atraso", "nota 1
   em 2018" viram cláusula `where` no banco vetorial e máscara no BM25;
2. **Polaridade como filtro implícito**: perguntas sobre problemas buscam notas até 3; sobre
   elogios, notas a partir de 4;
3. **Contexto de cada evidência**: o LLM sabe que aquele "demorou" veio de um pedido 12 dias
   atrasado.

Ganho medido nas 8 perguntas com recorte, mesma configuração com e sem filtros (notebook 03):

<!-- num:metadados -->
| 8 perguntas com recorte por metadado | Sem filtros | Com filtros (sistema final) |
|---|---|---|
| Conformidade ao recorte (top-10) | 42,5% | **91,2%** |
| P@10 (juiz vê os metadados) | 0,388 | **0,850** |
<!-- /num:metadados -->

Sem filtro, a busca acha o **tema** certo fora do **recorte** pedido (uma reclamação de móveis numa
pergunta sobre cama, mesa e banho), e essas avaliações ocupam vagas do contexto. Com o filtro, o
recorte é respeitado por construção.

## 9. Avaliação quantitativa

Detalhes, gráficos e leitura em [`notebooks/03_avaliacao.ipynb`](notebooks/03_avaliacao.ipynb).
**40 perguntas** ([`eval/perguntas.json`](eval/perguntas.json)): 28 respondíveis (os cinco tipos de
exploração do enunciado + 8 com metadados), 6 fora do escopo (incluindo *prompt injection*) e 6 sem
evidência na base. Relevância julgada por **pooling** (como no TREC) com um **LLM-juiz diferente do
gerador**; julgamentos versionados em `eval/julgamentos_relevancia.csv`.

**Ablação: o caminho até o sistema final** (28 perguntas respondíveis; P@10 = fração do top-10
com evidência clara, relevância 2):

<!-- num:ablacao -->
| Etapa | P@5 | P@10 | nDCG@10 | MRR | Hit@5 |
|---|---|---|---|---|---|
| RAG ingênuo (pergunta crua, só vetor) | 0,600 | 0,607 | 0,664 | 0,722 | 0,893 |
| + reescrita da pergunta | 0,821 | 0,800 | 0,817 | 0,863 | 0,893 |
| + BM25 (busca híbrida, fusão RRF) | 0,786 | 0,804 | 0,812 | 0,869 | 0,893 |
| **+ filtros de metadado, polaridade e reranker como porteiro (sistema final)** | 0,914 | 0,939 | 0,943 | 0,964 | 1,000 |
<!-- /num:ablacao -->

![Ablação](images/avaliacao_ablacao.png)

**Testado e descartado pelos dados.** Duas técnicas comuns em RAG pioraram a recuperação aqui e
ficaram fora do sistema final (continuam implementadas e reproduzíveis):

<!-- num:descartadas -->
| Técnica testada | P@10 com | P@10 sem | Decisão |
|---|---|---|---|
| multi-query + HyDE sobre a consulta reescrita | 0,750 | 0,800 | descartada |
| reranker ordenando o resultado da busca híbrida | 0,707 | 0,775 | descartada |
| reranker contra a consulta principal (em vez do máximo) | 0,757 | 0,775 | descartada |
| sistema completo ordenado pelo reranker | 0,857 | 0,939 | descartada |
<!-- /num:descartadas -->

As variações de consulta e o reranker têm o mesmo defeito neste domínio: puxam **temas
vizinhos**. Numa pergunta sobre embalagem, "produto veio quebrado" sobe ao topo com escore 1,00;
o vetor com a consulta reescrita mantém o assunto exato. O reranker segue no pipeline com outro
papel, o de porteiro de relevância, onde essa tolerância não atrapalha (D12, D13).

**Escolha do embedding** (mesma configuração para os três: consulta reescrita, só busca vetorial):

<!-- num:embeddings -->
| Modelo de embedding | P@10 | nDCG@10 | MRR |
|---|---|---|---|
| paraphrase-multilingual-MiniLM-L12-v2 | 0,704 | 0,713 | 0,739 |
| multilingual-e5-base | 0,711 | 0,735 | 0,796 |
| **bge-m3 (escolhido)** | 0,800 | 0,817 | 0,863 |
<!-- /num:embeddings -->

**Ponta a ponta** (40 perguntas, pipeline completo):

<!-- num:geracao -->
| Métrica | Resultado |
|---|---|
| Decisão responder x abster correta | 100,0% (40 de 40) |
| Abstenções corretas (fora de escopo + sem evidência) | 12 de 12 |
| Perguntas respondíveis recusadas indevidamente | 0 de 28 |
| Citações válidas (verificadas por código) | 100,0% de 635 |
| Fidelidade dos insights (juiz; sustentado = 1, parcial = 0,5) | 0,96 em 84 insights |
| Precisão do contexto enviado ao LLM | 91,0% |
| Extração correta dos filtros de metadado | 100% |
| AUC do reranker contra o juiz | 0,727 |
<!-- /num:geracao -->

**O juiz é confiável?** Com a cota gratuita, a maior parte dos julgamentos ficou com o modelo de
reserva (`gemini-3.1-flash-lite`). Uma amostra de 6 perguntas foi rejulgada por um modelo "flash"
independente; kappa acima de 0,8 é considerado concordância quase perfeita:

<!-- num:concordancia -->
| Concordância entre juízes (626 pares rejulgados por `gemini-3.5-flash`) | Resultado |
|---|---|
| Concordância exata na escala 0/1/2 | 90,4% |
| Kappa de Cohen ponderado (0/1/2) | 0,887 |
| Concordância em "evidência clara" (decisão usada na P@10) | 96,0% |
| Kappa de Cohen nessa decisão | 0,916 |
<!-- /num:concordancia -->

**Classificador de aspectos** (quadro de frequências):
<!-- num:aspectos -->
micro-F1 0,789 e macro-F1 0,744 em 600 rótulos de teste
<!-- /num:aspectos -->
([`reports/metricas_aspectos.json`](reports/metricas_aspectos.json)).

**Tempo de resposta** (5 perguntas inéditas, `reports/latencia.json`). O tempo é dominado pelas
duas chamadas ao LLM no plano gratuito, que inclui um intervalo mínimo entre chamadas para
respeitar o limite por minuto; a recuperação inteira roda em menos de 1 segundo:

<!-- num:latencia -->
| Etapa (mediana, sem cache) | Segundos |
|---|---|
| Análise da pergunta (LLM) | 9,9 |
| Recuperação (embeddings, ChromaDB, BM25, reranker; GPU) | 0,6 |
| Geração (LLM) | 13,2 |
| **Total por pergunta** | **22,4** |
<!-- /num:latencia -->

## 10. Exemplos de perguntas e respostas

Nove exemplos completos (análise da pergunta, filtros, consulta reescrita, resposta e evidências
com `review_id`) em [`reports/exemplos_perguntas_respostas.md`](reports/exemplos_perguntas_respostas.md);
as 40 respostas em [`reports/respostas_avaliacao.json`](reports/respostas_avaliacao.json).

<details>
<summary><b>Exemplo completo: pergunta do tipo "evidência"</b></summary>

<!-- num:exemplo -->
**Pergunta:** Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?

> As 15 avaliações recuperadas sustentam a conclusão de problemas recorrentes no prazo de entrega, apontando atrasos severos e não recebimento dos produtos [R1][R2][R3][R5]. Os clientes relatam descumprimento de prazos estabelecidos e falhas na comunicação por parte da loja [R5][R15].
>
> - **Descumprimento geral de prazos**: Os consumidores afirmam de forma recorrente que a loja falha em cumprir as datas estabelecidas para o recebimento das mercadorias [R2][R4][R5][R13]. *(apoio: 5 de 15 evidências)*
> - **Atrasos prolongados e falta de entrega**: Várias avaliações apontam que os produtos ultrapassam o prazo limite e demoram dias a mais para chegar ou simplesmente não são entregues [R1][R3][R6][R8]. *(apoio: 6 de 15 evidências)*
> - **Ausência de comunicação e satisfação**: Clientes criticam a falta de aviso prévio sobre os atrasos e a ausência de justificativas por parte da empresa sobre a demora [R5][R15]. *(apoio: 2 de 15 evidências)*
> - **Pedidos cancelados e não recebidos**: Há registros de produtos que continuam sem entrega até o momento da avaliação, resultando em insatisfação e pedidos cancelados [R7][R9][R11]. *(apoio: 3 de 15 evidências)*
>
> *Limitações: As constatações utilizam exclusivamente a amostra recuperada de 15 avaliações, sem permitir extrapolações para a base completa de 14445 comentários.*

| id | review_id | nota | texto do cliente |
|---|---|---|---|
| R1 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | Não cumpriu com o prazo e o produto não chegou. |
| R2 | `10467dc456e818c60bd750271b5d183e` | 1 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R3 | `48b3ce236ea9d35a4850ea94ca9ca38f` | 2 | Atraso. Produto não chegou no prazo |
<!-- /num:exemplo -->

</details>

## 11. Principais decisões técnicas

Registro completo (22 decisões com problema, alternativas, escolha e evidência):
[`reports/decisoes_tecnicas.md`](reports/decisoes_tecnicas.md).

| # | Decisão | Evidência |
|---|---|---|
| D1 | Uma avaliação = um documento, sem chunking | mediana de 9 palavras, máximo 47 |
| D8 | Embedding `bge-m3` local | nDCG@10 0,817 contra 0,735 (E5) e 0,713 (MiniLM) |
| D9 | Busca híbrida (vetor + BM25), negações fora das stopwords | "não chegou" ≠ "chegou"; BM25 ancora termos literais |
| D10 | Reescrita da pergunta no vocabulário do cliente; multi-query e HyDE desligados | P@10 0,607 → 0,800; variações pioraram (0,750) |
| D12 | Reranker como porteiro, ordem pela fusão RRF | ordenar pelo reranker piorou; sistema final P@10 0,857 → 0,939 |
| D13 | Limiar do porteiro escolhido pelo papel de abstenção | 0,1 a 0,5 barram 3 de 5 sem evidência e 0 de 28 respondíveis |
| D15 | Abstenção em três camadas | 12 de 12 recusas corretas, 0 de 28 recusas indevidas |
| D16 | Citações verificadas por código; controle de acentuação | 100% das citações válidas; fidelidade 0,96 |
| D17 | Quadro de frequências por classificador de aspectos + correção de prevalência | top-k não conta frequência |
| D18 | Metadados como filtro dentro da busca | conformidade ao recorte 42,5% → 91,2% |
| D19 | Gemini no plano gratuito com papéis por modelo e fallback | cota de 20 req/dia por modelo "flash" |
| D20 | Frequências relativas a quem comentou | nota 1 é 11% da base e 21% dos comentários |

## 12. Limitações

- **Juiz automático:** a relevância e a fidelidade foram julgadas por LLM (diferente do gerador),
  sem dupla anotação humana em escala. A maior parte ficou com o modelo de reserva
  (`gemini-3.1-flash-lite`); a concordância com um segundo juiz independente é quase perfeita
  (seção 9, D21), mas os dois são LLMs e podem compartilhar vieses.
- **Números do quadro com citação:** nos poucos insights julgados "parciais", o modelo anexou
  evidências individuais a um percentual da base completa; o juiz lê isso como extrapolação (D16).
- **Quem comenta não é todo cliente:** menos da metade das avaliações tem texto e os insatisfeitos
  comentam mais; os números descrevem os comentários.
- **Frequências são estimativas:** o quadro vem de um classificador (micro-F1 0,79); aspectos raros
  (elogio ao atendimento, embalagem) são menos confiáveis. É apresentado como ordem de grandeza.
- **Reranker:** tolerante à sobreposição temática; não ordena o resultado e, como porteiro, deixa
  passar casos como "entregas por drone" (avaliações sobre entrega comum pontuam alto). Por isso a
  suficiência final é decidida na geração.
- **Plano gratuito do Gemini:** 20 requisições por dia nos modelos "flash"; o sistema usa um modelo
  "lite" na geração e fallback automático entre modelos.
- **Base anonimizada e datada:** nomes de lojas foram trocados pela Olist por casas de *Game of
  Thrones*; nada posterior a 2018.

## 13. Como executar e reproduzir

**Pré-requisitos:** Python 3.12, [uv](https://docs.astral.sh/uv/) e uma chave gratuita do Gemini
([Google AI Studio](https://aistudio.google.com/apikey)). GPU NVIDIA é opcional (acelera embeddings e
reranker; sem ela tudo roda em CPU, mais devagar).

```bash
uv sync
cp .env.example .env          # e preencha GEMINI_API_KEY
```

```bash
uv run voc prepare            # baixa o dataset do Kaggle e constrói a base (~1 min)
uv run voc build              # embeddings + ChromaDB + BM25 (~2 min com GPU)
uv run voc aspectos           # classificador de aspectos (usa os rótulos versionados em eval/)
```

```bash
uv run streamlit run app/streamlit_app.py        # interface
uv run voc ask "Quais são os principais problemas relatados pelos clientes?"
```

```bash
uv run voc avaliar            # avaliação completa (reaproveita julgamentos e cache)
uv run pytest                 # testes
```

**Reprodutibilidade:** dependências travadas em `uv.lock`; semente 42; embeddings em cache alinhados
por `review_id`; chamadas ao LLM em cache por hash (`.cache/llm`); rótulos de aspectos e
julgamentos de relevância versionados em `eval/`. Com a chave gratuita, uma pessoa consegue fazer
algumas dezenas de perguntas por dia no app; a avaliação completa consome a cota de mais de um dia
se rodada do zero (D19).

## 14. Estrutura do repositório

```
tech-challenge-fase4/
├── app/streamlit_app.py           # interface
├── src/voc_rag/
│   ├── data/                      # prepare.py (base), text.py (limpeza)
│   ├── indexing/                  # embeddings, ChromaDB, BM25, build
│   ├── retrieval/                 # query.py (análise), retriever.py (híbrido, RRF, MMR),
│   │                              # rerank.py, filters.py (metadados)
│   ├── generation/                # llm.py (Gemini, cache, fallback), answer.py (contexto,
│   │                              # prompt, validação de citações)
│   ├── themes/                    # taxonomia e classificador de aspectos
│   ├── evaluation/                # juiz, recuperação, geração, relatórios
│   ├── pipeline.py                # orquestração e abstenção
│   └── cli.py                     # `voc prepare | build | aspectos | ask | avaliar`
├── notebooks/
│   ├── 01_eda_avaliacoes.ipynb
│   ├── 02_pipeline_passo_a_passo.ipynb
│   └── 03_avaliacao.ipynb
├── eval/                          # perguntas, rótulos do LLM e julgamentos de relevância
├── reports/                       # decisões, métricas (JSON), exemplos, roteiro do vídeo
├── images/                        # gráficos e capturas
├── tests/
├── docs/enunciado.md
├── pyproject.toml / uv.lock
└── .env.example
```

## 15. Vídeo

Roteiro em [`reports/roteiro_video.md`](reports/roteiro_video.md).

<!-- VIDEO_LINK -->
**Vídeo:** link adicionado após a gravação.
