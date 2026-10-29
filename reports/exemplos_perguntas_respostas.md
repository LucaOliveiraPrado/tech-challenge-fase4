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

<details><summary><b>As 30 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `9d6c1f490b2b4bfef33820b5679e2d82` | 1 | 0,98 | Atraso entrega. Não recebi o produto |
| R2 | 1 | `a04625605c0ed62e208637697536eff9` | 1 | 0,98 | Até o momento não recebi o produto que está atrasado na entrega. |
| R3 | 1 | `1bfec3e913196c72c1ea06fc8816bd9c` | 1 | 0,94 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R4 | 2 | `a9d65ad284bb1c477d7473cd06272070` | 3 | 0,99 | O produto veiocom defeito. O produto veio com defeito e atraso na entrega. |
| R5 | 2 | `83c4f54bd18decda21d563b5ddf5558a` | 1 | 0,93 | Recebi o produto com defeito |
| R6 | 1 | `98eaf3a20ac997b34bf433ac0979f4e2` | 1 | 0,98 | Atraso na entrega, até o momento nao recebi o meu produto. |
| R7 | 1 | `e99c29f0a950abd77239b15adaaa38b8` | 1 | 0,92 | Ainda nao recebi o produto e ja se encontra atrasado |
| R8 | 1 | `8f9772ae7dec3db4af0418fd7fb1be4d` | 1 | 0,99 | Produto com entrega atrasada |
| R9 | 1, 3 | `b5e71e87bfbbcd2a826b9610bac99680` | 1 | 0,87 | atraso na entrega. nao recebi meu produto e nem uma posição sobre o mesmo |
| R10 | 1 | `4a7118b1f9c3d06869e0cd9d5c1b4ccb` | 1 | 0,91 | meu produto nao chegou esta atrasado. |
| R11 | 1 | `2acb97b500b95b1205a5e4aea261a172` | 3 | 0,39 | Produto recebido é o correto, mas teve significativo atraso na entrega. |
| R12 | 1 | `2389923a5e31e36c1184402742965903` | 1 | 0,85 | entrega atrasada,produto ainda não veio |
| R13 | 1 | `b35041292c711e10c0589a676b4c88d6` | 3 | 0,98 | Recebi meu produto porem com certo atraso. |
| R14 | 1 | `66b7b7c200a3fa372cbd01606bba551f` | 2 | 0,90 | Entrega atrasada. Até o momento não foi entregue o produto |
| R15 | 2 | `801fb7f38a93205e682ef363234bd7dd` | 1 | 0,98 | a entrega demorou e o produto chegou com defeito |
| R16 | 2 | `556e5259e2d5b0cbeec371d7a22bef5a` | 1 | 0,72 | O produto veio estragado |
| R17 | 1 | `1f3f5e3000ed6307fbda490057bfa59b` | 2 | 0,93 | Atraso na entrega. Ainda não recebi o produto. |
| R18 | 1 | `db64106aff6c7180cb841937f43f5f44` | 1 | 0,90 | Entrega atrasada. Ainda não recebi o produto... |
| R19 | 1, 3 | `14ab06af2677555bfcf9ff2e64a1b203` | 1 | 0,67 | O produto não foi entregu. Sem satisfação sobre atraso na entrega |
| R20 | 2 | `6298846cdf0eceb7ba5661c3810725b7` | 1 | 0,74 | Atrasado e com defeito. Produto chegou atrasado, mal embalado e faltando um Ilhós. |
| R21 | 1 | `f6cdef6e564ca38cd4dcff3ddba22fe1` | 3 | 0,98 | Produto com o prazo de entrega atrasado |
| R22 | 1 | `ac6bdc8a49173f8db773a6a97fc6d087` | 2 | 0,88 | Atraso no entrega. Acredito que tenha sido atraso dos correios , ainda não recebi o produto . |
| R23 | 1 | `d5ec0edbe1505d4f8c80f52d9c19f98d` | 2 | 0,93 | demora na entrega, ainda não recebi o produto |
| R24 | 1 | `d8bef0bbad507b83d991b958f50b33f3` | 1 | 0,75 | não recebi o produto no prazo previsto |
| R25 | 1 | `4cc9dc519327a019f0193e75e34c851d` | 1 | 0,79 | Atraso. Ainda não recebi o produto. |
| R26 | 1 | `4ff3c370099faa740e4ff1c3626b760b` | 1 | 0,76 | Produto nao entregue. Meu produto nao foi entrrgue |
| R27 | 1 | `6f90ca0354205d409ba72f8fbdd2542e` | 2 | 0,81 | não tenho como avaliar. ainda nem recebi o produto, que esta com entrega atrasada. |
| R28 | 2, 3 | `b0604d9692c6e66726898d64faa22da2` | 1 | 0,47 | produto estragado. liguei na central de vcs e não obtive o retorno |
| R29 | 2, 3 | `db551ada5aa80d023f7529ca90bffee7` | 1 | 0,32 | O produto veio com defeito enviei email e nao obtive resposta |
| R30 | 1 | `d1cb6e8ac59c40427069ffddd69e0346` | 1 | 0,40 | PRODUTO 3 DIAS DE ATRASO. PRODUTO COM 3 DIAS DE ATRASO NA ENTREGA |

</details>

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

<details><summary><b>As 14 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `10467dc456e818c60bd750271b5d183e` | 1 | 1,00 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | 2 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | 1,00 | Não cumpriu com o prazo e o produto não chegou. |
| R3 | 1 | `48b3ce236ea9d35a4850ea94ca9ca38f` | 2 | 1,00 | Atraso. Produto não chegou no prazo |
| R4 | 1 | `1bfec3e913196c72c1ea06fc8816bd9c` | 1 | 0,97 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R5 | 2 | `9d6c1f490b2b4bfef33820b5679e2d82` | 1 | 0,98 | Atraso entrega. Não recebi o produto |
| R6 | 2 | `986820c39b1a0f1c99bf0592080078bd` | 1 | 0,99 | Não cumpriram o prazo de entrega,ainda não recebi o produto |
| R7 | 1 | `2389923a5e31e36c1184402742965903` | 1 | 1,00 | entrega atrasada,produto ainda não veio |
| R8 | 1 | `6bb17113a061e2e8bb65b706278b4d75` | 2 | 1,00 | Prazo de entrega não foi cumprido. Encomenda ainda não chegou. |
| R9 | 2 | `4a7118b1f9c3d06869e0cd9d5c1b4ccb` | 1 | 0,99 | meu produto nao chegou esta atrasado. |
| R10 | 2 | `81a57c09af35f9736f760b6ae16af118` | 1 | 0,99 | Demora, produto nao entregue! |
| R11 | 1 | `f6cdef6e564ca38cd4dcff3ddba22fe1` | 3 | 1,00 | Produto com o prazo de entrega atrasado |
| R13 | 1 | `a1e9b5056896b01638a5aa8e02673955` | 1 | 0,99 | demora na entrega (ainda nao chegou fora do prazo) |
| R14 | 2 | `1f3f5e3000ed6307fbda490057bfa59b` | 2 | 0,98 | Atraso na entrega. Ainda não recebi o produto. |
| R15 | 2 | `0bb09618b24d6de1e9bf4fee647023ae` | 1 | 0,87 | demora e não entrega. péssimo |

</details>

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

<details><summary><b>As 30 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1, 2 | `c6d38a0f9663dc7d1cae7cf29e5c85b4` | 5 | 1,00 | produto de excelente qualidade entrega super rapida adorei. |
| R2 | 1, 2 | `9eb82fb5f3e052a1feac474a6f49e417` | 5 | 0,99 | Adorei,produto ótimo e a entrega é super rápido |
| R3 | 1, 2 | `5ab5ace545295c27446efb6d17f6fae3` | 5 | 1,00 | Produto excelente e entrega ótima e rápida! |
| R4 | 1, 2 | `08b8ab4cd13b5ce55a4f6558ba1d1c87` | 5 | 0,99 | Ótimo produto excelente qualidade entrega rápida. |
| R5 | 3 | `b71e2b3cd969864092bc35e61126b5ca` | 5 | 0,94 | Adorei! Excelente atendimento! 👏 |
| R6 | 2, 3 | `5962f753a7cdb529f3793b9c47c6c563` | 5 | 0,99 | Excelente atendimento e entrega rápida!!! |
| R7 | 1, 2 | `a90c2e509ee3c268059e0069e197cfa4` | 5 | 1,00 | Entrega super rápida produto ótimo amei e recomendo |
| R8 | 1, 3 | `aa4c3c44ff9674915f652865b243ba31` | 5 | 0,98 | Produto excelente! Adorei! Estou feliz com o atendimento, o serviço prestado e o produto é ótimo. |
| R9 | 1, 2 | `33dd60a4eab572eaab8cc5471ac412de` | 5 | 1,00 | Produto ótimo chegou super rápido amei |
| R10 | 2, 3 | `0dc18463d185b23148ec7ceb0ac70b64` | 5 | 0,94 | Prazo de entrega excelente.Foi mais rápido do que eu esperava. Estão de parabéns pelo ótimo atendimento. |
| R11 | 1, 2 | `f2f694e8f172b05cfe300f31a749bb01` | 5 | 0,99 | amei o produto muito bom , entregue super rapido |
| R12 | 2, 3 | `76ebfe3c6a80a7924183178435de1399` | 5 | 0,99 | ótimo atendimento, entrega rápida. |
| R13 | 1, 2 | `54415d54900580729f397d75fd35bc06` | 5 | 1,00 | Excelente produto, entrega super rápida |
| R14 | 1, 2 | `bdaa916abe148098807f3a2e553a29a5` | 5 | 0,98 | Entrega super rápida ,produto excelente,minha filha adorou. |
| R15 | 1, 2 | `3470d23da6843a4ece28cdac3892430a` | 5 | 0,99 | entrega super rápida e ótimo produto |
| R16 | 1, 2 | `8a1d8ca4278233f4392523b32dd4f516` | 5 | 0,99 | ótimo produto e entrega super rápida. |
| R17 | 1, 2 | `78b60d1794db558c6ae574d04f1e2a77` | 5 | 1,00 | Ótimo! Adorei o produto, tempo de entrega rápido. |
| R18 | 1, 2 | `a0ba13e19e2a6f416f963ef97a0089b4` | 5 | 0,99 | Rápida entrega excelente produto |
| R19 | 3 | `2987a2dcd950d0a74f3db048033291b7` | 4 | 0,96 | Excelente. Ótimo atendimento |
| R20 | 1, 2 | `47581c0859ee6686c6a1aa71c2b9bd11` | 5 | 1,00 | Produto excelente e entrega super rápida. |
| R21 | 1, 2 | `4e75eb63d1145397fad978c933de9dc6` | 5 | 1,00 | Produto ótimo, entrega super rápida |
| R22 | 1, 2 | `76fe154d4cba8f87cc55433b3465fdc3` | 5 | 0,99 | Produto excelente chegou muito rápido recomendo |
| R23 | 1, 2 | `90cfae6fc1efa4e0d4d4483f81ad75b1` | 4 | 1,00 | Ótimo. Produto excelente, entrega rápida |
| R24 | 2, 3 | `8179eb34f345e70f71a4a3e7191f7ef9` | 5 | 0,96 | Ótimo atendimento. Muito bom o atendimento a entrega foi rápida e o produto foi entregue. |
| R25 | 1, 2 | `6953c13980fc183745ea3fc0595c0d4e` | 5 | 1,00 | ótimo produto, entrega rápida. |
| R26 | 1 | `02a8d9699a0dc9a726a7c530c70c839e` | 5 | 0,99 | Produto excelente e de ótima qualidade. Adorei. |
| R27 | 1, 2 | `b3c4ba2611c68e6c17ea54055d729fc2` | 5 | 0,99 | Entrega super rápida, ótimo produto |
| R28 | 3 | `0dc0fa5941a93260a51e03b73f743bd3` | 5 | 0,98 | Excelente Atendimento e extremamente rápido. |
| R29 | 2, 3 | `fd896ad2cffd5956a819fcbb3f7d7044` | 5 | 0,96 | Super Recomendado. entrega rápida, e atendimento excelente |
| R30 | 1, 2 | `d79c46a2a43217f5eab05683e580ce37` | 5 | 0,99 | Estraga rápida produto bom adorei excelente |

</details>

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

<details><summary><b>As 15 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `10467dc456e818c60bd750271b5d183e` | 1 | 1,00 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | 2 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | 1,00 | Não cumpriu com o prazo e o produto não chegou. |
| R3 | 1 | `48b3ce236ea9d35a4850ea94ca9ca38f` | 2 | 1,00 | Atraso. Produto não chegou no prazo |
| R4 | 1, 2 | `1bfec3e913196c72c1ea06fc8816bd9c` | 1 | 0,98 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R5 | 1, 2 | `9d6c1f490b2b4bfef33820b5679e2d82` | 1 | 0,99 | Atraso entrega. Não recebi o produto |
| R6 | 2 | `986820c39b1a0f1c99bf0592080078bd` | 1 | 0,99 | Não cumpriram o prazo de entrega,ainda não recebi o produto |
| R7 | 1 | `2389923a5e31e36c1184402742965903` | 1 | 1,00 | entrega atrasada,produto ainda não veio |
| R8 | 1, 2 | `4a7118b1f9c3d06869e0cd9d5c1b4ccb` | 1 | 0,99 | meu produto nao chegou esta atrasado. |
| R9 | 1, 2 | `6bb17113a061e2e8bb65b706278b4d75` | 2 | 1,00 | Prazo de entrega não foi cumprido. Encomenda ainda não chegou. |
| R10 | 1 | `f6cdef6e564ca38cd4dcff3ddba22fe1` | 3 | 1,00 | Produto com o prazo de entrega atrasado |
| R11 | 2 | `81a57c09af35f9736f760b6ae16af118` | 1 | 0,99 | Demora, produto nao entregue! |
| R12 | 1, 2 | `a1e9b5056896b01638a5aa8e02673955` | 1 | 0,99 | demora na entrega (ainda nao chegou fora do prazo) |
| R13 | 2 | `0b89db97b78e8a32cf537f263f4aeb65` | 1 | 0,99 | Não cumpre o prazo de entrega,até agora não recebi o meu produto. |
| R14 | 2 | `1f3f5e3000ed6307fbda490057bfa59b` | 2 | 0,98 | Atraso na entrega. Ainda não recebi o produto. |
| R15 | 1 | `85a391b84d8e864de7190a2afb6f82e4` | 1 | 0,93 | não cumpre prazo. Não cumpriram prazo de entrega e nem avisaram o atraso. |

</details>

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

<details><summary><b>As 21 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `d29b7015c1970a48ebd84998398336fb` | 5 | 0,88 | Produto de excelente qualidade, tecido macio e confortável. Recomendo |
| R2 | 1, 4 | `a1a020107703479332a3174ccbf3c039` | 5 | 0,87 | Produto muito bom adorei o tecido e entregue no prazo |
| R3 | 1, 2 | `4dfe75c40bfc9e9622bd023678bf4366` | 5 | 0,91 | Excelente produto, parece ser resistente e ficou lindo na cama, dá pena colocar lençol em cima. Amei! |
| R4 | 3 | `15fa2777d5ba15537d0cfea3fc458b35` | 5 | 0,64 | Jogo de cama. Excelente produto. Recomendo a todos |
| R5 | 1, 2 | `33e9e4a3b2e109d14a0ee690fb198a7c` | 5 | 0,55 | Jogo de lençol muito lindo...macio e aconchegante...ficou linda a minha cama.. |
| R6 | 2 | `aef781f1cdf68558187a2d2b042179cd` | 5 | 0,32 | Lindo e de qualidade. O tamanho é excelente e a cama ficou muito nobre. Recomendo. |
| R7 | 1 | `f559465cc5ef632af3bfc8ef12501b9d` | 4 | 0,75 | Ótimo produto e tem uma boa qualidade, tecido e costura muito bem feita. |
| R8 | 1 | `2e6df755486ec2fa17bebd038f7d0f90` | 5 | 0,88 | Adorei a qualidade e o acabamento. |
| R10 | 1 | `3dc34dca59e105526f4529f762ce596d` | 5 | 0,93 | Excelente tecido !!!! Recomendo! |
| R11 | 2 | `c4840b4b962b68618ddf9dc656882bfe` | 5 | 0,79 | Roupa de cama de muito boa qualidade. Deixa o quarto lindo. |
| R12 | 1 | `f66479352b04e33b4009139f5c6fa147` | 5 | 0,78 | Lençol de ótima qualidade! Cor um pouco mais clara do que na foto. |
| R13 | 3 | `7c61cf4990b780ec18f2fcf6ab4c6ff5` | 5 | 0,69 | Adorei o produto...ótima qualidade!! Recomendo. |
| R16 | 1 | `221894cf48eac99ea8e784c52e9be004` | 5 | 0,68 | Excelente produto. Adorei o cobertor. Muito confortável e bom custo benefício. |
| R18 | 2, 3 | `f75113128c5c1962af7b554ccddb9c92` | 5 | 0,31 | Atendeu minhas espectativas! Produto muito bom. Ficou ótimo na minha cama. Compraria novamente. |
| R19 | 2 | `54d9494c037eafacb61d86b6da1b143b` | 5 | 0,43 | Linda cortina. Adorei o tecido |
| R20 | 3 | `5630abc53f149bdca0caecf5add198b0` | 5 | 0,60 | material do tecido muito. preço otimo,e material muito bom,eu recomendo |
| R22 | 2, 4 | `0dfc8a64244f7f559f792e2e326434b6` | 5 | 0,39 | produto lindo,bem grande e otimo tecido entrega muito rapida estou muito satisfeita |
| R23 | 1 | `0720c7613ace9b12d61f2b08805d11c6` | 5 | 0,78 | produto muito bom,confortavel. |
| R26 | 2 | `651fd497cbd50edc1a7d19a3f1b87bd5` | 5 | 0,57 | É exatamente o que eu esperva,amei essa saia para cama excelente produto. |
| R27 | 1, 3, 4 | `5b54c52e7c7594250c4fc80280ba1d92` | 5 | 0,76 | Super Recomendo. Lençol e fronhas de ótima qualidade ,já lavei inclusive e não houve problemas na coloração ou encolhimento. Entrega feita antes do prazo. |
| R29 | 2 | `1678e11e7efd5ca53f73c6a465bf3f22` | 5 | 0,97 | Amei! Lindo o Lençol! |

</details>

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

<details><summary><b>As 29 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `373cbeecea8286a2b66c97b1b157ec46` | 1 | 0,99 | Não chegou meu produto. Péssimo |
| R2 | 1 | `9f642a55932d21d42cb4681ee0aff6cb` | 1 | 0,94 | Pessimo. Não entrega o produto |
| R3 | 1 | `95ba29208d5172ce9f9890946cd6e30a` | 1 | 0,96 | Produto não entregue. Péssima empresa, não entregam os produtos. |
| R4 | 3 | `e0837ec1045787e50e4a7be51779035b` | 1 | 0,96 | O produto não chegou está muito atrasado. Pessima essa loja |
| R5 | 3 | `9d6c1f490b2b4bfef33820b5679e2d82` | 1 | 0,97 | Atraso entrega. Não recebi o produto |
| R6 | 3 | `4a7118b1f9c3d06869e0cd9d5c1b4ccb` | 1 | 0,98 | meu produto nao chegou esta atrasado. |
| R7 | 3 | `2389923a5e31e36c1184402742965903` | 1 | 0,97 | entrega atrasada,produto ainda não veio |
| R8 | 3 | `b28bfbd00dfd0c6d80e9cb524e0f205e` | 1 | 0,95 | Produto não chegou está com 2 dias de atraso |
| R9 | 3 | `170b122d01f94b40e901a7a1d22cf67a` | 1 | 0,94 | Não recebi. O produto não chegou ainda, está em atraso. |
| R10 | 3 | `6cc69853b87354bdb75c227a85cde581` | 1 | 0,72 | Não entregaram o produto. Loja péssima, não cumpre com seus prazos! |
| R11 | 4 | `d4469da4ea0680551bd2f446a5e45a28` | 1 | 0,99 | pessimo. produto com defeito. |
| R12 | 4 | `190b01af91fb754443307e59209136d6` | 1 | 0,96 | produto insatisfatorio. demora na entrega e produto de baixa qualidade |
| R13 | 4 | `6298846cdf0eceb7ba5661c3810725b7` | 1 | 0,57 | Atrasado e com defeito. Produto chegou atrasado, mal embalado e faltando um Ilhós. |
| R14 | 1 | `51beaf6a397e57bb1880f4f49cb0535f` | 1 | 0,97 | produto não entregue |
| R15 | 2 | `ea98ee7eb77ad3f059f74548a87feb3a` | 1 | 0,87 | Péssimo atendimento o produto chegou mais não demorou um pouco |
| R16 | 2 | `237ec2d8031fa4fc3d6eb3c1825273ed` | 1 | 0,93 | Entrega e Atendimento. Péssimo atendimento! |
| R17 | 2 | `2e1d71fce98b42bf6cbdd5e06798c286` | 1 | 0,33 | Zero. O produto chegou com defeito é o site da lannister é péssimo pra trocas, suporte péssimo !!!! |
| R19 | 1 | `93058d6f2eb8fcf4174efcf87a42b2db` | 1 | 0,96 | Meu produto não foi entregue |
| R20 | 2, 3 | `4b25ec9d7825fbb69b4815c7ab4d94fa` | 1 | 0,40 | Entrega. Péssimo atendimento. Nao me deram nem explicações para este 1 MÊS de atraso. Nunca mais faço compras pela lannister. |
| R21 | 1 | `f142abf096ae70fa061c66fe2d36786b` | 1 | 0,99 | Meu produto não chegou. |
| R22 | 3 | `4d2d379325d0b5d7e92ea25ac8d289c4` | 1 | 0,97 | Meu produto está atrasado e ainda não chegou |
| R23 | 1 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | 0,96 | Não cumpriu com o prazo e o produto não chegou. |
| R24 | 2 | `ed8017eaaea74d271affe463beb1256d` | 1 | 0,67 | Péssimo atendimento péssima entrega. Sequer tive retorno de minha compra cadê o produto porque o PGTO já foi recebido. |
| R25 | 2 | `07df55457e11d32f632ba70fb0257406` | 1 | 0,47 | Zero. Atendimento péssimo |
| R26 | 4 | `9eb2e56b505c2cec094833032f94d3e1` | 1 | 0,43 | Não funciona, mais uma vez meu produto chegou com defeito! |
| R27 | 2 | `ced0560b692ae389904d584f03f4d8bf` | 1 | 0,45 | produto com defeito. estou desde o dia 22 tentando resolver o problema do produto ter vindo com defeito, mas só me atendem no atendimento eletrônico. |
| R28 | 3 | `cf6506ccf9e5680269e733ff320d514d` | 1 | 0,71 | Péssima entrega. Até agora não recebi meu produto. Minha esposa está tendo prejuízo financeiro por conta desse atraso, pois ela é nutricionista e está dependo disso para atender sua clientela. |
| R29 | 3 | `d1cb6e8ac59c40427069ffddd69e0346` | 1 | 0,32 | PRODUTO 3 DIAS DE ATRASO. PRODUTO COM 3 DIAS DE ATRASO NA ENTREGA |
| R30 | 4 | `d03d0d6dd3bfa65212e1f12ae7c0de8e` | 1 | 0,43 | Produto com defeito. O produto veio com defeito e não foi possível trocar, pois não havia como repor. |

</details>

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

<details><summary><b>As 19 evidências citadas</b> (review_id completo e insight que cada uma sustenta)</summary>

| id | sustenta o insight | review_id | nota | relevância | texto do cliente |
|---|---|---|---|---|---|
| R1 | 1 | `c84049c42940addc4d9b725ee5456da6` | 2 | 0,69 | Recebi pedido incompleto. Foi entregue somente parte do pedido, sendo que os produtos eram da mesma loja |
| R2 | 1 | `ee36eb06005e20daece65976bd9990e4` | 1 | 0,99 | Pedido entregue incompleto. |
| R3 | 1 | `ea367d520c1e07a970c0452a97496afe` | 1 | 0,61 | Nao recebi um dos produtos. o pedido veio incompleto! |
| R4 | 1 | `96b9f6a6bda6908a59c0a0c9a6141d2c` | 3 | 0,50 | Pedido Incompleto. Meu produto foi entregue parcialmente, falta 01 produto e consta no status que foi entregue. |
| R5 | 2 | `c7c623cd643523c4f570e2358dec9e61` | 1 | 0,32 | entrega incompleta. Comprei dois produtos da mesma loja porem recebia apenas não recebi nenhum retorno da loja ate agora |
| R6 | 2 | `fc61dfc1eae7e8444cbd745a0344da5f` | 2 | 0,60 | Produtos vieram incompletos,estou aguardando entrarem em contato comigo |
| R7 | 1 | `7e4dbfbeef349260ecb3422379692204` | 2 | 0,49 | Pedido atendido parcialmente. Comprei três produtos, mas somente um dos itens foi entregue . |
| R8 | 2 | `8cbd43b45179c8a12c3485edb697c56f` | 1 | 0,46 | Pedido veio incompleto. Vieram faltando produtos e até agora ninguém respondeu meus e-mails. |
| R9 | 1 | `bcf1f7d1fdf796f91d59cdfab8798d7a` | 1 | 0,40 | Produto entregue faltando encomendas |
| R10 | 1 | `2e56674aa72757a9c730a5886e3b210a` | 3 | 0,50 | Não entendo no mesmo pedido não entregarem a mercadoria completa |
| R11 | 1 | `e70c3511b7dcbe1966bec2a3b9f959d7` | 1 | 0,37 | O pedido veio somente um produto e faltando outro. |
| R12 | 1 | `bfcf782c80320e7e799e5f18381b5f35` | 1 | 0,44 | Ainda está no prazo, produto está incompleto |
| R13 | 1 | `b18340cf01849bf97d176b4b011dc7c0` | 1 | 0,89 | Não foi enviado o pedido completo, somente uma parte |
| R14 | 1 | `ff73170d8a9deb95aa4814ddbec217b4` | 2 | 0,75 | entregou faltando um produto |
| R15 | 2 | `5148ad2bdca65375e9504355d79c6ad4` | 1 | 0,32 | Entrega incompleta. Realizei um pedido com dois itens e apenas 1 deles foi entregue. Fiz algumas reclamações e até agora ninguém entrou em contato comigo pra entregar o outro produto ou para devolver o dinheiro. |
| R16 | 1 | `2376f556b8d5c24003acef73ab11f636` | 3 | 0,42 | Foi entregue apenas parte do pedido |
| R17 | 1 | `d765064065d3c324c90f7e24ed6e0d12` | 1 | 0,31 | Entrega incompleta. Comprei 2 itens...uma rede de dormir e mesa com 2 cadeiras infantis .Só recebi a rede. |
| R18 | 1 | `b8a5fabf78dad94a57610e6835fc9dd1` | 1 | 0,54 | Um dos produtos marcado como entregue não foi recebido. |
| R19 | 1 | `06ed69462b99956d9e41146accb7f291` | 2 | 0,86 | Falta entregar um dos produtos |

</details>

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

## Q37. Quais reclamações existem sobre pagamento com criptomoedas?

**Status:** abstenção: fora do escopo
  
**Análise da pergunta:** tipo `tema`, polaridade `qualquer`
  
**Consulta reescrita:** _pagamento criptomoedas bitcoin_

**Resposta:**

> **Fora do escopo da base de conhecimento.** A base de conhecimento não possui registros sobre pagamentos com criptomoedas.
>
> A base contém apenas avaliações escritas por clientes da Olist entre 2016 e 2018 sobre suas compras (entrega, produto, atendimento, vendedor, embalagem, preço). Não respondo com conhecimento externo para não apresentar algo que os dados não sustentam.
