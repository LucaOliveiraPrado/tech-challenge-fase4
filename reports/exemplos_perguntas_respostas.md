# Exemplos de perguntas e respostas

> Gerado automaticamente por `uv run voc avaliar` a partir de
> `reports/respostas_avaliacao.json` (todas as 40 respostas estão lá, com análise da
> pergunta, filtros, evidências e tempos). Cada evidência é rastreável pelo `review_id`
> na base da Olist.

## Q01. Quais são os principais problemas relatados pelos clientes em suas avaliações?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`
  
**Consulta reescrita:** _problema defeito atraso nao chegou produto estragado_
  
**Recuperação:** 14.445 avaliações no recorte, 61 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os principais problemas relatados pelos clientes envolvem falhas na entrega, como atrasos e não recebimento dos produtos [R1][R2][R3][R19], além de itens que chegam com defeitos [R5][R7][R8][R12]. Também são mencionadas falhas no atendimento e na comunicação com a loja [R18][R21].
>
> - **Atraso e não recebimento de produtos**: Os consumidores destacam expressivos atrasos no envio e casos em que os produtos não chegam ao destino [R1][R2][R3][R4]. Na base completa do recorte, o não recebimento representa 33,0% e o atraso na entrega 21,2% das avaliações. *(apoio: 20 de 30 evidências)*
> - **Produtos com defeito ou avarias**: Há recorrentes relatos de itens que chegam estragados, com defeitos de fabricação ou que param de funcionar rapidamente [R5][R7][R8][R12]. O aspecto de defeito ou avaria atinge 14,5% da base completa do recorte. *(apoio: 10 de 30 evidências)*
> - **Atendimento ruim e falta de suporte**: Clientes apontam dificuldades de contato e ausência de retorno por parte da central de atendimento ao buscar soluções [R18][R21]. Esse aspecto representa 19,0% das avaliações na base completa do recorte. *(apoio: 2 de 30 evidências)*
>
> *Limitações: Os dados da amostra recuperada refletem as avaliações selecionadas por relevância, enquanto os percentuais gerais correspondem à base completa do recorte.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `4a7118b1f9c3…` | 1 | 0,98 | meu produto nao chegou esta atrasado. |
| R2 | `48b3ce236ea9…` | 2 | 0,92 | Atraso. Produto não chegou no prazo |
| R3 | `b28bfbd00dfd…` | 1 | 0,92 | Produto não chegou está com 2 dias de atraso |
| R4 | `4d2d379325d0…` | 1 | 0,98 | Meu produto está atrasado e ainda não chegou |
| R5 | `801fb7f38a93…` | 1 | 0,90 | a entrega demorou e o produto chegou com defeito |

_+25 evidências no JSON completo._

## Q04. O que os clientes relatam sobre problemas relacionados à entrega?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`
  
**Consulta reescrita:** _produto não chegou atraso na entrega prazo não cumprido transportadora demorou_
  
**Recuperação:** 14.445 avaliações no recorte, 77 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes relatam expressivamente problemas com entregas, destacando o descumprimento de prazos combinados e produtos que não chegam ao destino [R1][R3][R5]. Na base completa do recorte, o problema de produto não recebido atinge 33,0% e o atraso na entrega representa 21,2%. Além disso, os consumidores apontam a falta de comunicação e satisfação por parte da loja sobre as ocorrências [R5][R21].
>
> - **Descumprimento de prazos e atrasos**: Os consumidores apontam que a empresa não cumpre o prazo estabelecido para envio e entrega das mercadorias [R1][R2][R4][R5]. As avaliações registram atrasos consideráveis em relação à data prevista [R11][R16][R19]. *(apoio: 17 de 30 evidências)*
> - **Ausência de recebimento e pedidos não entregues**: Outro problema recorrente é o não recebimento dos produtos adquiridos, culminando em pedidos cancelados e frustração [R3][R7][R8][R10]. Os consumidores relatam que os itens simplesmente não chegam ao destino final [R13][R14][R20]. Há também registros de transportadores que não realizaram a entrega [R23][R27][R28]. *(apoio: 10 de 30 evidências)*
> - **Falta de suporte e satisfação sobre atrasos**: Os compradores criticam a ausência de aviso prévio e de justificativas por parte da loja ou dos fornecedores quando ocorrem os atrasos [R5][R21][R24]. Há também menções negativas a problemas operacionais dos Correios [R25]. *(apoio: 4 de 30 evidências)*
>
> *Limitações: A análise é baseada em uma amostra recuperada de 30 avaliações de clientes, complementada pelos dados percentuais da base completa do recorte.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `10467dc456e8…` | 1 | 0,99 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | `48b3ce236ea9…` | 2 | 1,00 | Atraso. Produto não chegou no prazo |
| R3 | `a4f9f285b2ed…` | 1 | 1,00 | Não cumpriu com o prazo e o produto não chegou. |
| R4 | `4a7118b1f9c3…` | 1 | 0,99 | meu produto nao chegou esta atrasado. |
| R5 | `85a391b84d8e…` | 1 | 0,94 | não cumpre prazo. Não cumpriram prazo de entrega e nem avisaram o atraso. |

_+25 evidências no JSON completo._

## Q08. Quais aspectos da experiência de compra são mais elogiados pelos clientes?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `positiva`
  
**Consulta reescrita:** _entrega rapida produto bem embalado otimo atendimento adorei recomendo_
  
**Recuperação:** 27.693 avaliações no recorte, 78 relevantes entre 78 candidatas, 30 no contexto

**Resposta:**

> Os aspectos mais elogiados pelos clientes englobam a qualidade e o cuidado na embalagem dos produtos, a agilidade na entrega e a alta satisfação geral com recomendação [R4][R14][R19]. A base completa do recorte aponta que o produto bom ou conforme anunciado lidera as menções, seguido por entrega rápida e recomendação [R28].
>
> - **Qualidade e embalagem adequada dos produtos**: Os clientes destacam com frequência que os itens chegam bem embalados, seguros e em perfeito estado [R4][R10][R28][R29]. Na base completa do recorte, o aspecto de produto bom ou conforme anunciado representa 64,7% das avaliações. *(apoio: 27 de 30 evidências)*
> - **Agilidade e rapidez na entrega**: A rapidez no envio e o cumprimento dos prazos de entrega são amplamente elogiados nas avaliações [R1][R6][R14][R26]. O quadro de frequências indica que a entrega rápida ou no prazo está presente em 45,8% das avaliações do recorte. *(apoio: 29 de 30 evidências)*
> - **Satisfação geral e recomendação**: Muitos consumidores expressam forte satisfação com a compra realizada e recomendam a loja e os produtos [R3][R4][R13][R19]. O aspecto de satisfação geral e recomendação atinge 40,1% da base completa do recorte. *(apoio: 15 de 30 evidências)*
> - **Bom atendimento e preço competitivo**: Embora em menor escala na amostra, o bom atendimento e o preço bom também são mencionados como pontos positivos [R9][R21][R25]. O quadro de frequências aponta o bom atendimento em 8,2% e o bom preço em 3,5% das avaliações. *(apoio: 3 de 30 evidências)*
>
> *Limitações: As análises baseiam-se em uma amostra de 30 avaliações recuperadas por relevância, cujas tendências gerais são complementadas pelos percentuais informados no quadro de frequências da base completa.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `3ec2b04cc124…` | 5 | 0,99 | Ótimo produto, bem embalado e entrega rápida. Recomendo |
| R2 | `656fba433b3b…` | 5 | 1,00 | A entrega foi muito rápida, adorei ! O produto veio super bem embalado, recomendo. |
| R3 | `6b7a213b453a…` | 4 | 1,00 | Rapida entrega. Produto bem embalado. Recomendo. |
| R4 | `0036406b2cc6…` | 5 | 0,98 | Ótimo produto,entrega rápida e super bem embalado.Super recomendo!!! |
| R5 | `e612bef182e4…` | 4 | 1,00 | recomendo. produto chegou rápido e bem embalado. |

_+25 evidências no JSON completo._

## Q19. Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `evidencia`, polaridade `negativa`
  
**Consulta reescrita:** _produto não chegou atraso na entrega prazo não cumprido demorou muito_
  
**Recuperação:** 14.445 avaliações no recorte, 76 relevantes entre 80 candidatas, 15 no contexto

**Resposta:**

> As 15 avaliações recuperadas sustentam a conclusão de problemas recorrentes no prazo de entrega, apontando atrasos severos e não recebimento dos produtos [R1][R2][R3][R5]. Os clientes relatam descumprimento de prazos estabelecidos e falhas na comunicação por parte da loja [R5][R15].
>
> - **Descumprimento geral de prazos**: Os consumidores afirmam de forma recorrente que a loja falha em cumprir as datas estabelecidas para o recebimento das mercadorias [R2][R4][R5][R13]. *(apoio: 5 de 15 evidências)*
> - **Atrasos prolongados e falta de entrega**: Várias avaliações apontam que os produtos ultrapassam o prazo limite e demoram dias a mais para chegar ou simplesmente não são entregues [R1][R3][R6][R8]. *(apoio: 6 de 15 evidências)*
> - **Ausência de comunicação e satisfação**: Clientes criticam a falta de aviso prévio sobre os atrasos e a ausência de justificativas por parte da empresa sobre a demora [R5][R15]. *(apoio: 2 de 15 evidências)*
> - **Pedidos cancelados e não recebidos**: Há registros de produtos que continuam sem entrega até o momento da avaliação, resultando em insatisfação e pedidos cancelados [R7][R9][R11]. *(apoio: 3 de 15 evidências)*
>
> *Limitações: As constatações utilizam exclusivamente a amostra recuperada de 15 avaliações, sem permitir extrapolações para a base completa de 14445 comentários.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `a4f9f285b2ed…` | 1 | 1,00 | Não cumpriu com o prazo e o produto não chegou. |
| R2 | `10467dc456e8…` | 1 | 0,99 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R3 | `48b3ce236ea9…` | 2 | 1,00 | Atraso. Produto não chegou no prazo |
| R4 | `4a7118b1f9c3…` | 1 | 0,99 | meu produto nao chegou esta atrasado. |
| R5 | `85a391b84d8e…` | 1 | 0,87 | não cumpre prazo. Não cumpriram prazo de entrega e nem avisaram o atraso. |

_+10 evidências no JSON completo._

## Q22. O que os clientes mais elogiam na categoria cama, mesa e banho?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `positiva`, filtros `{"nota_min": 4, "categorias": ["cama_mesa_banho"]}`
  
**Consulta reescrita:** _cama mesa e banho tecido bom qualidade excelente recomendo_
  
**Recuperação:** 2.741 avaliações no recorte, 44 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes elogiam primordialmente a alta qualidade e a conformidade dos produtos na categoria de cama, mesa e banho [R1][R5][R9]. Conforme o quadro de frequências da base completa, 70,5% das avaliações apontam produtos bons ou conforme anunciado, e 35,9% destacam a entrega rápida [R10][R16][R18]. O conforto, a maciez do tecido e o preço competitivo também recebem forte reconhecimento [R4][R12].
>
> - **Alta qualidade e conformidade dos produtos**: Os consumidores destacam com frequência a excelente qualidade dos materiais, costura bem feita e total fidelidade aos anúncios [R1][R3][R9][R13]. O quadro de frequências mostra que o aspecto produto bom ou conforme anunciado representa 70,5% da base completa do recorte. *(apoio: 21 de 30 evidências)*
> - **Conforto e tamanho adequado dos itens**: A maciez do tecido e o tamanho ideal dos produtos, como jogos de cama e tapetes felpudos, são amplamente elogiados [R1][R5][R17][R23]. Os clientes enfatizam que os itens proporcionam conforto e ajuste perfeito [R12][R14][R27]. *(apoio: 9 de 30 evidências)*
> - **Preço otimizado e agilidade na entrega**: O ótimo custo-benefício e os preços atrativos aparecem elogiados juntamente com a rapidez no envio [R4][R6][R10][R16]. A base completa do recorte aponta que a entrega rápida no prazo representa 35,9% das menções [R18]. *(apoio: 6 de 30 evidências)*
>
> *Limitações: Esta análise baseia-se em uma amostra de 30 avaliações recuperadas por relevância a partir de um total de 2741 comentários no recorte, sendo os percentuais globais extraídos do quadro de frequências da base completa.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `d29b7015c197…` | 5 | 0,83 | Produto de excelente qualidade, tecido macio e confortável. Recomendo |
| R2 | `3dc34dca59e1…` | 5 | 0,98 | Excelente tecido !!!! Recomendo! |
| R3 | `15fa2777d5ba…` | 5 | 0,59 | Jogo de cama. Excelente produto. Recomendo a todos |
| R4 | `5630abc53f14…` | 5 | 0,85 | material do tecido muito. preço otimo,e material muito bom,eu recomendo |
| R5 | `aef781f1cdf6…` | 5 | 0,80 | Lindo e de qualidade. O tamanho é excelente e a cama ficou muito nobre. Recomendo. |

_+24 evidências no JSON completo._

## Q26. O que disseram os clientes que deram nota 1 em compras de 2018?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`, filtros `{"nota_min": 1, "nota_max": 1, "ano_mes_inicio": 201801, "ano_mes_fim": 201812}`
  
**Consulta reescrita:** _produto ruim defeito nao funciona nao chegou atrasado_
  
**Recuperação:** 4.864 avaliações no recorte, 64 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes que atribuíram nota 1 em 2018 relataram principalmente problemas relacionados a produtos não recebidos, itens com defeito e atrasos nas entregas [R8][R2][R7]. O quadro de frequências aponta que o produto não recebido afeta 48,5% das avaliações do recorte [R8].
>
> - **Produto não recebido**: Clientes relatam que a compra não foi entregue ou que o pedido foi cancelado [R8][R11][R15][R22]. A base completa indica que a falta de recebimento ocorre em 48,5% das 4864 avaliações do recorte. *(apoio: 13 de 30 evidências)*
> - **Produtos com defeito**: Consumidores apontam que os itens chegaram com defeito ou não funcionam corretamente [R2][R3][R4][R10]. O quadro de frequências mostra que defeito ou avaria está presente em 13,1% do recorte. *(apoio: 13 de 30 evidências)*
> - **Atrasos na entrega**: Há reclamações de que os pedidos foram entregues com vários dias de atraso em relação ao prazo [R1][R5][R6][R7]. O atraso na entrega representa 26,0% da base completa do recorte. *(apoio: 10 de 30 evidências)*
>
> *Limitações: As informações refletem uma amostra de 30 evidências complementada pelo quadro de frequências da base completa do recorte.*

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `4a7118b1f9c3…` | 1 | 0,99 | meu produto nao chegou esta atrasado. |
| R2 | `93f72220a2ee…` | 1 | 0,96 | Produto já veio com defeito não funciona |
| R3 | `a61e65fa1f26…` | 1 | 0,99 | Produto com defeito. Produto não funciona |
| R4 | `459c0d0a0258…` | 1 | 0,40 | Recebi o produto no prazo certo, mas está com defeito, não está funcionando! |
| R5 | `b28bfbd00dfd…` | 1 | 0,85 | Produto não chegou está com 2 dias de atraso |

_+25 evidências no JSON completo._

## Q29. Qual foi o faturamento da Olist em 2018?

**Status:** abstenção: fora do escopo
  
**Análise da pergunta:** tipo `panorama`, polaridade `qualquer`
  
**Consulta reescrita:** _faturamento da empresa_

**Resposta:**

> **Fora do escopo da base de conhecimento.** A pergunta pede dados financeiros e de faturamento da empresa, que não constam nas avaliações de clientes.
>
> A base contém apenas avaliações escritas por clientes da Olist entre 2016 e 2018 sobre suas compras (entrega, produto, atendimento, vendedor, embalagem, preço). Não respondo com conhecimento externo para não apresentar algo que os dados não sustentam.

## Q35. O que os clientes acharam das entregas feitas por drone?

**Status:** abstenção: evidências não sustentam resposta
  
**Análise da pergunta:** tipo `tema`, polaridade `qualquer`
  
**Consulta reescrita:** _entrega feita por drone produto chegou por drone_
  
**Recuperação:** 42.138 avaliações no recorte, 46 relevantes entre 80 candidatas, 15 no contexto

**Resposta:**

> **As evidências recuperadas não sustentam uma resposta.** As evidências recuperadas tratam apenas de entregas tradicionais de diversas categorias [R1][R2], não havendo nenhuma menção ou dado sobre entregas feitas por drone.

| id | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|
| R1 | `1ef6bce020ad…` | 1 | 0,99 | o produto foi entregue |
| R2 | `ec083db11bd4…` | 4 | 0,99 | Foi entregue o produto |
| R3 | `a19e0a3ad1dc…` | 5 | 0,99 | Produto entregue |
| R4 | `c020b491ced4…` | 5 | 0,32 | Entrega feita com sucesso. Entrega feita e o produto é o que eu queria, muito bom!! |
| R5 | `0bc44abd645a…` | 5 | 0,68 | Produto chega rapido, e conforme feito no pedido. |

_+10 evidências no JSON completo._

## Q37. Quais reclamações existem sobre pagamento com criptomoedas?

**Status:** abstenção: sem evidência relevante
  
**Análise da pergunta:** tipo `tema`, polaridade `negativa`
  
**Consulta reescrita:** _pagamento com bitcoin criptomoeda erro na transacao_
  
**Recuperação:** 14.445 avaliações no recorte, 0 relevantes entre 80 candidatas, 0 no contexto

**Resposta:**

> **Não encontrei avaliações relevantes para responder com segurança.** Analisei 80 candidatas no recorte (nota de 1 a 3; 14.445 avaliações com comentário), e nenhuma atingiu a relevância mínima (0,30). Prefiro não responder a inventar uma conclusão sem suporte nos dados.
