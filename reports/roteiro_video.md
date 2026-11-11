# Roteiro do Vídeo de Apresentação (até 7 minutos)

Uma história contada do primeiro ao último slide: o problema, a decisão de construir o sistema, o
que os dados mostraram, os tropeços, o app funcionando de verdade, os números e o agradecimento. A
linguagem é a de uma conversa profissional; a parte técnica detalhada fica no repositório. As falas
também estão nas notas dos slides.

## Como gravar a voz

1. Lugar silencioso, sempre com o mesmo microfone e a mesma distância (uns 20 cm).
2. Leia o texto como está escrito, no seu ritmo natural. O tempo final é ajustado na edição.
3. Em cada ⏸, faça uma pausa de 2 segundos: é por ela que a edição encaixa a troca de slide e as
   cenas do app.
4. Errou uma frase? Pare um instante e repita a partir do último ⏸; a edição fica com a última
   versão.
5. Pode ser um arquivo só ou vários (um por slide, por exemplo), em qualquer formato de áudio.

## A história, bloco por bloco

*Na tela* descreve a cena do app que entra no vídeo junto com a fala; nos outros blocos, aparece o
slide indicado.

### O começo: o problema e por que a gente decidiu fazer

**1. O problema** (slide 1)

> Oi, pessoal, tudo bem? Meu nome é Luca, do Grupo 110. Toda loja online recebe uma montanha de avaliações, e ninguém consegue ler tudo. Hoje a gente conta como transformou 42 mil comentários da Olist em respostas com prova, e o que deu errado no caminho. ⏸

**2. A decisão** (slide 2)

> Tudo começou com uma pergunta simples: por que o cliente está insatisfeito? A nota avisa, mas quem conta o motivo é o comentário. Então a gente decidiu: e se desse pra simplesmente perguntar? Com três promessas: achar as avaliações certas, mostrar a prova e, quando não souber, admitir. ⏸

### A construção: cada decisão, na ordem em que aconteceu

**3. O primeiro passo** (slide 3)

> O primeiro passo foi abrir os dados. Das 99 mil linhas, só 42 mil tinham comentário, e curtinho, umas 9 palavras, tipo “Atraso. Produto não chegou no prazo”. Por isso a gente decidiu não picotar nada: cada avaliação inteira é uma evidência. ⏸

**4. O que os dados contaram** (slide 4)

> E os dados já contaram duas coisas. Quando a entrega atrasa, as avaliações negativas vão de 9 pra 62%, então a entrega virou filtro de busca. E quem comenta é mais crítico, então todo percentual aqui vale só pra quem comentou. ⏸

**5. O plano** (slide 5)

> Com isso, a gente desenhou o caminho de uma pergunta. O sistema entende o pedido, busca por significado e por palavra exata, separa o que importa, escreve a resposta só com o que encontrou, e no fim o código confere cada citação. ⏸

**6. O primeiro tombo** (slide 6)

> Aí veio o primeiro tombo. Na versão mais simples, só 56% do que vinha era evidência clara. O gestor pergunta “quais reclamações aparecem mais?”, e o cliente escreve “comprei o produto na black friday e até hoje não recebi”. Então a gente decidiu traduzir a pergunta pras palavras do cliente, e subiu pra 71%. ⏸

**7. A surpresa** (slide 7)

> Depois veio a surpresa. A gente colocou um segundo modelo pra reorganizar os resultados, achando que ia melhorar, e caiu de 70 pra 65%, porque ele confunde temas parecidos. Virou só um porteiro. Daí nasceu a regra: só fica o que o teste aprova. ⏸

**8. O grande salto** (slide 8)

> E o grande salto veio dos filtros. Sem eles, a busca achava o tema certo, mas fora do que foi pedido. Com eles, o respeito ao pedido foi de 27 pra 98%. E ainda apareceu um padrão: pedido com mais de um vendedor tem 61% de negativas, contra 26% no geral. ⏸

**9. O que faltava** (slide 9)

> Só que achar não é contar. Se o gestor pergunta o que aparece mais, 30 avaliações não respondem. Ler as 42 mil com IA gastaria cota demais, então a IA etiquetou 3 mil, e essas ensinaram um classificador a estimar o resto. ⏸

### O sistema funcionando: o app de verdade, respondendo e recusando

**10. O sistema funcionando** (app)

*Na tela: O app aberto; o cursor clica na pergunta de exemplo sobre entrega e a resposta aparece.*

> Agora, o sistema funcionando. Eu pergunto: quais reclamações de entrega aparecem mais? ⏸

**11. O sistema funcionando** (app)

*Na tela: A tela desce até o gráfico de frequência dos temas.*

> Produto não recebido lidera, com 33%, e atraso vem depois, com 21%. E esse número olha os 14 mil comentários, não só as 30 avaliações da tela. ⏸

**12. O sistema funcionando** (app)

*Na tela: O cursor abre as evidências do primeiro insight.*

> E cada conclusão abre as avaliações que a sustentam, com o código de cada uma na Olist. ⏸

**13. Sem caixa-preta** (app)

*Na tela: O cursor clica na pergunta de elogios em cama, mesa e banho.*

> Agora um elogio, em cama, mesa e banho, sem marcar filtro nenhum. ⏸

**14. Sem caixa-preta** (app)

*Na tela: A tela desce até “Como a resposta foi construída”.*

> E aqui embaixo ele mostra o caminho: tirou a categoria e a nota da própria pergunta, e de 2.741 avaliações chegou nas 30 que usou. ⏸

**15. O mais difícil** (app)

*Na tela: O cursor clica em “Qual foi o faturamento da Olist em 2018?” e a recusa aparece.*

> Mas o mais difícil foi ensinar o sistema a dizer não. Faturamento da Olist? Fora do assunto: ele nem busca. ⏸

**16. O mais difícil** (app)

*Na tela: O cursor clica na pergunta sobre entrega por drone e a recusa aparece.*

> Entrega por drone é mais traiçoeira: ele acha avaliações de entrega, mas nenhuma fala de drone, então recusa e explica por quê. ⏸

**17. O mais difícil** (slide 12)

> Na avaliação, foram 13 recusas certas em 13, até uma tentativa de manipular o sistema, e nenhuma pergunta válida recusada. ⏸

### A prova e o fim: os números, o que deu trabalho e o agradecimento

**18. A pergunta que importa** (slide 13)

> Aí veio a pergunta que importa: dá pra confiar? A gente montou 44 perguntas, com outra IA julgando. A evidência clara foi de 56 pra 93%, as 44 decisões deram certo, as 714 citações são reais e 101 das 103 conclusões se sustentam. ⏸

**19. A prova real** (slide 14)

> Só que essas perguntas ajudaram a ajustar o sistema, né? Então a gente congelou tudo, escreveu 19 perguntas novas e rodou uma vez só. Deu 19 de 19, com os mesmos 93%. ⏸

**20. O que deu trabalho** (slide 15)

> Nem tudo foi tranquilo. A IA inventava motivo pra recusar, e essa decisão passou pro código. O juiz reprovava resposta certa porque não via os dados do pedido. A cota grátis acabava no meio da avaliação. E teve chamada que travou tudo. ⏸

**21. O que ainda falta** (slide 16)

> E ainda falta coisa: quem julgou foi uma IA, 19 perguntas são poucas e os percentuais são estimativas. ⏸

**22. Obrigado** (slide 17)

> Voltando lá pro começo: agora quem cuida do cliente sabe o motivo da insatisfação e sabe em que confiar. Responder é fácil; o trabalho é saber quando não responder. A parte técnica está toda no GitHub. Muito obrigado! ⏸

## O que o enunciado pede e onde aparece

| Item do enunciado | Blocos |
|---|---|
| Problema de negócio | 1 e 2 |
| Arquitetura proposta | 5 |
| Estratégia do pipeline RAG | 5, 6, 7 e 9 |
| Recuperação das avaliações relevantes | 5, 6, 7, 8 e 14 |
| Demonstração prática (app rodando) | 10 a 16 |
| Exemplos de perguntas | 10, 13, 15 e 16 |
| Evidências que fundamentam as respostas | 12 e 14 |
| Desafios e decisões técnicas | 3, 4, 7, 9 e 20 |
