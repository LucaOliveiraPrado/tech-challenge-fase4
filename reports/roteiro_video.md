# Roteiro do Vídeo de Apresentação (até 7 minutos)

> Público: banca técnica da pós. O enunciado pede o **raciocínio técnico**, não só o
> funcionamento: cada bloco mostra uma decisão e a evidência que a sustenta. Tela dividida entre o
> apresentador e o material indicado entre parênteses (app em `uv run streamlit run
> app/streamlit_app.py`, notebooks e imagens de `images/`).

---

## Bloco 1: O problema (0:00 a 0:40)

**Fala:**

"Um e-commerce recebe milhares de avaliações. A nota diz se o cliente ficou satisfeito; o
comentário diz por quê. Só que ninguém lê 42 mil comentários, e um painel de notas não responde
'o que os clientes insatisfeitos relatam?' nem 'que evidências mostram que o prazo de entrega é um
problema recorrente?'.

Construímos um sistema de RAG sobre as avaliações da Olist que responde perguntas em linguagem
natural, mostra quais avaliações sustentam cada afirmação e se recusa a responder quando a base
não tem evidência."

*(Visual: `images/app_resposta.png`.)*

## Bloco 2: A base de conhecimento (0:40 a 1:30)

**Fala:**

"Partimos de 99 mil linhas de avaliações. Menos da metade tem comentário: são 42 mil documentos.
Decisão número um: uma avaliação é um documento, sem chunking, porque a mediana é de 9 palavras e
a avaliação é a unidade que o gestor quer ver citada.

A análise exploratória mudou o projeto em dois pontos. Primeiro, quem comenta é mais crítico: a
nota 1 é 11% das avaliações e 21% dos comentários; então todo número que o sistema mostra é
relativo aos comentários. Segundo, o atraso na entrega multiplica a insatisfação: por isso a
situação da entrega virou metadado de cada documento e filtro de busca."

*(Visuais: `eda_comentario_por_nota.png`, `eda_entrega_negativas.png`.)*

## Bloco 3: A arquitetura e o pipeline (1:30 a 3:00)

**Fala:**

"O pipeline tem cinco etapas. (mostrar o diagrama do README)

Um: um LLM analisa a pergunta. Ele decide se está no escopo, extrai filtros como 'nota baixa' ou
'cama, mesa e banho' e reescreve a pergunta no vocabulário do cliente. Isso importa porque o
gestor pergunta 'quais reclamações aparecem com mais frequência' e o cliente escreve 'comprei dia
10 e até hoje nada'.

Dois: busca híbrida. Um índice vetorial com bge-m3 no ChromaDB, com filtro de metadado dentro da
consulta, e um BM25 com stemming em português em que o 'não' não é stopword, porque 'não chegou'
e 'chegou' são opiniões opostas. As listas são fundidas por RRF.

Três: seleção. Um reranker cross-encoder avalia cada candidato contra a consulta reescrita
(contra a pergunta original ele dava relevância mediana de 0,002; contra a reescrita, 0,87). A
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

## Bloco 4: Demonstração (3:00 a 5:00)

**Ação na tela (app):**

1. "Quais reclamações relacionadas à entrega aparecem com maior frequência?" Mostrar a resposta,
   o gráfico de frequência dos temas e as evidências com borda azul. Abrir uma evidência e mostrar
   o `review_id`.
2. "O que os clientes mais elogiam na categoria cama, mesa e banho?" Abrir "Como a resposta foi
   construída": o filtro de categoria e o de nota foram extraídos da pergunta; mostrar o funil
   (recorte, candidatas, relevantes, contexto).
3. "Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao
   prazo de entrega?" Pergunta do tipo evidência: as avaliações vêm primeiro.
4. "Qual foi o faturamento da Olist em 2018?" Recusa por escopo.
5. "O que os clientes acharam das entregas feitas por drone?" As avaliações recuperadas falam de
   entrega, mas nenhuma de drone: a geração recusa e explica por quê.

**Fala (durante 4 e 5):** "Responder é fácil; o difícil é saber quando não responder. São três
camadas: escopo na análise da pergunta, relevância no reranker e suficiência na geração."

## Bloco 5: Como sabemos que funciona (5:00 a 6:15)

**Fala:**

"Medimos. Montamos 40 perguntas: os cinco tipos do enunciado, oito com metadados, seis fora do
escopo e seis sem evidência na base. A relevância foi julgada por pooling, como em avaliações de
busca, com um LLM juiz diferente do que gera as respostas.

A ablação mostra o caminho: o RAG ingênuo, com a pergunta crua contra o vetor, coloca 61% de
evidência clara no top-10; a reescrita sobe para 80%; com metadados e o porteiro, o sistema final
chega a 94%. E medir mudou o sistema: multi-query, HyDE e a reordenação pelo reranker pioraram a
precisão e ficaram de fora. Isso só aparece porque medimos.

O bge-m3 venceu dois outros modelos de embedding na mesma configuração.

Nas perguntas com recorte, os metadados levam a conformidade ao recorte de 42% para 91%, e a
precisão de 0,39 para 0,85.

Ponta a ponta: 40 de 40 decisões corretas entre responder e abster, 100% das citações válidas e
fidelidade de 0,96 nos insights, auditada por um modelo diferente do que gera."

*(Visuais: `avaliacao_ablacao.png`, tabelas do README, notebook 03.)*

## Bloco 6: Desafios e decisões (6:15 a 6:50)

**Fala:**

"Quatro desafios. O primeiro foi a distância entre a linguagem do gestor e a do cliente,
resolvida com a reescrita da pergunta. O segundo foi a frequência: RAG recupera, não conta, daí o
classificador de aspectos com correção de prevalência. O terceiro foi medir com honestidade: o
juiz precisou ver os metadados nas perguntas com recorte, senão zerava respostas certas. O
quarto foi a cota gratuita do Gemini, de 20 requisições por dia por modelo: papéis separados por
modelo, fallback automático, cache e julgamentos salvos a cada pergunta, e a avaliação aborta se
o LLM cair, para nunca medir um sistema diferente do real."

## Bloco 7: Fecho (6:50 a 7:00)

**Fala:** "Código, avaliação, os julgamentos e as 22 decisões técnicas estão no repositório,
reproduzíveis com quatro comandos. Obrigado."

---

## Checklist de gravação

- [ ] Até 7 minutos: a fala soma ~810 palavras (~5,5 min a 150 palavras por minuto), então a
      demonstração no app precisa caber em ~1,5 min (perguntas já em cache respondem na hora);
- [ ] Os oito itens do enunciado: problema, arquitetura, estratégia do RAG, recuperação,
      demonstração prática, exemplos de perguntas, evidências recuperadas, desafios e decisões;
- [ ] App já aberto e aquecido antes de gravar (primeira pergunta carrega os modelos);
- [ ] Perguntas da demonstração já feitas uma vez (cache do LLM: resposta instantânea e sem gastar
      cota na gravação);
- [ ] Publicar o vídeo (asset do release ou YouTube não listado) e pôr o link no README.
