# Exemplos de perguntas e respostas

> Gerado automaticamente por `uv run voc avaliar` a partir de
> `reports/respostas_avaliacao.json` (todas as 44 respostas estão lá, com análise da
> pergunta, filtros, evidências e tempos). Cada evidência é rastreável pelo `review_id`
> na base da Olist; a coluna "sustenta o insight" liga cada avaliação aos insights da
> resposta que a citam. "Apoio: X de N" diz quantas das N evidências do contexto o
> modelo listou como sustentação do insight (todas validadas por código; o texto mostra
> só as mais representativas entre colchetes).

## Q01. Quais são os principais problemas relatados pelos clientes em suas avaliações?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`, filtros `{"nota_max": 2}`
  
**Consulta reescrita:** _atraso na entrega produto defeituoso nao recebi produto errado pessimo atendimento_
  
**Recuperação:** 10.845 avaliações no recorte, 76 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os principais problemas relatados abrangem a ausência de recebimento, atrasos expressivos e o envio de mercadorias incorretas [R1][R3][R8]. O problema de produto não recebido representa 42,1% das avaliações do recorte completo, enquanto o atendimento ruim atinge 25,8% e o atraso na entrega soma 24,4%. Os consumidores também destacam suporte ineficiente e defeitos nos itens recebidos [R10][R16][R17].
>
> - **Ausência de recebimento do produto**: Diversos clientes relatam que pagaram pelos itens mas nunca os receberam ou tiveram pedidos cancelados sem justificativa [R1][R5][R12][R18]. Há queixas explícitas sobre a falta de entrega e de retorno da empresa [R6][R13][R21][R22]. *(apoio: 16 de 30 evidências)*
> - **Atendimento ao cliente insatisfatório**: O suporte é classificado como péssimo pelos consumidores que apontam falta de explicações e ausência de retorno [R10][R19][R22][R29]. Os compradores também cobram satisfações sobre pagamentos já efetuados e relatam atendimento desrespeitoso [R28][R30]. *(apoio: 7 de 30 evidências)*
> - **Atrasos expressivos na entrega**: As avaliações mencionam prazos não cumpridos com demoras recorrentes após o término estipulado [R2][R4][R7][R8]. Os consumidores criticam a extrapolação do prazo e a ausência de aviso prévio [R15][R18][R25][R30]. *(apoio: 15 de 30 evidências)*
> - **Envio de produto incorreto ou defeituoso**: Clientes relatam o recebimento de mercadorias trocadas com incorreções em cores ou tamanhos [R3][R9][R11][R20]. Também são apontados itens com defeitos de fabricação e qualidade insatisfatória [R16][R17][R27][R28]. *(apoio: 8 de 30 evidências)*
>
> *Limitações: As análises baseiam-se em uma amostra recuperada por relevância cujas proporções diferem da base completa embora o quadro de frequências indique a dimensão geral dos aspectos.*
>
> *Percentuais: estimativa do classificador de aspectos sobre as 10.845 avaliações com comentário do recorte (nota de 1 a 2).*

<details><summary><b>As 30 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1, 2 | `18825455b8639598b4511791079ee332` | 1 | 0,99 | Não recebi meu produto dentro do prazo e o atendimento foi péssimo |
| R2 | 1, 3 | `9d6c1f490b2b4bfef33820b5679e2d82` | 1 | 0,99 | Atraso entrega. Não recebi o produto |
| R3 | 4 | `29f677904b91e78ddd47643653c55c3e` | 1 | 0,84 | O produto foi entregue errado. Não recebi o produto que comprei. |
| R4 | 1, 3 | `1bfec3e913196c72c1ea06fc8816bd9c` | 1 | 0,97 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R5 | 1 | `0f80e3076617983291eb9fd9c1dc3498` | 1 | 0,99 | nao recebi produto. pessimo |
| R6 | 1 | `9f642a55932d21d42cb4681ee0aff6cb` | 1 | 0,85 | Pessimo. Não entrega o produto |
| R7 | 1, 3 | `98eaf3a20ac997b34bf433ac0979f4e2` | 1 | 0,99 | Atraso na entrega, até o momento nao recebi o meu produto. |
| R8 | 1, 3 | `1f3f5e3000ed6307fbda490057bfa59b` | 2 | 0,99 | Atraso na entrega. Ainda não recebi o produto. |
| R9 | 4 | `add668839f75a741571e3af8d9c047c6` | 2 | 0,93 | Produto errado. Não recebi o produto que eu comprei |
| R10 | 2, 3 | `ea98ee7eb77ad3f059f74548a87feb3a` | 1 | 0,97 | Péssimo atendimento o produto chegou mais não demorou um pouco |
| R11 | 4 | `5cebd0cb812691be648e2be73527bfce` | 1 | 0,88 | péssimo, além da demora ainda mandaram o produto errado. |
| R12 | 1 | `95ba29208d5172ce9f9890946cd6e30a` | 1 | 0,85 | Produto não entregue. Péssima empresa, não entregam os produtos. |
| R13 | 1 | `86c917ec7c07573968fb6a568647b8e2` | 1 | 0,71 | Péssimo. Eu quero o meu produto. Eu paguei. E nao recebi. |
| R14 | 1, 3 | `93623428a858a3a0cf8679c420c4a8d3` | 1 | 0,93 | atraso na entrega. não recebi a entrega ainda. |
| R15 | 1, 3 | `170b122d01f94b40e901a7a1d22cf67a` | 1 | 0,90 | Não recebi. O produto não chegou ainda, está em atraso. |
| R16 | 4 | `e573c4329c52f7412b0799f640ef81c7` | 1 | 0,97 | produto defeituoso |
| R17 | 3, 4 | `190b01af91fb754443307e59209136d6` | 1 | 0,98 | produto insatisfatorio. demora na entrega e produto de baixa qualidade |
| R18 | 1, 3 | `b5e71e87bfbbcd2a826b9610bac99680` | 1 | 0,95 | atraso na entrega. nao recebi meu produto e nem uma posição sobre o mesmo |
| R19 | 2 | `237ec2d8031fa4fc3d6eb3c1825273ed` | 1 | 0,90 | Entrega e Atendimento. Péssimo atendimento! |
| R20 | 4 | `2f2a5e457479ae6caa49462daad14e5d` | 1 | 0,76 | Produto errado,cor e tamanho errado, péssima qualidade. |
| R21 | 1 | `0bb09618b24d6de1e9bf4fee647023ae` | 1 | 0,93 | demora e não entrega. péssimo |
| R22 | 1, 2 | `ed8017eaaea74d271affe463beb1256d` | 1 | 0,78 | Péssimo atendimento péssima entrega. Sequer tive retorno de minha compra cadê o produto porque o PGTO já foi recebido. |
| R23 | 3 | `e0837ec1045787e50e4a7be51779035b` | 1 | 0,74 | O produto não chegou está muito atrasado. Pessima essa loja |
| R24 | 3 | `10467dc456e818c60bd750271b5d183e` | 1 | 0,92 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R25 | 1, 3 | `420d5ecc5bcb6367d1c9d81ff6eb13d0` | 1 | 0,74 | Entrega super atrasada, não recebi ainda o produto e nem me deram satisfação de nada. |
| R26 | 1, 3 | `a04625605c0ed62e208637697536eff9` | 1 | 0,98 | Até o momento não recebi o produto que está atrasado na entrega. |
| R27 | 3, 4 | `801fb7f38a93205e682ef363234bd7dd` | 1 | 0,98 | a entrega demorou e o produto chegou com defeito |
| R28 | 2, 4 | `9c7e8cb49484cadce2bcc143729438af` | 1 | 0,77 | recebi o produto errado ja fiz reclamaçao e nao fui atendida pelo contrario a funcionaria ANDRESSA dava risada da minha cara por telefone PESSIMO ATENDIMENTO E COMPLETAMENTE INSATISFEITA |
| R29 | 2 | `e7bdc78c5f75abf94b8b1ef5c588352f` | 1 | 0,35 | Péssimo atendimento, não recomendo ,..... |
| R30 | 2, 3 | `4b25ec9d7825fbb69b4815c7ab4d94fa` | 1 | 0,68 | Entrega. Péssimo atendimento. Nao me deram nem explicações para este 1 MÊS de atraso. Nunca mais faço compras pela lannister. |

</details>

## Q04. O que os clientes relatam sobre problemas relacionados à entrega?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`
  
**Consulta reescrita:** _atraso na entrega produto não chegou prazo não cumprido transportadora_
  
**Recuperação:** 14.445 avaliações no recorte, 77 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes relatam problemas graves relacionados a prazos não cumpridos e falhas no recebimento das mercadorias [R2][R4][R7]. É frequente a queixa de que o produto não chega após o término do prazo estipulado [R14][R17][R24]. Além disso, há insatisfação com a ausência de justificativas ou avisos sobre a demora [R4][R17][R27].
>
> - **Descumprimento de prazos de entrega**: Os consumidores apontam que a loja falha em cumprir as datas estabelecidas, resultando em espera além do combinado [R1][R4][R12][R14]. O término do prazo ocorre sem que a encomenda seja entregue [R7][R24][R25][R29]. *(apoio: 8 de 30 evidências)*
> - **Não recebimento e cancelamento de pedidos**: Há relatos de produtos que nunca chegam ao destino ou resultam em pedidos cancelados por incapacidade de entrega [R8][R9][R11][R22]. Os clientes também mencionam falhas diretas das transportadoras ou itens não enviados [R18][R20][R28][R2]. *(apoio: 8 de 30 evidências)*
> - **Ausência de comunicação sobre os atrasos**: Os compradores criticam a falta de aviso prévio e de satisfação por parte dos fornecedores e lojas quando ocorrem os atrasos [R4][R17][R27]. *(apoio: 3 de 30 evidências)*
>
> *Limitações: O quadro de frequências aponta que o produto não recebido atinge 33,0% das avaliações e o atraso na entrega representa 21,2%, mas os insights qualitativos refletem apenas a amostra recuperada de 30 avaliações.*
>
> *Percentuais: estimativa do classificador de aspectos sobre as 14.445 avaliações com comentário do recorte (nota de 1 a 3).*

<details><summary><b>As 18 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `10467dc456e818c60bd750271b5d183e` | 1 | 1,00 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | 2 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | 1,00 | Não cumpriu com o prazo e o produto não chegou. |
| R4 | 1, 3 | `85a391b84d8e864de7190a2afb6f82e4` | 1 | 0,94 | não cumpre prazo. Não cumpriram prazo de entrega e nem avisaram o atraso. |
| R7 | 1 | `1bfec3e913196c72c1ea06fc8816bd9c` | 1 | 0,93 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R8 | 2 | `9d6c1f490b2b4bfef33820b5679e2d82` | 1 | 0,95 | Atraso entrega. Não recebi o produto |
| R9 | 2 | `0b89db97b78e8a32cf537f263f4aeb65` | 1 | 0,97 | Não cumpre o prazo de entrega,até agora não recebi o meu produto. |
| R11 | 2 | `986820c39b1a0f1c99bf0592080078bd` | 1 | 0,97 | Não cumpriram o prazo de entrega,ainda não recebi o produto |
| R12 | 1 | `f2a8882c104b38310adaf0a9a521b42f` | 1 | 0,98 | Produto atrasado, loja não cumpre o q promete. |
| R14 | 1 | `6bb17113a061e2e8bb65b706278b4d75` | 2 | 1,00 | Prazo de entrega não foi cumprido. Encomenda ainda não chegou. |
| R17 | 3 | `98c303ce6a5deb174c7a4b76c882d940` | 1 | 0,93 | Produto comprado e não entregue no prazo. O fornecedor não deu satisfação a respeito do atraso. |
| R18 | 2 | `312b3a6eded3cb2a7f04b73a8fbf169f` | 1 | 0,99 | O produto não foi entregado no prazo determinado. |
| R20 | 2 | `2f788d5b81dedfdb75dbe5345a3a9cf0` | 1 | 0,96 | Transportador não entregou o produto |
| R22 | 2 | `71fd2bd9edec8a1cd368a5fa173979d6` | 1 | 0,93 | Não cumpriu o prazo.. Não teve capacidade para entregar o meu produto... |
| R24 | 1 | `37e346997374feaa28ba066c1be68571` | 2 | 0,97 | já passou o prazo de entrega e o produto não chegou. |
| R25 | 1 | `0162340d190549d567ee0fdfb8fb725b` | 1 | 0,90 | Atraso na entrega. Ainda não recebi o produto é já se passou o prazo solicitado. |
| R27 | 3 | `14ab06af2677555bfcf9ff2e64a1b203` | 1 | 0,93 | O produto não foi entregu. Sem satisfação sobre atraso na entrega |
| R28 | 2 | `6cc69853b87354bdb75c227a85cde581` | 1 | 0,67 | Não entregaram o produto. Loja péssima, não cumpre com seus prazos! |
| R29 | 1 | `8b592f04ffb1115da4b08205a4f0f3b1` | 1 | 0,96 | prazo longo de entrega e não chegou no prazo |

</details>

## Q08. Quais aspectos da experiência de compra são mais elogiados pelos clientes?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `positiva`, filtros `{"nota_min": 4}`
  
**Consulta reescrita:** _entrega rápida, produto excelente, ótimo atendimento, recomendo_
  
**Recuperação:** 27.693 avaliações no recorte, 80 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes elogiam principalmente a qualidade dos produtos recebidos e a agilidade na entrega [R2][R7][R12]. Além disso, a satisfação geral com a recomendação da loja e o bom atendimento prestado destacam-se nas avaliações positivas [R1][R5][R8].
>
> - **Produto de boa qualidade**: O aspecto de produto bom ou conforme anunciado aparece em 64,7% das avaliações do recorte completo. Nas evidências, os clientes destacam com frequência a excelência e a qualidade superior dos itens adquiridos [R3][R7][R12][R17]. *(apoio: 18 de 30 evidências)*
> - **Entrega rápida e no prazo**: A agilidade na entrega é mencionada em 45,8% das avaliações da base completa do recorte. Os clientes reforçam que o recebimento ocorreu de forma rápida e antes do esperado [R10][R19][R24]. *(apoio: 24 de 30 evidências)*
> - **Satisfação geral e recomendação**: O aspecto de satisfação geral e recomendação da loja abrange 40,1% das avaliações do recorte completo. Os consumidores expressam forte recomendação dos produtos e serviços da empresa [R4][R6][R12]. *(apoio: 16 de 30 evidências)*
> - **Bom atendimento**: O atendimento prestado é citado em 8,2% das avaliações da base completa. Na amostra, os clientes elogiam explicitamente a qualidade do suporte recebido [R1][R8][R27]. *(apoio: 13 de 30 evidências)*
>
> *Limitações: As porcentagens baseiam-se na base completa do recorte, enquanto os trechos detalhados refletem uma amostra recuperada por relevância.*
>
> *Percentuais: estimativa do classificador de aspectos sobre as 27.693 avaliações com comentário do recorte (nota de 4 a 5).*

<details><summary><b>As 30 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 2, 4 | `76ebfe3c6a80a7924183178435de1399` | 5 | 1,00 | ótimo atendimento, entrega rápida. |
| R2 | 1, 2, 3 | `3c571246af9f29615cec3b55ea5188e0` | 5 | 1,00 | Entrega rápida e produto excelente, recomendo. |
| R3 | 1, 2 | `90cfae6fc1efa4e0d4d4483f81ad75b1` | 4 | 1,00 | Ótimo. Produto excelente, entrega rápida |
| R4 | 1, 2, 3 | `685fdc1417570bd85b9579e215c03944` | 5 | 1,00 | entrega rápida, ótimo produto, recomendo. |
| R5 | 1, 3, 4 | `02bc7560638893ea3d61a3f775ce7c5d` | 5 | 1,00 | RECOMENDO. ótimo produto, ótimo atendimento, entrega.. |
| R6 | 1, 2, 3 | `8aa5905667b126c8cd113a1ab88ecf74` | 5 | 1,00 | super recomendo. excelente produto, entrega rápida. recomendo. |
| R7 | 1, 2 | `6f96de0b0526fd16fcdc0e372aef7402` | 5 | 1,00 | Excelente. Produto de ótima qualidade, entrega rápida. |
| R8 | 4 | `de3e95570326b73ee34a82d800b01f6f` | 5 | 1,00 | Excelente recomendo. otimo atendimento |
| R9 | 2, 4 | `5962f753a7cdb529f3793b9c47c6c563` | 5 | 1,00 | Excelente atendimento e entrega rápida!!! |
| R10 | 2, 4 | `0dc18463d185b23148ec7ceb0ac70b64` | 5 | 0,97 | Prazo de entrega excelente.Foi mais rápido do que eu esperava. Estão de parabéns pelo ótimo atendimento. |
| R11 | 1, 2, 3 | `7046fbb96a01a1a4352ed2dac74f52cf` | 5 | 1,00 | Produto ótimo, entrega rapida, super recomendo |
| R12 | 1, 2, 3 | `01e020b5ae19cd99749bc9313cc3418f` | 5 | 1,00 | Entrega super rápida, produto de ótima qualidade, recomendo com certeza |
| R13 | 4 | `2987a2dcd950d0a74f3db048033291b7` | 4 | 0,99 | Excelente. Ótimo atendimento |
| R14 | 1, 2, 3 | `a26ba95a5def3814a0389cbd23e2fb5a` | 5 | 0,98 | Super recomendo, entrega rápida. Produto ótimo. |
| R15 | 1, 2 | `6953c13980fc183745ea3fc0595c0d4e` | 5 | 1,00 | ótimo produto, entrega rápida. |
| R16 | 1, 2 | `5ab5ace545295c27446efb6d17f6fae3` | 5 | 1,00 | Produto excelente e entrega ótima e rápida! |
| R17 | 1, 2 | `1c73fb8f9b4cbeafe2507c515bd73f4a` | 5 | 1,00 | Excelente. Entrega rápida, produto de qualidade. |
| R18 | 1, 2, 3 | `fb1ced216a53e930aac853a87d082c63` | 5 | 1,00 | ótimo produto. rápida entrega. Super recomendo. |
| R19 | 2, 3 | `7d9da71ec31738461497b83d74eb75aa` | 4 | 1,00 | ótima compra, entrega rápida. recomendo |
| R20 | 2, 4 | `8179eb34f345e70f71a4a3e7191f7ef9` | 5 | 0,99 | Ótimo atendimento. Muito bom o atendimento a entrega foi rápida e o produto foi entregue. |
| R21 | 1, 3, 4 | `086ef5f2c69d15f84c37dafee78a2b53` | 5 | 0,86 | Recomendo. Excelente atendimento e o douro de ótima qualidade |
| R22 | 1, 2, 3 | `31bdc52857f8f7dcfd20484ee64c6e97` | 5 | 1,00 | entrega rápida e produto de boa qualidade, recomendo |
| R23 | 2, 3, 4 | `fcaed0146af21af35019018c3e68d971` | 5 | 0,98 | Excelente loja. ótimo atendimento, prazo de entrega perfeito. Recomendo |
| R24 | 2, 3, 4 | `04a1616211be3a7ef23c70c64b2e6528` | 5 | 1,00 | Atendimento excelente e o produto chegou super rápido. Eu recomendo a loja. |
| R25 | 1, 2 | `80bb77cfa8bf9e0bc28d00ac6cee7485` | 5 | 1,00 | Excelente produto, rápida entrega. Obrigada |
| R26 | 1, 2 | `6ba1b5655cae1d0f1ee4850cd75eb228` | 5 | 0,99 | ótimo produto, entrega rápida,muito satisfeito |
| R27 | 4 | `0dc0fa5941a93260a51e03b73f743bd3` | 5 | 0,99 | Excelente Atendimento e extremamente rápido. |
| R28 | 2, 3, 4 | `fd896ad2cffd5956a819fcbb3f7d7044` | 5 | 1,00 | Super Recomendado. entrega rápida, e atendimento excelente |
| R29 | 1, 2, 3 | `e9de07dc30df1f38c40f934cfc6c36ba` | 5 | 0,99 | Ótima entrega e produto p. O produto e excelente e a entrega foi super rápida! Super recomendo! |
| R30 | 3, 4 | `f0234138a63f1298d79d517aee8537a3` | 5 | 0,66 | Mochila ótima. Sempre recomendo a lannister pois o atendimento é excelente! |

</details>

## Q19. Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `evidencia`, polaridade `negativa`
  
**Consulta reescrita:** _atraso na entrega produto não chegou prazo não cumprido demorou muito_
  
**Recuperação:** 14.445 avaliações no recorte, 77 relevantes entre 80 candidatas, 15 no contexto

**Resposta:**

> O problema de prazo de entrega é corroborado pelo quadro de frequências, que aponta atraso na entrega em 21,2% e produto não recebido em 33,0% das 14445 avaliações do recorte. Todas as 15 avaliações recuperadas sustentam essa conclusão, evidenciando falhas no cumprimento de datas prometidas [R1][R5][R10][R15]. Os clientes relatam insatisfação com a demora e com a falta de entrega dos itens [R2][R6][R11].
>
> - **Descumprimento de prazos de entrega**: Os clientes relatam recorrentemente que a loja não cumpre os prazos estabelecidos para a entrega das mercadorias [R1][R2][R5][R6]. Há queixas explícitas sobre o não cumprimento das datas prometidas no momento da compra [R3][R8][R10][R13]. *(apoio: 8 de 15 evidências)*
> - **Atrasos prolongados e produtos não entregues**: Várias avaliações apontam que os produtos estão atrasados e não chegaram aos endereços dos consumidores [R4][R7][R9][R11]. Também são relatados prazos longos e a ausência de recebimento definitivo dos itens [R12][R14]. *(apoio: 6 de 15 evidências)*
> - **Falta de comunicação sobre o atraso**: Os consumidores destacam a ausência de aviso prévio sobre os problemas de atraso na entrega [R13]. Além disso, é apontada a falta de satisfação ou justificativas por parte da empresa quanto à demora [R15]. *(apoio: 2 de 15 evidências)*
>
> *Limitações: O quadro de frequências indica a proporção na base completa de 14445 avaliações do recorte, enquanto as 15 evidências representam apenas uma amostra recuperada por relevância.*
>
> *Percentuais: estimativa do classificador de aspectos sobre as 14.445 avaliações com comentário do recorte (nota de 1 a 3).*

<details><summary><b>As 15 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `10467dc456e818c60bd750271b5d183e` | 1 | 1,00 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | 1 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | 1,00 | Não cumpriu com o prazo e o produto não chegou. |
| R3 | 1 | `48b3ce236ea9d35a4850ea94ca9ca38f` | 2 | 1,00 | Atraso. Produto não chegou no prazo |
| R4 | 2 | `4a7118b1f9c3d06869e0cd9d5c1b4ccb` | 1 | 0,97 | meu produto nao chegou esta atrasado. |
| R5 | 1 | `f2a8882c104b38310adaf0a9a521b42f` | 1 | 0,98 | Produto atrasado, loja não cumpre o q promete. |
| R6 | 1 | `7a37e297352c8a7b1652f721c861dcd6` | 1 | 0,98 | Não cumpriu o prazo de entrega. |
| R7 | 2 | `1bfec3e913196c72c1ea06fc8816bd9c` | 1 | 0,94 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R8 | 1 | `6bb17113a061e2e8bb65b706278b4d75` | 2 | 0,99 | Prazo de entrega não foi cumprido. Encomenda ainda não chegou. |
| R9 | 2 | `b28bfbd00dfd0c6d80e9cb524e0f205e` | 1 | 0,99 | Produto não chegou está com 2 dias de atraso |
| R10 | 1 | `986820c39b1a0f1c99bf0592080078bd` | 1 | 0,96 | Não cumpriram o prazo de entrega,ainda não recebi o produto |
| R11 | 2 | `4d2d379325d0b5d7e92ea25ac8d289c4` | 1 | 0,99 | Meu produto está atrasado e ainda não chegou |
| R12 | 2 | `170b122d01f94b40e901a7a1d22cf67a` | 1 | 0,94 | Não recebi. O produto não chegou ainda, está em atraso. |
| R13 | 1, 3 | `85a391b84d8e864de7190a2afb6f82e4` | 1 | 0,86 | não cumpre prazo. Não cumpriram prazo de entrega e nem avisaram o atraso. |
| R14 | 2 | `8b592f04ffb1115da4b08205a4f0f3b1` | 1 | 0,98 | prazo longo de entrega e não chegou no prazo |
| R15 | 3 | `c3039a71818e8c4ebe2f1a905ab1f863` | 1 | 0,92 | Demora muito e eles não dão satisfação pelo motivo do atraso |

</details>

## Q22. O que os clientes mais elogiam na categoria cama, mesa e banho?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `positiva`, filtros `{"nota_min": 4, "nota_max": 5, "categorias": ["cama_mesa_banho"]}`
  
**Consulta reescrita:** _produto excelente, qualidade ótima, tecido bom, bonito, adorei_
  
**Recuperação:** 2.741 avaliações no recorte, 76 relevantes entre 77 candidatas, 30 no contexto

**Resposta:**

> O principal elogio na base completa do recorte refere-se a produtos bons e conforme anunciado, totalizando 70,5% das menções. Os clientes destacam frequentemente a excelente qualidade, a maciez dos tecidos e o acabamento caprichado [R1][R4][R16][R20]. A satisfação geral com as compras e a rapidez na entrega também recebem forte destaque positivo [R6][R13][R25].
>
> - **Qualidade e maciez do material**: Os compradores enfatizam a ótima qualidade, a maciez e o acabamento bem feito dos produtos recebidos [R1][R4][R16][R20]. O aspecto visual e a beleza dos itens geram elogios adicionais dos consumidores [R5][R15][R17][R19]. *(apoio: 8 de 30 evidências)*
> - **Satisfação geral com a compra**: Clientes expressam forte contentamento e indicam que adoraram os artigos adquiridos e recomendam a marca [R1][R8][R10][R14]. O aspecto de satisfação geral e recomendação representa 43,2% das menções na base completa do recorte. *(apoio: 4 de 30 evidências)*
> - **Agilidade na entrega**: A pontualidade e a rapidez no envio são pontos altamente valorizados por quem recebeu os pedidos a tempo [R6][R13][R25]. A categoria de entrega rápida ou no prazo soma 35,9% no quadro de frequências da base completa. *(apoio: 3 de 30 evidências)*
> - **Preço e custo beneficio**: Alguns consumidores pontuam o preço ótimo e a vantagem financeira na aquisição dos produtos [R7][R12]. O aspecto de bom preço e custo beneficio atinge 3,9% das avaliações da base completa. *(apoio: 2 de 30 evidências)*
>
> *Limitações: Esta resposta baseia-se em uma amostra de 30 avaliações recuperadas por relevância, cujos detalhes qualitativos aplicam-se a esse grupo, enquanto os percentuais refletem a base completa do recorte.*
>
> *Percentuais: estimativa do classificador de aspectos sobre as 2.741 avaliações com comentário do recorte (nota de 4 a 5; categoria cama_mesa_banho).*

<details><summary><b>As 16 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1, 2 | `d29b7015c1970a48ebd84998398336fb` | 5 | 0,98 | Produto de excelente qualidade, tecido macio e confortável. Recomendo |
| R4 | 1 | `f559465cc5ef632af3bfc8ef12501b9d` | 4 | 0,99 | Ótimo produto e tem uma boa qualidade, tecido e costura muito bem feita. |
| R5 | 1 | `e756e7d72459f513ac8cbf720f1e56cb` | 4 | 0,99 | Produto ótimo, de qualidade e muito bonito. Recomendadíssimo!!! |
| R6 | 3 | `a1a020107703479332a3174ccbf3c039` | 5 | 0,99 | Produto muito bom adorei o tecido e entregue no prazo |
| R7 | 4 | `871b65a180fc735459a52e7cb61bcceb` | 5 | 0,97 | Ótima. Ótimo produto, excelente qualidade e excelente preço |
| R8 | 2 | `3dc34dca59e105526f4529f762ce596d` | 5 | 0,99 | Excelente tecido !!!! Recomendo! |
| R10 | 2 | `7c61cf4990b780ec18f2fcf6ab4c6ff5` | 5 | 0,99 | Adorei o produto...ótima qualidade!! Recomendo. |
| R12 | 4 | `5630abc53f149bdca0caecf5add198b0` | 5 | 0,90 | material do tecido muito. preço otimo,e material muito bom,eu recomendo |
| R13 | 3 | `c72821d9db19d3ef91d532fe35cd9896` | 5 | 0,90 | produto foi entregue no prazo, qualidade otima do tecido |
| R14 | 2 | `188d1e63b81f41613f57b12a9cabf784` | 4 | 1,00 | Gostei do produto, de boa qualidade, bonito, recomendo. |
| R15 | 1 | `9d00d05ef1d1d8537c1cd5fb5e55a7c4` | 5 | 0,99 | Um produto bonito e qualidade muito boa. |
| R16 | 1 | `2618402149d7aa92058600bf12258cbf` | 5 | 1,00 | Produto excelente. Produto de exelente qualidade,ótimo acabamento e muito bonito. Fiquei muito satisfeita. |
| R17 | 1 | `2c9e8b76b29a327017a7d060a2324af3` | 5 | 1,00 | Produto de boa qualidade. Produto lindo e muito bom, ótima qualidade |
| R19 | 1 | `9e3bb4adc687592ec040b546c477d37a` | 5 | 0,98 | Muito bonito , de qualidade. |
| R20 | 1 | `77a65ebc9f9a9ca607f9e4871bf3e75e` | 5 | 0,94 | Chegou igual estava descrito, ótima qualidade, bem bonito e excelente acabamento, recomendo. |
| R25 | 3 | `0dfc8a64244f7f559f792e2e326434b6` | 5 | 0,90 | produto lindo,bem grande e otimo tecido entrega muito rapida estou muito satisfeita |

</details>

## Q26. O que disseram os clientes que deram nota 1 em compras de 2018?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `panorama`, polaridade `negativa`, filtros `{"nota_min": 1, "nota_max": 1, "ano_mes_inicio": 201801, "ano_mes_fim": 201812}`
  
**Consulta reescrita:** _produto não chegou, atraso na entrega, produto com defeito, péssimo atendimento_
  
**Recuperação:** 4.864 avaliações no recorte, 77 relevantes entre 80 candidatas, 30 no contexto

**Resposta:**

> Os clientes que atribuíram nota 1 em 2018 relataram principalmente problemas graves relacionados à ausência de entrega dos produtos [R1][R2][R3] e atrasos expressivos nos prazos estabelecidos [R4][R5][R8]. Além disso, foram apontadas falhas no atendimento ao cliente e suporte ineficiente para trocas [R18][R19][R28], bem como o recebimento de itens com defeito ou incompletos [R12][R13][R15].
>
> - **Não recebimento de produtos**: Muitos consumidores relataram que os itens comprados nunca chegaram ou tiveram os pedidos cancelados sem o devido suporte [R1][R2][R3][R11]. Há também registros de pagamentos efetuados sem a respectiva entrega ou retorno da loja [R20][R27]. *(apoio: 8 de 30 evidências)*
> - **Atrasos na entrega**: Clientes frequentemente reclamaram do descumprimento de prazos, com demoras que variam de poucos dias a semanas em relação à data prevista [R4][R5][R6][R7]. Algumas entregas acumularam atrasos prolongados que geraram forte insatisfação nos compradores [R18][R23]. *(apoio: 13 de 30 evidências)*
> - **Atendimento e suporte inadequados**: O suporte ao cliente foi duramente criticado por ser considerado péssimo e ineficiente, especialmente na resolução de problemas e tentativas de troca [R18][R19][R28]. Clientes mencionam que o atendimento eletrônico não resolve as demandas e que faltam explicações da empresa [R23][R30]. *(apoio: 7 de 30 evidências)*
> - **Defeitos e itens faltantes**: Algumas avaliações apontam que os produtos chegaram com defeitos de funcionamento, mal embalados ou com peças faltando [R12][R13][R15][R29]. Os consumidores expressaram insatisfação com a baixa qualidade dos itens recebidos [R14][R30]. *(apoio: 6 de 30 evidências)*
>
> *Limitações: Na base completa do recorte, o problema de produto não recebido representou 48,5% das avaliações e o atendimento ruim 31,1%. Esta análise detalhada baseia-se em uma amostra recuperada de 30 comentários e serve como ilustração dos principais pontos relatados.*
>
> *Percentuais: estimativa do classificador de aspectos sobre as 4.864 avaliações com comentário do recorte (nota 1; compras de 01/2018 a 12/2018).*

<details><summary><b>As 29 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `373cbeecea8286a2b66c97b1b157ec46` | 1 | 1,00 | Não chegou meu produto. Péssimo |
| R2 | 1 | `9f642a55932d21d42cb4681ee0aff6cb` | 1 | 0,84 | Pessimo. Não entrega o produto |
| R3 | 1 | `95ba29208d5172ce9f9890946cd6e30a` | 1 | 0,97 | Produto não entregue. Péssima empresa, não entregam os produtos. |
| R4 | 2 | `e0837ec1045787e50e4a7be51779035b` | 1 | 0,99 | O produto não chegou está muito atrasado. Pessima essa loja |
| R5 | 2 | `9d6c1f490b2b4bfef33820b5679e2d82` | 1 | 0,96 | Atraso entrega. Não recebi o produto |
| R6 | 2 | `2389923a5e31e36c1184402742965903` | 1 | 0,98 | entrega atrasada,produto ainda não veio |
| R7 | 2 | `b28bfbd00dfd0c6d80e9cb524e0f205e` | 1 | 0,98 | Produto não chegou está com 2 dias de atraso |
| R8 | 2 | `6cc69853b87354bdb75c227a85cde581` | 1 | 0,87 | Não entregaram o produto. Loja péssima, não cumpre com seus prazos! |
| R9 | 2 | `170b122d01f94b40e901a7a1d22cf67a` | 1 | 0,98 | Não recebi. O produto não chegou ainda, está em atraso. |
| R10 | 2 | `4a7118b1f9c3d06869e0cd9d5c1b4ccb` | 1 | 0,99 | meu produto nao chegou esta atrasado. |
| R11 | 1 | `6beadf98a21eed6fe9e4da342ed94227` | 1 | 0,76 | Meu produto nunca chegou. Péssimo. Revoltada. |
| R12 | 4 | `e9f0bde9a98ff79305964e9033ed8cd2` | 1 | 0,90 | O produto chegou faltando e em péssimas condições. |
| R13 | 4 | `d4469da4ea0680551bd2f446a5e45a28` | 1 | 0,99 | pessimo. produto com defeito. |
| R14 | 2, 4 | `190b01af91fb754443307e59209136d6` | 1 | 0,99 | produto insatisfatorio. demora na entrega e produto de baixa qualidade |
| R15 | 4 | `6298846cdf0eceb7ba5661c3810725b7` | 1 | 0,95 | Atrasado e com defeito. Produto chegou atrasado, mal embalado e faltando um Ilhós. |
| R17 | 2 | `10467dc456e818c60bd750271b5d183e` | 1 | 0,95 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R18 | 2, 3 | `237ec2d8031fa4fc3d6eb3c1825273ed` | 1 | 0,99 | Entrega e Atendimento. Péssimo atendimento! |
| R19 | 3 | `2e1d71fce98b42bf6cbdd5e06798c286` | 1 | 0,51 | Zero. O produto chegou com defeito é o site da lannister é péssimo pra trocas, suporte péssimo !!!! |
| R20 | 1 | `0bb09618b24d6de1e9bf4fee647023ae` | 1 | 0,97 | demora e não entrega. péssimo |
| R21 | 3 | `e7bdc78c5f75abf94b8b1ef5c588352f` | 1 | 0,73 | Péssimo atendimento, não recomendo ,..... |
| R22 | 1 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | 0,95 | Não cumpriu com o prazo e o produto não chegou. |
| R23 | 2, 3 | `4b25ec9d7825fbb69b4815c7ab4d94fa` | 1 | 0,68 | Entrega. Péssimo atendimento. Nao me deram nem explicações para este 1 MÊS de atraso. Nunca mais faço compras pela lannister. |
| R24 | 2 | `f2a8882c104b38310adaf0a9a521b42f` | 1 | 0,98 | Produto atrasado, loja não cumpre o q promete. |
| R25 | 2 | `4d2d379325d0b5d7e92ea25ac8d289c4` | 1 | 0,98 | Meu produto está atrasado e ainda não chegou |
| R26 | 1 | `51beaf6a397e57bb1880f4f49cb0535f` | 1 | 0,96 | produto não entregue |
| R27 | 1, 3 | `ed8017eaaea74d271affe463beb1256d` | 1 | 0,89 | Péssimo atendimento péssima entrega. Sequer tive retorno de minha compra cadê o produto porque o PGTO já foi recebido. |
| R28 | 3 | `07df55457e11d32f632ba70fb0257406` | 1 | 0,53 | Zero. Atendimento péssimo |
| R29 | 4 | `9eb2e56b505c2cec094833032f94d3e1` | 1 | 0,75 | Não funciona, mais uma vez meu produto chegou com defeito! |
| R30 | 3, 4 | `ced0560b692ae389904d584f03f4d8bf` | 1 | 0,75 | produto com defeito. estou desde o dia 22 tentando resolver o problema do produto ter vindo com defeito, mas só me atendem no atendimento eletrônico. |

</details>

## Q42. Quais problemas aparecem em pedidos com produtos de mais de um vendedor?

**Status:** respondida com evidências
  
**Análise da pergunta:** tipo `tema`, polaridade `negativa`, filtros `{"multi_vendedor": true}`
  
**Consulta reescrita:** _produtos diferentes, entrega separada, faltou um produto, lojas diferentes, problema com os vendedores_
  
**Recuperação:** 625 avaliações no recorte, 53 relevantes entre 80 candidatas, 15 no contexto

**Resposta:**

> Nos pedidos com mais de um vendedor, o principal problema relatado é o recebimento incompleto de itens [R1][R3][R6][R10]. Há também registros de entregas fracionadas [R2], divergências no status do pedido [R8][R12] e falta de resposta no pós-venda [R12].
>
> - **Recebimento incompleto de produtos**: O problema mais recorrente é a ausência de um ou mais itens no momento do recebimento, fazendo com que o cliente receba apenas parte do que comprou [R1][R3][R7][R10]. *(apoio: 15 de 15 evidências)*
> - **Divergência de status e falha no suporte**: O sistema indica que a entrega foi totalmente concluída quando na verdade faltam produtos, além da demora ou ausência de resposta ao abrir reclamações [R8][R12]. *(apoio: 2 de 15 evidências)*
> - **Entregas fracionadas**: Os clientes destacam que um único pedido é enviado em entregas separadas pelos diferentes vendedores, gerando confusão no recebimento [R2]. *(apoio: 1 de 15 evidências)*
>
> *Limitações: Como não há quadro de frequências, as noções de frequência valem apenas para a amostra recuperada de 15 avaliações, dentro de um recorte total de 625 comentários.*

<details><summary><b>As 15 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `3e5855205340c723730123053cc1171f` | 1 | 0,77 | Faltou 2 produtos na entrega, tive de ligar na loja para reclamar. |
| R2 | 1, 3 | `55ffbc6435b1f6ce484421370d364401` | 2 | 0,78 | Fiz um pedido só, e veio separado.as.entregas faltando um produto (best whey) |
| R3 | 1 | `ff73170d8a9deb95aa4814ddbec217b4` | 2 | 0,97 | entregou faltando um produto |
| R4 | 1 | `bcf1f7d1fdf796f91d59cdfab8798d7a` | 1 | 0,81 | Produto entregue faltando encomendas |
| R5 | 1 | `4589b661245306b0f4ce2ee972bbf1ab` | 1 | 0,84 | Tive problemas com a entrega. E ainda não mandaram todos os produtos! |
| R6 | 1 | `7d6ba969ba93e86ed87d563c1821616b` | 1 | 0,72 | Entrega faltando produtos. Fiz pedido de 6 produtos e só recebi 2. |
| R7 | 1 | `e70c3511b7dcbe1966bec2a3b9f959d7` | 1 | 0,96 | O pedido veio somente um produto e faltando outro. |
| R8 | 1, 2 | `42a3a3e2b79465364e24f6f4c642bc23` | 1 | 0,57 | Em partes. Sou cliente há anos, porém sempre há divergências e problemas na entrega, consta como produto entregue, porém foi entregue apenas 1 produto, aguardo solução! |
| R9 | 1 | `06ed69462b99956d9e41146accb7f291` | 2 | 0,98 | Falta entregar um dos produtos |
| R10 | 1 | `fdfca8fa7eeb3f2451289557e4aa7efb` | 1 | 0,96 | Olá!! recebi só parcialmente os produtos; faltou um item. |
| R11 | 1 | `7d81592881b86d6ba09e4e5ae954a59d` | 1 | 0,80 | Chegou o produto atrasado, faltando outro. Falta chegar os demais. O cliente está zangado. |
| R12 | 1, 2 | `707879ba994360a7805bdda512738e6d` | 1 | 0,76 | Entrega faltando. Comprei dois produtos na loja só veio um. É no site está dizendo que foi entregue os dois. Fiz a reclamação a 4 dias e ainda não tive resposta. |
| R13 | 1 | `a7aa38eca8d2ea1641852cfa1b09ad42` | 1 | 0,67 | targaryen não entregou os produtos completos. No dois itens comprados veio faltando unidades. |
| R14 | 1 | `7359e94ddcdbe22c2f749d794c96c683` | 3 | 0,80 | Falta 1 produto. Foi entregue somente um dos produtos. O arranhador de canto está faltando entregar ainda. |
| R15 | 1 | `051922be8fec8220564a359b3b11f3b7` | 1 | 0,70 | Não recebi todos os produ. Falta duas unidades do outro produto que comprei. |

</details>

## Q29. Qual foi o faturamento da Olist em 2018?

**Status:** abstenção: fora do escopo
  
**Análise da pergunta:** tipo `panorama`, polaridade `qualquer`
  
**Consulta reescrita:** __

**Resposta:**

> **Fora do escopo da base de conhecimento.**
>
> A base contém apenas avaliações escritas por clientes da Olist entre 2016 e 2018 sobre suas compras (entrega, produto, atendimento, vendedor, embalagem, preço). Não respondo com conhecimento externo para não apresentar algo que os dados não sustentam.

## Q35. O que os clientes acharam das entregas feitas por drone?

**Status:** abstenção: evidências não sustentam resposta
  
**Análise da pergunta:** tipo `tema`, polaridade `qualquer`
  
**Consulta reescrita:** _entrega por drone, chegou por drone, encomenda de drone_
  
**Recuperação:** 42.138 avaliações no recorte, 20 relevantes entre 80 candidatas, 15 no contexto

**Resposta:**

> **As evidências recuperadas não sustentam uma resposta.** As evidências recuperadas tratam apenas de prazos e rapidez geral de entrega, sem conter informações sobre entregas feitas por drone [R1][R3][R6][R9]. Portanto, os dados disponíveis não permitem responder à pergunta do gestor.

## Q37. Quais reclamações existem sobre pagamento com criptomoedas?

**Status:** abstenção: evidência insuficiente
  
**Análise da pergunta:** tipo `tema`, polaridade `negativa`
  
**Consulta reescrita:** _pagamento com criptomoeda, bitcoin, erro no pagamento_
  
**Recuperação:** 14.445 avaliações no recorte, 1 relevantes entre 80 candidatas, 1 no contexto

**Resposta:**

> **Evidência insuficiente para apontar um padrão.** Só 1 avaliação passou pelo limiar de relevância no recorte (nota de 1 a 3), abaixo do mínimo de 3. Não generalizo; seguem para conferência, sem verificação de que tratam do tema:
>
> - [R1] (nota 1/5) "o produto recebido veio errado"
