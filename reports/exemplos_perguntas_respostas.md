# Exemplos de perguntas e respostas

> Gerado automaticamente por `uv run voc avaliar` a partir de
> `reports/respostas_avaliacao.json` (todas as 44 respostas estão lá, com análise da
> pergunta, filtros, evidências e tempos). Cada evidência é rastreável pelo `review_id`
> na base da Olist.

## Q01. Quais são os principais problemas relatados pelos clientes em suas avaliações?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`
  
**Consulta reescrita:** _produto com defeito atraso na entrega nao recebi produto estragado_
  
**Recuperação:** 14.445 avaliações no recorte, 61 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os principais problemas relatados pelos clientes envolvem falhas logísticas graves, destacando-se o não recebimento e o atraso na entrega dos produtos [R1][R2][R3]. Além disso, há recorrentes queixas sobre itens que chegam danificados ou com defeito [R4][R15][R20]. Os consumidores também relatam frustração com a ausência de suporte e de retorno adequado da central de atendimento [R28][R29].
>
> - **Atrasos e não recebimento**: Na base completa do recorte, o produto não recebido soma 33,0% e o atraso na entrega representa 21,2% das avaliações. Os clientes frequentemente relatam que o prazo estipulado venceu e a mercadoria não foi entregue [R1][R3][R6]. *(apoio: 23 de 30 evidências)*
> - **Produtos com defeito**: O quadro de frequências aponta que o aspecto de defeito ou avaria atinge 14,5% das avaliações do recorte. Problemas relacionados a itens estragados ou com falhas de fabricação aparecem nas avaliações dos consumidores [R4][R5][R16]. *(apoio: 7 de 30 evidências)*
> - **Atendimento ruim e suporte**: O atendimento ruim é mencionado em 19,0% das avaliações da base completa do recorte. A dificuldade de obter retorno da central de atendimento e a ausência de respostas aos e-mails enviados são reclamações pontuais dos clientes [R28][R29]. *(apoio: 4 de 30 evidências)*
>
> *Limitações: As análises numéricas refletem a base completa do recorte, ao passo que os exemplos qualitativos baseiam-se na amostra recuperada por relevância.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `9d6c1f490b2b…` | 1 | 0,98 | Atraso entrega. Não recebi o produto |
| R2 | `a04625605c0e…` | 1 | 0,98 | Até o momento não recebi o produto que está atrasado na entrega. |
| R3 | `1bfec3e91319…` | 1 | 0,94 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R4 | `a9d65ad284bb…` | 3 | 0,99 | O produto veiocom defeito. O produto veio com defeito e atraso na entrega. |
| R5 | `83c4f54bd18d…` | 1 | 0,93 | Recebi o produto com defeito |

_+25 evidências no JSON completo._

## Q04. O que os clientes relatam sobre problemas relacionados à entrega?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `tema`, polaridade `negativa`
  
**Consulta reescrita:** _produto não chegou, atraso na entrega, prazo não cumprido, demora para entregar_
  
**Recuperação:** 14.445 avaliações no recorte, 79 relevantes entre 80 candidatas, 15 no contexto

**Resposta:**

> Os clientes relatam problemas graves relacionados a atrasos e descumprimento de prazos de entrega [R1][R3][R8][R11], acompanhados de relatos frequentes de que os produtos não foram recebidos [R2][R4][R5][R9]. Essas falhas geram grande insatisfação na amostra recuperada [R15].
>
> - **Descumprimento de prazos**: Os compradores apontam falhas recorrentes no cumprimento dos prazos estabelecidos para o recebimento das compras [R1][R3][R8][R11]. As avaliações destacam que as entregas ocorrem dias após o vencimento estipulado [R4][R7][R13]. *(apoio: 7 de 15 evidências)*
> - **Ausência de recebimento**: Vários clientes relatam que, além do atraso, os itens não chegaram até o momento da avaliação [R2][R5][R9][R14]. Há registros de demora excessiva associados a pedidos cancelados [R6][R10][R15]. *(apoio: 7 de 15 evidências)*
>
> *Limitações: As informações apresentadas refletem exclusivamente a amostra recuperada de avaliações, não sendo possível extrapolar a proporção desses problemas para a base completa.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `10467dc456e8…` | 1 | 1,00 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | `a4f9f285b2ed…` | 1 | 1,00 | Não cumpriu com o prazo e o produto não chegou. |
| R3 | `48b3ce236ea9…` | 2 | 1,00 | Atraso. Produto não chegou no prazo |
| R4 | `1bfec3e91319…` | 1 | 0,97 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R5 | `9d6c1f490b2b…` | 1 | 0,98 | Atraso entrega. Não recebi o produto |

_+9 evidências no JSON completo._

## Q08. Quais aspectos da experiência de compra são mais elogiados pelos clientes?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `positiva`, filtros `{"nota_min": 4}`
  
**Consulta reescrita:** _produto excelente entrega rápida atendimento ótimo adorei_
  
**Recuperação:** 27.693 avaliações no recorte, 80 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes destacam principalmente a alta qualidade dos produtos e a agilidade nas entregas [R1][R2]. O atendimento prestado também recebe elogios expressivos nas avaliações [R5][R8]. A satisfação geral com a experiência culmina em forte recomendação do serviço [R10][R22].
>
> - **Qualidade superior dos produtos**: Na base completa do recorte, o aspecto de produto bom ou conforme anunciado representa 64,7% das menções. Os consumidores destacam com frequência que os itens recebidos possuem excelente qualidade e correspondem ao esperado [R1][R4][R7][R8]. Essa percepção positiva é amplamente reforçada pelas manifestações dos compradores [R9][R11][R13][R14]. *(apoio: 22 de 30 evidências)*
> - **Rapidez no prazo de entrega**: A entrega rápida ou no prazo atinge 45,8% das avaliações na base completa do recorte. A velocidade com que os pedidos chegam é amplamente elogiada, superando as expectativas iniciais [R3][R10][R14][R18]. Os clientes valorizam bastante o recebimento antes do prazo estipulado [R1][R2][R7][R9]. *(apoio: 25 de 30 evidências)*
> - **Qualidade no atendimento prestado**: O bom atendimento aparece em 8,2% das avaliações da base completa do recorte. O suporte ao cliente recebe menções muito positivas, sendo apontado como um diferencial na experiência de compra [R5][R8][R10][R19]. Os compradores expressam satisfação com o serviço oferecido durante todo o processo [R6][R12][R24][R28]. *(apoio: 9 de 30 evidências)*
>
> *Limitações: As conclusões combinam uma amostra de 30 avaliações recuperadas por relevância com os dados estatísticos da base completa de 27693 registros.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `c6d38a0f9663…` | 5 | 1,00 | produto de excelente qualidade entrega super rapida adorei. |
| R2 | `9eb82fb5f3e0…` | 5 | 0,99 | Adorei,produto ótimo e a entrega é super rápido |
| R3 | `5ab5ace54529…` | 5 | 1,00 | Produto excelente e entrega ótima e rápida! |
| R4 | `08b8ab4cd13b…` | 5 | 0,99 | Ótimo produto excelente qualidade entrega rápida. |
| R5 | `b71e2b3cd969…` | 5 | 0,94 | Adorei! Excelente atendimento! 👏 |

_+25 evidências no JSON completo._

## Q19. Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `evidencia`, polaridade `negativa`
  
**Consulta reescrita:** _produto não chegou, atraso na entrega, prazo não cumprido, demora na entrega_
  
**Recuperação:** 14.445 avaliações no recorte, 79 relevantes entre 80 candidatas, 15 no contexto

**Resposta:**

> As 15 avaliações recuperadas sustentam a conclusão de que existem problemas recorrentes com o prazo de entrega, evidenciados pelo descumprimento de prazos [R1][R2][R3][R4] e pelo não recebimento das mercadorias [R5][R6][R7][R8]. Os clientes relatam atrasos significativos e falta de aviso prévio por parte da empresa [R9][R10][R15].
>
> - **Atrasos recorrentes nas entregas**: Os consumidores apontam o descumprimento sistemático dos prazos estabelecidos para o envio das mercadorias [R1][R3][R4][R10]. Também há menção sobre a falta de comunicação e aviso prévio a respeito da demora [R15]. *(apoio: 10 de 15 evidências)*
> - **Produtos não entregues após o prazo**: Várias avaliações destacam que os produtos não chegaram aos destinatários mesmo após o término do prazo determinado [R2][R4][R6][R11]. Ocorrem situações de demora extrema e pedidos não entregues [R11][R13][R14]. *(apoio: 10 de 15 evidências)*
>
> *Limitações: Este relatório fundamenta a análise em uma amostra de 15 avaliações recuperadas por relevância a partir de um recorte de 14445 comentários, portanto a frequência observada vale apenas para esta amostra.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `10467dc456e8…` | 1 | 1,00 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | `a4f9f285b2ed…` | 1 | 1,00 | Não cumpriu com o prazo e o produto não chegou. |
| R3 | `48b3ce236ea9…` | 2 | 1,00 | Atraso. Produto não chegou no prazo |
| R4 | `1bfec3e91319…` | 1 | 0,98 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R5 | `9d6c1f490b2b…` | 1 | 0,99 | Atraso entrega. Não recebi o produto |

_+10 evidências no JSON completo._

## Q22. O que os clientes mais elogiam na categoria cama, mesa e banho?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `positiva`, filtros `{"nota_min": 4, "categorias": ["cama_mesa_banho"]}`
  
**Consulta reescrita:** _produto de cama mesa e banho excelente qualidade tecido bom adorei o lençol_
  
**Recuperação:** 2.741 avaliações no recorte, 64 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes elogiam majoritariamente a alta qualidade, o conforto e a estética dos produtos de cama, mesa e banho [R1][R5]. Na base completa do recorte, o aspecto de produto bom e conforme anunciado atinge cerca de 1932 avaliações, correspondendo a 70,5% do total. Adicionalmente, os compradores destacam a satisfação com a rapidez na entrega e o acabamento impecável [R2][R11].
>
> - **Qualidade superior e conforto do tecido**: Os consumidores destacam frequentemente a maciez, o conforto e o bom acabamento dos itens de cama, mesa e banho [R1][R7][R8]. Vários clientes relatam que o material é resistente e proporciona uma excelente experiência de uso [R3][R5]. *(apoio: 11 de 30 evidências)*
> - **Aparência e design que valorizam o ambiente**: O aspecto estético é muito valorizado, com relatos frequentes de que os produtos deixam os quartos mais bonitos e bem decorados [R3][R11]. Os compradores mencionam que os itens possuem excelente tamanho e ótimo caimento na cama [R6][R18][R22]. *(apoio: 9 de 30 evidências)*
> - **Alta satisfação geral e recomendação**: Na base completa do recorte, a satisfação geral e a recomendação aparecem em cerca de 1184 avaliações, o que representa 43,2% do total. Na amostra recuperada, os clientes expressam forte aprovação, afirmando que comprariam novamente e recomendando os produtos [R4][R13][R18][R27]. *(apoio: 5 de 30 evidências)*
> - **Agilidade e pontualidade na entrega**: A entrega rápida e no prazo é um ponto de forte elogio, presente em cerca de 984 avaliações da base completa, equivalente a 35,9% do recorte. Clientes da amostra relatam que receberam os pedidos com agilidade, muitas vezes antes do prazo previsto [R2][R22][R27]. *(apoio: 3 de 30 evidências)*
>
> *Limitações: As análises combinam percentuais gerais do quadro de frequências da base completa com uma amostra qualitativa restrita de 30 avaliações selecionadas por relevância.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `d29b7015c197…` | 5 | 0,88 | Produto de excelente qualidade, tecido macio e confortável. Recomendo |
| R2 | `a1a020107703…` | 5 | 0,87 | Produto muito bom adorei o tecido e entregue no prazo |
| R3 | `4dfe75c40bfc…` | 5 | 0,91 | Excelente produto, parece ser resistente e ficou lindo na cama, dá pena colocar lençol em cima. Amei! |
| R4 | `15fa2777d5ba…` | 5 | 0,64 | Jogo de cama. Excelente produto. Recomendo a todos |
| R5 | `33e9e4a3b2e1…` | 5 | 0,55 | Jogo de lençol muito lindo...macio e aconchegante...ficou linda a minha cama.. |

_+16 evidências no JSON completo._

## Q26. O que disseram os clientes que deram nota 1 em compras de 2018?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`, filtros `{"nota_min": 1, "nota_max": 1, "ano_mes_inicio": 201801, "ano_mes_fim": 201812}`
  
**Consulta reescrita:** _produto não chegou produto com defeito péssimo atendimento atraso entrega_
  
**Recuperação:** 4.864 avaliações no recorte, 74 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes que atribuíram nota 1 em 2018 relataram principalmente problemas graves com a entrega, como produtos não recebidos e atrasos expressivos [R1][R4][R7]. Além disso, houve fortes reclamações sobre o atendimento deficiente, suporte ineficiente para trocas e itens entregues com defeito ou baixa qualidade [R11][R16][R17].
>
> - **Produto não recebido**: Clientes relatam que os produtos comprados nunca chegaram, configurando o principal motivo de insatisfação na amostra analisada [R1][R2][R3][R14]. O quadro de frequências aponta que o problema de produto não recebido abrange 48,5% da base completa do recorte. *(apoio: 7 de 30 evidências)*
> - **Atendimento ruim e suporte ineficiente**: Os consumidores criticam severamente a qualidade do atendimento e a dificuldade para conseguir suporte ou realizar trocas quando necessário [R16][R17][R20]. O quadro de frequências demonstra que o atendimento ruim representa 31,1% das avaliações do recorte. *(apoio: 7 de 30 evidências)*
> - **Atrasos na entrega**: Vários compradores apontam que os pedidos demoraram dias ou até meses além do prazo estipulado para a entrega [R4][R7][R20]. De acordo com os dados gerais, o atraso na entrega afeta 26,0% das avaliações do recorte. *(apoio: 11 de 30 evidências)*
> - **Defeito e baixa qualidade nos itens**: Há relatos de mercadorias que chegaram danificadas, com defeitos de funcionamento ou com qualidade abaixo do esperado pelos consumidores [R11][R12][R13][R26]. Segundo o quadro de frequências, problemas de defeito ou avaria correspondem a 13,1% da base total do recorte. *(apoio: 5 de 30 evidências)*
>
> *Limitações: As análises baseiam-se em uma amostra recuperada por relevância de avaliações de nota 1 do ano de 2018, cujas menções refletem os aspectos mais recorrentes reportados pelos clientes.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `373cbeecea82…` | 1 | 0,99 | Não chegou meu produto. Péssimo |
| R2 | `9f642a55932d…` | 1 | 0,94 | Pessimo. Não entrega o produto |
| R3 | `95ba29208d51…` | 1 | 0,96 | Produto não entregue. Péssima empresa, não entregam os produtos. |
| R4 | `e0837ec10457…` | 1 | 0,96 | O produto não chegou está muito atrasado. Pessima essa loja |
| R5 | `9d6c1f490b2b…` | 1 | 0,97 | Atraso entrega. Não recebi o produto |

_+24 evidências no JSON completo._

## Q42. Quais problemas aparecem em pedidos com produtos de mais de um vendedor?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`, filtros `{"multi_vendedor": true}`
  
**Consulta reescrita:** _pedido com vários vendedores entrega incompleta produtos de lojas diferentes_
  
**Recuperação:** 625 avaliações no recorte, 19 relevantes entre 80 candidatas, 19 no contexto

**Resposta:**

> O quadro de frequências indica que o pedido incompleto é o problema mais recorrente, presente em 83,7% das avaliações do recorte. Os clientes frequentemente relatam que recebem apenas uma fração dos produtos adquiridos em compras com mais de um vendedor [R1][R2][R4][R7]. Consumidores também destacam a dificuldade em obter suporte ou retorno das lojas para resolver os itens faltantes [R5][R8][R15].
>
> - **Recebimento parcial dos itens do pedido**: Diversos clientes apontam que o pedido chega incompleto, com a entrega de apenas parte dos produtos comprados [R1][R7][R13][R17]. Em algumas situações, o sistema indica que a entrega foi concluída, embora ainda existam itens pendentes [R4][R18]. *(apoio: 15 de 19 evidências)*
> - **Falta de retorno e atendimento deficiente**: Consumidores relatam que tentam contato após receberem os produtos incompletos, mas não obtêm resposta ou retorno das lojas [R5][R8][R15]. Os compradores ficam aguardando posicionamento para a entrega dos itens restantes ou reembolso [R6][R15]. *(apoio: 4 de 19 evidências)*
>
> *Limitações: A análise é baseada em uma amostra de avaliações recuperadas por relevância, refletindo os principais problemas relatados sem abranger a totalidade da base.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `c84049c42940…` | 2 | 0,69 | Recebi pedido incompleto. Foi entregue somente parte do pedido, sendo que os produtos eram da mesma loja |
| R2 | `ee36eb06005e…` | 1 | 0,99 | Pedido entregue incompleto. |
| R3 | `ea367d520c1e…` | 1 | 0,61 | Nao recebi um dos produtos. o pedido veio incompleto! |
| R4 | `96b9f6a6bda6…` | 3 | 0,50 | Pedido Incompleto. Meu produto foi entregue parcialmente, falta 01 produto e consta no status que foi entregue. |
| R5 | `c7c623cd6435…` | 1 | 0,32 | entrega incompleta. Comprei dois produtos da mesma loja porem recebia apenas não recebi nenhum retorno da loja ate agora |

_+14 evidências no JSON completo._

## Q29. Qual foi o faturamento da Olist em 2018?

**Status:** abstenção: fora do escopo
  
**Análise da pergunta:** tipo `panorama`, polaridade `qualquer`
  
**Consulta reescrita:** _faturamento da Olist 2018_

**Resposta:**

> **Fora do escopo da base de conhecimento.** A pergunta pede dados financeiros e de faturamento da empresa, que não constam nas avaliações de clientes.
>
> A base contém apenas avaliações escritas por clientes da Olist entre 2016 e 2018 sobre suas compras (entrega, produto, atendimento, vendedor, embalagem, preço). Não respondo com conhecimento externo para não apresentar algo que os dados não sustentam.

## Q35. O que os clientes acharam das entregas feitas por drone?

**Status:** abstenção: evidências não sustentam resposta
  
**Análise da pergunta:** tipo `tema`, polaridade `qualquer`
  
**Consulta reescrita:** _entrega feita por drone, entrega via drone_
  
**Recuperação:** 42.138 avaliações no recorte, 24 relevantes entre 80 candidatas, 15 no contexto

**Resposta:**

> **As evidências recuperadas não sustentam uma resposta.** As evidências recuperadas não trazem informações sobre entregas feitas por drone, abordando apenas aspectos gerais de prazos e recebimentos [R1][R3][R7]. Portanto, não é possível responder ao que os clientes acharam desse método específico de entrega.

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `e10c873dd7f4…` | 5 | 0,38 | Entrega feita. Td certo com a entrega |
| R2 | `63a5d53b4f2c…` | 4 | 0,61 | Produto entregue, |
| R3 | `d71825799ddb…` | 5 | 0,90 | entregue. entrega rápida e eficiente |
| R4 | `d2482a794ec9…` | 5 | 0,66 | entrega bem rapida |
| R5 | `fe65d131efb9…` | 3 | 0,35 | entrega produto. bom |

_+10 evidências no JSON completo._

## Q37. Quais reclamações existem sobre pagamento com criptomoedas?

**Status:** abstenção: fora do escopo
  
**Análise da pergunta:** tipo `tema`, polaridade `qualquer`
  
**Consulta reescrita:** _pagamento criptomoedas bitcoin_

**Resposta:**

> **Fora do escopo da base de conhecimento.** A base de conhecimento não possui registros sobre pagamentos com criptomoedas.
>
> A base contém apenas avaliações escritas por clientes da Olist entre 2016 e 2018 sobre suas compras (entrega, produto, atendimento, vendedor, embalagem, preço). Não respondo com conhecimento externo para não apresentar algo que os dados não sustentam.
