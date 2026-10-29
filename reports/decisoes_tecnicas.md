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
| paraphrase-multilingual-MiniLM-L12-v2 | 0,632 | 0,645 |
| multilingual-e5-base | 0,632 | 0,651 |
| **bge-m3** | **0,713** | **0,733** |

A vantagem de P@10 (+0,08 contra cada um) tem intervalo de confiança de 95% por bootstrap
pareado que exclui o zero (tabela do README). Numa rodada anterior, com outra versão do prompt de
análise, o intervalo encostava no zero: com 31 perguntas a ordem dos modelos é estável, a margem
nem tanto.
Local e não via API: indexar ~42 mil documentos sem limite de requisições, custo zero e vetores
reproduzíveis por qualquer avaliador (105 s na GPU; roda em CPU, mais devagar).

### D9: ChromaDB + BM25 (busca híbrida)

**Decisão:** ChromaDB persistente (embutido, sem servidor, HNSW com cosseno e filtro de
metadado na própria consulta) para a busca semântica; BM25 (`bm25s`, stemming Snowball em
português, acentos removidos) para termos exatos ("correios", "nota fiscal", "lacrado").
**Detalhe que importa:** as negações (`não`, `nunca`, `nem`, `sem`, `só`, `ainda`) **não** estão
nas stopwords: "não chegou" e "chegou" são opiniões opostas.
**Evidência:** na pergunta do notebook 02 (sistema final, uma consulta), dos 80 candidatos 36
vieram só do BM25, 36 só do vetor e 8 dos dois índices: as duas buscas trazem conjuntos bem
diferentes. Na média da avaliação, porém, o BM25 **não melhora** a P@10 (0,713 só vetor contra
0,703 híbrido; 0,713 contra 0,703 também com várias consultas), um empate. Numa rodada anterior
o híbrido ficava levemente à frente (0,713 contra 0,703 só vetor): o efeito é pequeno e oscila com a
redação da consulta. Fica no sistema final pelo custo desprezível (milissegundos) e pela
robustez a termos exatos e negações, que a média das 31 perguntas não isola.

### D10: Transformação da pergunta por LLM

**Problema:** a pergunta do gestor é analítica ("quais reclamações aparecem com maior
frequência?"), o documento é coloquial ("comprei dia 10 e até hoje nada").
**Decisão:** uma chamada estruturada (JSON validado por Pydantic) produz escopo, tipo
(panorama/tema/evidência), polaridade, filtros explícitos, consulta reescrita no vocabulário do
cliente, 2 a 3 variações (multi-query) e uma avaliação hipotética (HyDE).
**Escopo decidido em código:** o LLM responde três perguntas objetivas (é sobre experiência de
compra? cita algo posterior a 2018? tenta mudar as instruções?) e o código decide o escopo (D15).
**Consulta sem o recorte:** o prompt pede que o que já virou filtro (vendedores, pagamento,
valor, região, categoria) não entre na consulta reescrita, que deve descrever o relato. Quando a
consulta só descrevia o recorte ("vários vendedores, lojas diferentes"), o porteiro não
reconhecia as avaliações, que falam de "faltou produto", e a pergunta sobre pedidos com mais de
um vendedor caía para 1 evidência relevante. Na rodada final o modelo ainda mantém "lojas
diferentes" nessa consulta, mas ela passou a descrever o relato ("faltou um produto, entrega
separada") e o porteiro reconhece 53 relevantes.
**Regra de fidelidade:** as variações não podem generalizar o assunto. Sem ela, "entregas por
drone" virava "entrega rápida drone" e recuperava elogios genéricos de entrega com relevância
0,99.
**Evidência:** a reescrita é o maior ganho isolado do projeto: P@10 de **0,561 → 0,713** e
nDCG@10 de 0,619 → 0,733 (pergunta crua contra consulta reescrita, mesma busca vetorial). No
espaço vetorial, o cosseno médio com 200 reclamações de entrega sobe de 0,51 para 0,65
(notebook 02). Já **multi-query e HyDE não trazem ganho**: isolados, empatam (0,713 → 0,713); no
sistema completo, também não melhoram (0,929 → 0,916, empate técnico), porque as variações puxam
temas vizinhos mesmo com a regra de fidelidade, e custam chamadas a mais. Numa primeira rodada da avaliação, com 28 perguntas, já tinham
piorado também isolados (0,800 → 0,750). Por isso o sistema final usa só a consulta reescrita; as variações e a avaliação hipotética continuam implementadas, medidas e
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
contra a pergunta original. Na pergunta do notebook 02, o escore mediano dos 80 candidatos é
**0,0** contra a pergunta analítica e **0,94** contra a reescrita: o modelo foi treinado em pares
pergunta→trecho-que-responde, e nenhuma avaliação "responde" literalmente a uma pergunta sobre o
que os clientes dizem.
**Segundo achado (a avaliação refutou a hipótese):** mesmo assim, ordenar pelo reranker
**piorou** a recuperação em todas as variantes testadas:

| Ordenação (mesmas candidatas) | P@10 |
|---|---|
| fusão RRF, sem reranker | 0,703 |
| reranker, maior escore entre as consultas | 0,655 |
| reranker contra a consulta principal | 0,674 |
| reranker pela média das consultas | 0,639 |

A análise pergunta a pergunta mostra o mecanismo: o cross-encoder confunde temas vizinhos.
Numa pergunta sobre **embalagem** ele põe "Produto veio quebrado" no topo; nas de elogio ao
**atendimento** e de pedidos atrasados, o mesmo padrão (notebook 03, seção 2). O vetor com a consulta reescrita mantém o assunto exato.
**Decisão:** a ordem final é a da fusão RRF; o reranker continua no pipeline como **porteiro de
relevância** (D13), papel em que a sobreposição temática é tolerável. Resultado no sistema
completo: P@10 0,861 (ordem do reranker) → **0,929** (ordem RRF, reranker como porteiro), a
única diferença da tabela de técnicas descartadas cujo intervalo de confiança exclui o zero. O
resultado se repetiu em todas as rodadas da avaliação.

### D13: Limiar do porteiro escolhido pelo papel de abstenção

**Evidência:** sobre 2.179 pares julgados, o escore do reranker tem AUC 0,833 contra o juiz, e a
precisão das evidências varia pouco entre limiares (0,88 em 0,05; 0,90 em 0,30; 0,92 em 0,90),
enquanto o recall cai de 0,97 para 0,56. Ou seja: o limiar não serve para filtrar evidência; o
que ele faz é identificar perguntas sem evidência sem recusar as respondíveis: entre 0,1 e 0,5,
**nenhuma** das 31 respondíveis fica abaixo do mínimo, e de 0,2 a 0,5 ele barra 4 das 6
perguntas sem evidência que chegam à recuperação (as 2 restantes, drone e painel solar, ficam
para a geração). Com tão poucos casos, não há base estatística para ajustar o limiar fino.
**Decisão:** limiar 0,30 (recall 0,88) e mínimo de 3 evidências acima dele; abaixo disso o
sistema mostra o que encontrou e não generaliza.
**Limite conhecido:** o reranker é tolerante à sobreposição de palavras: "entregas feitas por
drone" tem candidatos com 0,85 porque falam de "entrega". Por isso a decisão fina de suficiência
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
| Relevância | reranker + limiar | nenhuma evidência acima do limiar; menos de 3 relevantes | "O que os clientes dizem sobre a instalação de ar-condicionado feita pela loja?" |
| Suficiência | geração | evidências tocam o tema mas não respondem | "O que os clientes acharam das entregas feitas por drone?" (evidências só sobre entrega comum) |

**Por que três:** cada camada é mais cara e mais fina que a anterior. Abster cedo economiza
chamadas; abster tarde pega o que o limiar numérico não vê.
**Evidência:** nas 44 perguntas da avaliação, **44 de 44** decisões entre responder e abster
foram corretas: as 31 respondíveis foram respondidas e as 13 que deviam ser recusadas foram:
7 por escopo (as 6 fora do escopo, incluindo a *prompt injection*, e o iPhone 15, escrito como
"sem evidência" mas recusado pela regra de data, por ser posterior à base), 4 pelo porteiro (cashback, criptomoeda, retirada
em loja, instalação de ar-condicionado) e 2 pela geração (drone, painel solar), em que a
recuperação trouxe avaliações sobre "entrega" e "instalação" e o LLM reconheceu que elas não
tratam do assunto perguntado (`reports/avaliacao_geracao.json`).
**Escopo derivado em código:** na rodada anterior versionada, o modelo marcava como "fora do
escopo" temas de compra só ausentes da base (cashback, criptomoeda, retirada em loja) e
justificava com fatos que não podia saber ("não possui um programa de cashback"); numa rodada
intermediária, fez o mesmo com drone e ar-condicionado, contrariando o próprio prompt. A decisão
saiu do texto livre: o LLM responde três perguntas objetivas (experiência de compra; algo
posterior a 2018; tentativa de manipular as instruções) e `decide_escopo` deriva o escopo só
delas (`tests/test_escopo.py`). Na rodada final, o campo livre concordou com a regra nas 44
perguntas; a regra é a garantia, e a melhora veio sobretudo do prompt reescrito.
**Evidência insuficiente sem rótulo enganoso:** quando menos de 3 avaliações passam pelo limiar,
a resposta as mostra "para conferência, sem verificação de que tratam do tema", em vez de
chamá-las de relevantes: em criptomoedas, a única acima do limiar diz "o produto recebido veio
errado". O motivo escrito pelo LLM nunca chega à resposta do usuário; aparece só
no rastro técnico, identificado como tal.

### D16: Saída estruturada e citações verificadas por código

**Decisão:** o LLM devolve JSON (`resumo`, `insights[{titulo, descricao, evidencias}]`,
`limitacoes`, `suficiente`). O código remove ids inexistentes, aceita os formatos `[R1]`,
`[R1, R2]` e `[R1; R2]`, normaliza para `[R1][R2]` e descarta insight sem evidência válida. Cada
insight mostra o apoio ("apoio: 16 de 30 evidências") e cada `[R#]` leva a um `review_id` real.
**Por que:** rastreabilidade não pode depender de o modelo obedecer ao prompt.
**Evidência:** 714 citações nas respostas geradas, **100% válidas**; 103 insights, nenhum
descartado por falta de evidência. A auditoria do juiz (modelo diferente do gerador) julgou 101
dos 103 insights como **sustentados** e 2 como parciais (escore 0,99); 96,8% dos resumos foram
julgados integralmente sustentados. Das avaliações citadas que o juiz de relevância julgou para
a pergunta, 93,2% são evidência clara.
**O que a auditoria ensinou:** a primeira auditoria da rodada final deu 0,93, com três causas.
(1) O modelo anexava marcas `[R#]` a percentuais do quadro de frequências; o prompt passou a
exigir que número do quadro fique numa frase sem citação. (2) O auditor recebia só o texto das
evidências, sem os metadados que o gerador viu ("pago com boleto" parecia extrapolação); ele
passou a ver o mesmo contexto do gerador. (3) Extrapolações reais ("esperas de meses") levaram a
uma regra contra quantificar além das evidências. Com as três correções, 0,93 → 0,96. Na rodada
final, o auditor passou a receber o quadro exatamente como o gerador o viu (com o denominador) e
a conferir qualificadores ao lado dos números ("antes do prazo", "pontuais"); a resposta ganhou
uma linha, escrita pelo código, com o denominador dos percentuais: 0,96 → 0,99.
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
grandeza. O quadro entra nas perguntas de panorama e nas de evidência: pedir as avaliações que
sustentam um problema "recorrente" é pedir frequência, e sem o quadro a resposta só podia contar
a amostra. A resposta traz, escrita pelo código, a linha com o denominador dos percentuais
(quantas avaliações do recorte), para o leitor não confundir a frequência com a amostra.
**Limite:** aspectos raros (elogio ao atendimento, embalagem) têm F1 baixo (0,42 e 0,60).

## Metadados (desafio adicional)

### D18: Metadados como filtro dentro do banco vetorial

**Decisão:** filtros explícitos da pergunta viram cláusula `where` no Chroma e máscara no BM25
(a mesma definição gera as duas, com teste de equivalência): nota, categoria, período, situação
da entrega, UF, região e **informações do pedido** (forma de pagamento, faixa de valor dos itens,
pedido com mais de um vendedor). A polaridade vira filtro implícito de nota (problemas: nota ≤ 3;
elogios: nota ≥ 4) quando a pergunta não fixa nota; o campo `sentimentos` que o LLM às vezes
preenche é descartado para não estreitar o recorte duas vezes.
**Como os metadados melhoram a recuperação:** sem filtro, a busca vetorial acha o **tema** certo
fora do **recorte** pedido (reclamação de móveis numa pergunta sobre cama, mesa e banho; nota 4
numa pergunta sobre nota 1; pedido de cartão numa pergunta sobre boleto), e essas avaliações
ocupam vagas do contexto. Com o filtro dentro da consulta, o recorte é respeitado por construção
e as vagas vão para evidências do recorte. Os metadados também entram no **contexto** de cada
evidência (nota, atraso em dias, categoria, pagamento, valor, vendedores), o que deixa o LLM
interpretar "demorou" à luz de um pedido 12 dias atrasado.
**Evidência:** nas 11 perguntas com recorte (8 de nota, categoria, período, entrega e região; 3
de informações do pedido), julgadas com os metadados visíveis para o juiz:

| Perguntas com recorte | P@10 | Conformidade ao recorte (top-10) |
|---|---|---|
| sem filtros (mesma configuração do sistema final) | 0,236 | 27,3% |
| sistema final (filtros + ordem RRF) | **0,900** | **98,2%** |

Nas 3 perguntas de informações do pedido, a P@10 vai de 0,0 a 0,2 sem filtro para 1,0 com
filtro. As informações do pedido também revelam padrão: pedidos com itens de **mais de um
vendedor** têm 61,3% de avaliações negativas, contra 25,7% na base de comentários.
A conformidade não chega a 100% porque o filtro aplicado é o que a análise da pergunta extraiu:
quando o LLM amplia um campo (ex.: "móveis" incluindo móveis de escritório e de sala), o recorte
fica mais largo que o pedido. A extração dos filtros esperados foi correta nas 11 perguntas.

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
| Análise da pergunta e geração | `gemini-3.5-flash-lite` | `gemini-3.1-flash-lite` | cota diária compatível com uso e avaliação; JSON estável |
| Rotulagem de aspectos | `gemini-3.5-flash-lite` | n/a | tarefa simples em lote |
| Juiz da avaliação | `gemini-3.6-flash` | `gemini-3.7-flash`, `gemini-3.8-flash`, `gemini-3.1-flash-lite` | modelo diferente do gerador, reduz autoaprovação; o último da lista é o juiz de reserva quando a cota dos "flash" acaba |

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
contextos finais e uma amostra ao longo do ranking, forma o conjunto julgado (8.680 pares); o
juiz atribui relevância 0/1/2 com critério escrito à mão por pergunta; julgamentos versionados em
`eval/julgamentos_relevancia.csv`, com o modelo que julgou cada par. Fidelidade dos insights
auditada pelo juiz contra as evidências citadas.
**Correção durante o projeto:** a primeira rodada julgava só o texto. Nas perguntas com recorte
("reclamações do Nordeste", "elogios em beleza e saúde"), o juiz não tinha como saber a região
ou a categoria e zerava avaliações corretas. Nas perguntas com recorte ele passou a ver os metadados de
cada avaliação, e os julgamentos foram refeitos.
**Juízes efetivos:** a cota gratuita dos modelos "flash" acaba no meio de cada rodada; dos 8.680
pares, 5.940 foram julgados pelo `gemini-3.1-flash-lite`, 1.896 pelo `gemini-3.6-flash`, 486 pelo
`gemini-3.7-flash` e 358 pelo `gemini-3.8-flash`; 34 das 37 perguntas julgadas têm pares de dois
ou três modelos. Cada par é julgado uma vez e reaproveitado; as configurações de uma pergunta são
medidas sobre os mesmos julgamentos, então a comparação entre configurações é justa mesmo com
juízes mistos.
**Concordância entre juízes:** 6 perguntas, escolhidas à mão para cobrir os grupos (não
sorteadas), com os 626 pares julgados até então (as rodadas seguintes acrescentaram pares a essas
perguntas, que não foram rejulgados), rejulgadas pelo `gemini-3.5-flash`:
concordância exata de 90,4% na escala 0/1/2 (kappa ponderado 0,887) e de 96,0% na decisão
"evidência clara", a usada na P@10 (kappa 0,916). Kappa acima de 0,8 é concordância quase
perfeita: o juiz de reserva mede o mesmo que um modelo "flash"
(`reports/concordancia_juizes.json`).
**Limite:** os juízes são LLMs e podem compartilhar vieses; não houve dupla anotação humana em
escala. A concordância acima vale para a **relevância**; a **fidelidade** dos insights teve um
único juiz (o de reserva, `gemini-3.1-flash-lite`), por isso o README reporta também o critério
estrito (insights integralmente sustentados) ao lado do escore com meio ponto para "parcial".

### D22: Reprodutibilidade

`uv` com `uv.lock` (Python 3.12), torch CUDA no Windows/Linux com fallback para CPU, dataset
baixado do Kaggle por `kagglehub` (sem login), embeddings em cache alinhados por `review_id`,
semente 42, cache das chamadas ao LLM e rótulos/julgamentos versionados.
**Atalho para quem avalia:** reproduzir do zero exige GPU (42 mil embeddings `bge-m3`) e uma
chave do Gemini com cota de mais de um dia para a avaliação completa. A release `artefatos-v2`
(120 MB) leva a base processada, os embeddings e o cache do LLM; `voc baixar` extrai só os
caminhos esperados e `voc build` monta ChromaDB e BM25 em cerca de um minuto. Validado num clone
limpo, em CPU e sem chave: as perguntas da avaliação reproduzem as mesmas decisões (respondida,
fora de escopo, sem evidência) a partir do cache. Alternativas descartadas: versionar o índice
no git (1,2 GB) e publicar o ChromaDB pronto (amarrado à versão do Chroma e aos três modelos da
comparação de embeddings).

### D23: Conjunto de perguntas: desenvolvimento, não teste retido

**Problema:** não existe um conjunto público de perguntas de gestores com respostas esperadas
para esta base.
**Decisão:** 44 perguntas escritas pela equipe (`eval/perguntas.json`): os cinco tipos do
enunciado, as perguntas do problema de negócio, 11 com recorte por metadado, 6 fora do escopo e
7 sem evidência, cada respondível com um critério de relevância escrito à mão.
**Limite assumido:** o mesmo conjunto guiou as escolhas (sistema final, ordem RRF, limiar 0,30,
redação dos prompts) e mediu o resultado. Na rodada final, os exemplos do prompt de análise que
coincidiam com temas do teste (drone, cashback, faturamento, R$ 500) foram trocados por temas que
não estão nas perguntas (motoboy, vale-presente, voucher, R$ 1.000); mesmo assim, o prompt foi
ajustado três vezes olhando estas 44 perguntas (escopo em código, recorte fora da consulta). Os
números são, portanto, de desenvolvimento:
comparam bem as configurações entre si (todas medidas sobre os mesmos julgamentos), mas tendem a
ser otimistas como estimativa absoluta. Com 13 recusas esperadas, "13 de 13" tem intervalo de
confiança de Wilson de 95% entre 0,77 e 1,00. A forma correta de estimar sem viés é um conjunto
retido, escrito depois de congelado o sistema e rodado uma única vez.
