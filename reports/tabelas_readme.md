<!-- base -->
| Etapa | Quantidade |
|---|---|
| Linhas na fonte | 99.224 |
| `review_id` ligados a mais de um pedido (contam uma vez) | 789 |
| Avaliações únicas | 98.410 |
| Sem mensagem na fonte | 57.742 |
| Mensagem vazia após limpeza | 186 |
| **Documentos na base de conhecimento** | **42.138** |

<!-- ablacao -->
| Etapa | P@5 | P@10 | nDCG@10 | MRR | Hit@5 |
|---|---|---|---|---|---|
| RAG ingênuo (pergunta crua, só vetor) | 0,548 | 0,561 | 0,619 | 0,691 | 0,839 |
| + reescrita da pergunta | 0,723 | 0,703 | 0,723 | 0,789 | 0,806 |
| + BM25 (busca híbrida, fusão RRF) | 0,723 | 0,713 | 0,728 | 0,793 | 0,839 |
| **+ filtros de metadado e polaridade (sistema final)** | 0,923 | 0,926 | 0,941 | 0,968 | 1,000 |

<!-- ablacao_recorte -->
| Etapa | P@10 sem recorte (20 perguntas) | P@10 com recorte (11 perguntas) |
|---|---|---|
| RAG ingênuo (pergunta crua, só vetor) | 0,755 | 0,209 |
| + reescrita da pergunta | 0,925 | 0,300 |
| + BM25 (busca híbrida, fusão RRF) | 0,955 | 0,273 |
| + filtros de metadado e polaridade (sistema final) | 0,955 | 0,873 |

<!-- descartadas -->
| Técnica testada | P@10 com | P@10 sem | Decisão |
|---|---|---|---|
| multi-query + HyDE no sistema completo | 0,903 | 0,926 | descartada |
| reranker ordenando o resultado da busca híbrida | 0,648 | 0,703 | descartada |
| reranker contra a consulta principal (em vez do máximo) | 0,668 | 0,703 | descartada |
| sistema completo ordenado pelo reranker | 0,871 | 0,926 | descartada |

<!-- embeddings -->
| Modelo de embedding | P@10 | nDCG@10 | MRR |
|---|---|---|---|
| paraphrase-multilingual-MiniLM-L12-v2 | 0,632 | 0,664 | 0,758 |
| multilingual-e5-base | 0,671 | 0,686 | 0,762 |
| **bge-m3 (escolhido)** | 0,703 | 0,723 | 0,789 |

<!-- metadados -->
| 11 perguntas com recorte por metadado | Sem filtros | Com filtros (sistema final) |
|---|---|---|
| Conformidade ao recorte (top-10) | 30,9% | **95,5%** |
| P@10 (juiz vê os metadados) | 0,273 | **0,873** |

<!-- geracao -->
| Métrica | Resultado |
|---|---|
| Decisão responder x abster correta | 100,0% (44 de 44) |
| Abstenções corretas (fora de escopo + sem evidência) | 13 de 13 |
| Perguntas respondíveis recusadas indevidamente | 0 de 31 |
| Citações válidas (verificadas por código) | 100,0% de 669 |
| Fidelidade dos insights (juiz; sustentado = 1, parcial = 0,5) | 0,96 em 98 insights |
| Insights integralmente sustentados (critério estrito) | 90 de 98 (91,8%) |
| Resumos sustentados pelas evidências citadas | 93,5% |
| Precisão do contexto enviado ao LLM | 92,3% |
| Extração correta dos filtros de metadado | 100% |
| AUC do reranker contra o juiz | 0,707 |

<!-- abstencao -->
| Camada que recusou | Recusas | Perguntas |
|---|---|---|
| 1. Escopo (análise da pergunta, antes de buscar) | 10 | Q29, Q30, Q31, Q32, Q33, Q34, Q36, Q37, Q38, Q40 |
| 2. Relevância (porteiro: menos de 3 evidências acima do limiar) | 1 | Q44 |
| 3. Suficiência (geração: evidências não respondem) | 2 | Q35, Q39 |

<!-- multivendedor -->
pedidos com itens de **mais de um vendedor** (838 comentários) têm 61,3% de avaliações negativas, contra 25,7% na base de comentários

<!-- latencia -->
| Etapa (mediana, sem cache) | Segundos |
|---|---|
| Análise da pergunta (LLM) | 9,9 |
| Recuperação (embeddings, ChromaDB, BM25, reranker; GPU) | 0,6 |
| Geração (LLM) | 13,2 |
| **Total por pergunta** | **22,4** |

<!-- concordancia -->
| Concordância entre juízes (626 pares rejulgados por `gemini-3.5-flash`) | Resultado |
|---|---|
| Concordância exata na escala 0/1/2 | 90,4% |
| Kappa de Cohen ponderado (0/1/2) | 0,887 |
| Concordância em "evidência clara" (decisão usada na P@10) | 96,0% |
| Kappa de Cohen nessa decisão | 0,916 |

<!-- exemplo -->
**Pergunta:** Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?

> As 15 avaliações recuperadas sustentam a conclusão de que existem problemas recorrentes com o prazo de entrega, evidenciados pelo descumprimento de prazos [R1][R2][R3][R4] e pelo não recebimento das mercadorias [R5][R6][R7][R8]. Os clientes relatam atrasos significativos e falta de aviso prévio por parte da empresa [R9][R10][R15].
>
> - **Atrasos recorrentes nas entregas**: Os consumidores apontam o descumprimento sistemático dos prazos estabelecidos para o envio das mercadorias [R1][R3][R4][R10]. Também há menção sobre a falta de comunicação e aviso prévio a respeito da demora [R15]. *(apoio: 10 de 15 evidências)*
> - **Produtos não entregues após o prazo**: Várias avaliações destacam que os produtos não chegaram aos destinatários mesmo após o término do prazo determinado [R2][R4][R6][R11]. Ocorrem situações de demora extrema e pedidos não entregues [R11][R13][R14]. *(apoio: 10 de 15 evidências)*
>
> *Limitações: Este relatório fundamenta a análise em uma amostra de 15 avaliações recuperadas por relevância a partir de um recorte de 14445 comentários, portanto a frequência observada vale apenas para esta amostra.*

| id | sustenta o insight | review_id | nota | texto do cliente |
|---|---|---|---|---|
| R1 | 1 | `10467dc456e818c60bd750271b5d183e` | 1 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | 2 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | Não cumpriu com o prazo e o produto não chegou. |
| R3 | 1 | `48b3ce236ea9d35a4850ea94ca9ca38f` | 2 | Atraso. Produto não chegou no prazo |
| R4 | 1, 2 | `1bfec3e913196c72c1ea06fc8816bd9c` | 1 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R5 | 1, 2 | `9d6c1f490b2b4bfef33820b5679e2d82` | 1 | Atraso entrega. Não recebi o produto |
| R6 | 2 | `986820c39b1a0f1c99bf0592080078bd` | 1 | Não cumpriram o prazo de entrega,ainda não recebi o produto |
| R7 | 1 | `2389923a5e31e36c1184402742965903` | 1 | entrega atrasada,produto ainda não veio |
| R8 | 1, 2 | `4a7118b1f9c3d06869e0cd9d5c1b4ccb` | 1 | meu produto nao chegou esta atrasado. |
| R9 | 1, 2 | `6bb17113a061e2e8bb65b706278b4d75` | 2 | Prazo de entrega não foi cumprido. Encomenda ainda não chegou. |
| R10 | 1 | `f6cdef6e564ca38cd4dcff3ddba22fe1` | 3 | Produto com o prazo de entrega atrasado |
| R11 | 2 | `81a57c09af35f9736f760b6ae16af118` | 1 | Demora, produto nao entregue! |
| R12 | 1, 2 | `a1e9b5056896b01638a5aa8e02673955` | 1 | demora na entrega (ainda nao chegou fora do prazo) |
| R13 | 2 | `0b89db97b78e8a32cf537f263f4aeb65` | 1 | Não cumpre o prazo de entrega,até agora não recebi o meu produto. |
| R14 | 2 | `1f3f5e3000ed6307fbda490057bfa59b` | 2 | Atraso na entrega. Ainda não recebi o produto. |
| R15 | 1 | `85a391b84d8e864de7190a2afb6f82e4` | 1 | não cumpre prazo. Não cumpriram prazo de entrega e nem avisaram o atraso. |

<!-- aspectos -->
micro-F1 0,789 e macro-F1 0,744 em 600 rótulos de teste
