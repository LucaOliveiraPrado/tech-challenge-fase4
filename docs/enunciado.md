# Tech Challenge Fase 4 (IAST): Voice of Customer Intelligence com RAG

> Conversão do PDF oficial `[IAST] - Tech Challenge - Fase 4.pdf` (12 páginas)
> para Markdown. Conteúdo do enunciado preservado; a seção final
> ("Checklist de entrega") é nossa, derivada dos requisitos.

---

## Regras gerais

- O Tech Challenge engloba os conhecimentos de todas as disciplinas da fase.
- Atividade em grupo, **obrigatória**, com prazo de entrega.
- Vale **90% da nota final**.

### Bônus opcional: Databricks (+10 pontos na nota final, individual)

- Trilha **Generative AI Engineering Pathway** na Databricks Academy (parceria
  com a POSTECH).
- Quem concluir a trilha pode ganhar **+10 pontos** na nota final.
- Comprovação (enviada pela própria Databricks Academy), uma destas:
  - certificado de conclusão da formação, se a trilha disponibilizar; ou
  - print da área *My Courses and Learning Plans / My Activities* com os
    conteúdos da trilha como **Completed**; ou
  - badge da formação, se a Databricks disponibilizar.
- A comprovação precisa identificar nome/conta e a conclusão dos cursos.

---

## Contexto

Empresas de e-commerce recebem milhares de avaliações por dia. Notas
(quantitativo) mostram o nível de satisfação, mas os insights mais relevantes
estão nos **comentários textuais** (não estruturados). Eles respondem perguntas
como:

- Quais são os principais motivos de insatisfação dos clientes?
- Quais problemas aparecem com maior frequência nas avaliações?
- O que os consumidores mais valorizam na experiência?
- Quais padrões aparecem em relatos sobre entrega, qualidade dos produtos ou
  atendimento?
- Quais evidências nos comentários sustentam determinado insight?

Análise manual de milhares de comentários é complexa, demorada e pouco
escalável. IA Generativa com **Retrieval-Augmented Generation (RAG)** transforma
esse volume em base de conhecimento explorável: perguntas em linguagem natural,
respostas fundamentadas nas experiências reais dos clientes.

## O desafio

Desenvolver uma solução de **Voice of Customer Intelligence baseada em RAG**
para explorar as avaliações da base **Brazilian E-Commerce Public Dataset by
Olist**.

- ~100 mil pedidos, 2016 a 2018: pedidos, produtos, pagamentos, entregas e
  avaliações escritas pelos consumidores.
- **Foco principal:** conteúdo textual das avaliações.
- Fonte: <https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data>

## Problema de negócio

A equipe faz parte de um e-commerce que quer entender a voz do cliente. Há
milhares de avaliações armazenadas, mas os gestores não conseguem identificar
rapidamente problemas, elogios e padrões. A equipe deve construir uma solução
de IA que transforme os comentários em **base de conhecimento inteligente e
explorável**.

Perguntas que gestores e analistas devem conseguir fazer:

- Quais são os principais problemas relatados pelos clientes?
- Quais reclamações relacionadas à entrega aparecem com maior frequência?
- O que os clientes mais elogiam em suas experiências de compra?
- Quais problemas são relatados por clientes insatisfeitos?
- Existem padrões recorrentes nas avaliações relacionadas à qualidade dos
  produtos?

A solução deve **recuperar avaliações relevantes** da base e usar essas
evidências como **contexto para gerar a resposta**.

## Objetivo da solução: arquitetura RAG

Fluxo esperado:

```
Pergunta do usuário
  ↓
Processamento da pergunta
  ↓
Representação vetorial / Embeddings
  ↓
Recuperação das avaliações mais relevantes
  ↓
Construção do contexto
  ↓
Geração da resposta utilizando um modelo de linguagem
  ↓
Resposta fundamentada nas evidências recuperadas
```

Tecnologias, modelos, estratégia de embeddings, banco vetorial e técnicas de
recuperação: **escolha da equipe**.

---

## Requisitos (mínimo obrigatório)

### 1. Construção da Base de Conhecimento

Processar o conteúdo textual das avaliações. **Definir e justificar** as
estratégias de:

- [ ] seleção dos dados;
- [ ] limpeza e preparação dos textos;
- [ ] tratamento de valores ausentes;
- [ ] organização dos documentos usados pela solução;
- [ ] criação dos embeddings;
- [ ] armazenamento e indexação das informações.

### 2. Implementação do Pipeline RAG

Pipeline que recupera informação relevante a partir da pergunta do usuário.
**Demonstrar** como ocorre:

- [ ] a transformação da pergunta;
- [ ] a recuperação semântica das avaliações;
- [ ] a seleção dos conteúdos mais relevantes;
- [ ] a construção do contexto enviado ao modelo de linguagem;
- [ ] a geração da resposta final.

Estratégias diferentes de recuperação e enriquecimento são permitidas, desde que
**justificadas tecnicamente**.

### 3. Respostas fundamentadas em evidências

- A resposta deve estar fundamentada nos comentários da base.
- Sempre que possível, **apresentar ao usuário as evidências** usadas,
  permitindo identificar **quais avaliações** contribuíram para cada insight.
- **Critério de avaliação explícito:** não serão avaliadas apenas respostas bem
  escritas. Será avaliada **principalmente** a capacidade de **recuperar
  informação relevante** e gerar respostas **coerentes com as evidências**.

### 4. Tratamento de perguntas sem evidências suficientes

O sistema deve reconhecer suas limitações e **não gerar informação sem suporte
nos dados** quando:

- [ ] não existem avaliações relevantes para a pergunta;
- [ ] as evidências recuperadas são insuficientes;
- [ ] a pergunta está fora do escopo da base de conhecimento.

---

## Exemplos de exploração

| Tipo | Pergunta |
|---|---|
| Investigação de reclamações | Quais são os principais problemas relatados pelos clientes em suas avaliações? |
| Tema específico | O que os clientes relatam sobre problemas relacionados à entrega? |
| Experiências positivas | Quais aspectos da experiência de compra são mais elogiados pelos clientes? |
| Insatisfação | Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos? |
| Baseada em evidências | Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega? |

## Desafio adicional (não obrigatório): metadados e exploração contextual

Enriquecer o RAG com informações adicionais da base, por exemplo:

- nota da avaliação;
- período da compra;
- informações do pedido;
- informações de entrega;
- categoria dos produtos.

Perguntas que isso habilita:

- Quais são os principais problemas relatados nas avaliações com nota baixa?
- O que os clientes mais elogiam em determinadas categorias de produtos?
- Quais temas aparecem nas avaliações relacionadas a experiências de entrega
  insatisfatórias?

**Obrigatório se usar:** justificar **como os metadados contribuem para a
qualidade da recuperação**.

---

## Entregáveis

### 1. Repositório público no GitHub

Conteúdo mínimo:

- [ ] código-fonte da solução;
- [ ] instruções de instalação e execução;
- [ ] `README.md` explicando o projeto;
- [ ] descrição da arquitetura;
- [ ] tecnologias e bibliotecas utilizadas;
- [ ] estratégia de construção do pipeline RAG;
- [ ] explicação da preparação da base;
- [ ] justificativa das principais decisões técnicas;
- [ ] exemplos de perguntas e respostas;
- [ ] informações para reproduzir a solução.

**Organização e clareza do repositório também contam na nota.**

### 2. Vídeo de apresentação (até 7 minutos)

Demonstrar de forma objetiva:

- [ ] o problema de negócio;
- [ ] a arquitetura proposta;
- [ ] a estratégia do pipeline RAG;
- [ ] como ocorre a recuperação das avaliações relevantes;
- [ ] demonstração prática da solução;
- [ ] exemplos de perguntas;
- [ ] as evidências recuperadas que fundamentam as respostas;
- [ ] os principais desafios e decisões técnicas da equipe.

O vídeo deve mostrar **o raciocínio técnico** por trás da solução, não só o
funcionamento da aplicação.

## Critérios esperados

Um RAG eficiente **não** é avaliado só pela qualidade textual. A solução deve:

- [ ] recuperar conteúdos relevantes;
- [ ] construir contexto adequado para o modelo;
- [ ] gerar respostas coerentes com as evidências;
- [ ] evitar informações não fundamentadas;
- [ ] permitir a rastreabilidade dos insights;
- [ ] reconhecer quando não há informação suficiente para responder.

---

## Checklist de entrega (nosso, para nota máxima)

Mapeamento requisito → onde fica a prova no repositório. Preenchido conforme o
projeto avança.

| Requisito | Prova no repositório |
|---|---|
| Base de conhecimento justificada (6 itens) | _a definir_ |
| Pipeline RAG demonstrado (5 etapas) | _a definir_ |
| Evidências rastreáveis por avaliação | _a definir_ |
| Abstenção (3 cenários) | _a definir_ |
| Metadados (bônus) com justificativa de ganho | _a definir_ |
| Avaliação quantitativa (recuperação + fidelidade + abstenção) | _a definir_ |
| README com os 10 itens mínimos | _a definir_ |
| Vídeo até 7 min com os 8 tópicos | _a definir_ |
