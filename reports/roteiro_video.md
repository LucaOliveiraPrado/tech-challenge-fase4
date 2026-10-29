# Roteiro do Vídeo de Apresentação (até 7 minutos)

> Público: banca técnica da pós. O enunciado pede o **raciocínio técnico**, não só o
> funcionamento: cada bloco mostra uma decisão e a evidência que a sustenta. Tela dividida entre o
> apresentador e o material indicado entre parênteses (app em `uv run streamlit run
> app/streamlit_app.py`, notebooks e imagens de `images/`).

---

## Bloco 1: O problema (0:00 a 0:35)

**Fala:**

"Um e-commerce recebe milhares de avaliações. A nota diz se o cliente ficou satisfeito; o
comentário diz por quê. Só que ninguém lê 42 mil comentários, e um painel de notas não responde
'o que os clientes insatisfeitos relatam?' nem 'que evidências mostram que o prazo de entrega é um
problema recorrente?'.

Construímos um sistema de RAG sobre as avaliações da Olist que responde perguntas em linguagem
natural, mostra quais avaliações sustentam cada afirmação e se recusa a responder quando a base
não tem evidência."

*(Visual: `images/app_resposta.png`.)*

## Bloco 2: A base de conhecimento (0:35 a 1:20)

**Fala:**

"Partimos de 99 mil linhas de avaliações. Menos da metade tem comentário: são 42 mil documentos.
Decisão número um: uma avaliação é um documento, sem chunking, porque a mediana é de 9 palavras e
a avaliação é a unidade que o gestor quer ver citada.

A análise exploratória mudou o projeto em dois pontos. Primeiro, quem comenta é mais crítico: a
nota 1 é 11% das avaliações e 21% dos comentários; então todo número que o sistema mostra é
relativo aos comentários. Segundo, o atraso na entrega multiplica a insatisfação: por isso a
situação da entrega virou metadado de cada documento e filtro de busca."

*(Visuais: `eda_comentario_por_nota.png`, `eda_entrega_negativas.png`.)*

## Bloco 3: A arquitetura e o pipeline (1:20 a 2:55)

**Fala:**

"O pipeline tem cinco etapas. (mostrar o diagrama do README)

Um: um LLM analisa a pergunta. Ele decide se está no escopo, extrai filtros como 'nota baixa' ou
'cama, mesa e banho' e reescreve a pergunta no vocabulário do cliente. Isso importa porque o
gestor pergunta 'quais reclamações aparecem com mais frequência' e o cliente escreve 'comprei dia
10 e até hoje nada'.

Dois: busca híbrida. Um índice vetorial com bge-m3 no ChromaDB, com filtro de metadado dentro da
consulta, e um BM25 com stemming em português em que o 'não' não é stopword, porque 'não chegou'
e 'chegou' são opiniões opostas. As listas são fundidas por RRF.

Três: seleção. Um reranker cross-encoder avalia cada candidato contra a consulta reescrita. A
hipótese era usar ele para reordenar, mas a avaliação mostrou o contrário: ele confunde temas
vizinhos e piorou a precisão. Então a ordem final é a da fusão, e o reranker virou porteiro: só
decide se há evidência relevante o bastante.

Quatro: o contexto. Evidências numeradas, com nota, atraso e categoria de cada uma. Em perguntas
de panorama entra também um quadro de frequências, porque o top-k mostra as avaliações mais
relevantes, mas não conta: um classificador de aspectos estima a frequência de cada tema na base
inteira.

Cinco: a geração devolve JSON, e o código verifica cada citação. Citação que não existe é
removida e insight sem evidência é descartado."

*(Visuais: diagrama mermaid do README; `images/app_rastro.png`; notebook 02, etapas 1 e 4.)*

## Bloco 4: Demonstração (2:55 a 4:45)

**Ação na tela (app) e fala de cada pergunta:**

1. "Quais reclamações relacionadas à entrega aparecem com maior frequência?" Mostrar a resposta,
   o gráfico de frequência e as evidências com borda azul; abrir "Evidências do insight 1".
   **Fala:** "Cada insight abre as avaliações que o sustentam, com o `review_id` da Olist. O
   percentual não vem das 30 evidências: vem do classificador de aspectos sobre todos os
   comentários do recorte, e a resposta diz qual é esse denominador."
2. "O que os clientes mais elogiam na categoria cama, mesa e banho?" Abrir "Como a resposta foi
   construída". **Fala:** "O filtro de categoria e o de nota saíram da própria pergunta. O funil
   mostra o recorte, as candidatas da busca híbrida, as que passaram no porteiro e as que foram
   para o contexto."
3. "Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao
   prazo de entrega?" **Fala:** "Aqui o gestor pede a prova: cada citação aponta uma avaliação
   real, e a legenda mostra que nenhuma citação inválida passou pela verificação do código."
4. "Qual foi o faturamento da Olist em 2018?" Recusa por escopo.
5. "O que os clientes acharam das entregas feitas por drone?" As avaliações recuperadas falam de
   entrega, mas nenhuma de drone: a geração recusa e explica por quê.

**Fala (durante 4 e 5):** "Responder é fácil; o difícil é saber quando não responder. São três
camadas: escopo na análise da pergunta, relevância no porteiro e suficiência na geração."

## Bloco 5: Como sabemos que funciona (4:45 a 6:05)

**Fala:**

"Medimos. Montamos 44 perguntas: os cinco tipos do enunciado, onze com metadados, seis fora do
escopo e sete sem evidência na base. A relevância foi julgada por pooling, como em avaliações de
busca, com um LLM juiz diferente do que gera as respostas.

A ablação mostra o caminho: o RAG ingênuo, com a pergunta crua contra o vetor, coloca 56% de
evidência clara no top-10; a reescrita sobe para 70%; com os filtros de metadado, o sistema final
chega a 93%. E medir mudou o sistema: multi-query, HyDE e a reordenação pelo reranker pioraram o
sistema completo e ficaram de fora. Isso só aparece porque medimos.

Nas perguntas com recorte, inclusive pagamento, valor e número de vendedores, os metadados levam a
conformidade ao recorte de 31% para 96%, e a precisão de 0,27 para 0,87. E revelam padrão: pedidos
com mais de um vendedor têm 61% de avaliações negativas, contra 26% no geral.

Ponta a ponta: 44 de 44 decisões corretas entre responder e abster, 100% das citações válidas e
fidelidade de 0,96 nos insights, auditada por um modelo diferente do que gera. Como as perguntas
são nossas e guiaram as escolhas, tratamos esses números como de desenvolvimento."

*(Visuais: `avaliacao_ablacao.png`, tabelas do README, notebook 03.)*

## Bloco 6: Desafios e decisões (6:05 a 6:40)

**Fala:**

"Três desafios. O primeiro foi a distância entre a linguagem do gestor e a do cliente,
resolvida com a reescrita da pergunta. O segundo foi medir com honestidade: o juiz precisou ver
os metadados nas perguntas com recorte, senão zerava respostas certas. O terceiro foi a cota gratuita do Gemini, de 20 requisições por dia por modelo: papéis separados por
modelo, fallback automático, cache e julgamentos salvos a cada pergunta, e a avaliação aborta se
o LLM cair, para nunca medir um sistema diferente do real."

## Bloco 7: Fecho (6:40 a 6:50)

**Fala:** "Código, avaliação, os julgamentos e as 23 decisões técnicas estão no repositório,
reproduzíveis com quatro comandos. Obrigado."

---

## Checklist de gravação

- [ ] Até 7 minutos: a fala soma ~840 palavras (~5,6 min a 150 palavras por minuto); com ~1 min
      de cliques e digitação na demonstração, o total fica perto de 6:50. Ensaiar com cronômetro;
      se passar de 6:45, encurtar o bloco 3 (é o mais longo, ~1:30 de fala);
- [ ] Os oito itens do enunciado: problema, arquitetura, estratégia do RAG, recuperação,
      demonstração prática, exemplos de perguntas, evidências recuperadas, desafios e decisões;
- [ ] App já aberto e aquecido antes de gravar (primeira pergunta carrega os modelos);
- [ ] Perguntas da demonstração já feitas uma vez (cache do LLM: resposta instantânea e sem gastar
      cota na gravação);
- [ ] Publicar o vídeo (asset do release ou YouTube não listado) e pôr o link no README.
