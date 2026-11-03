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
| + reescrita da pergunta | 0,736 | 0,713 | 0,733 | 0,795 | 0,839 |
| + BM25 (busca híbrida, fusão RRF) | 0,690 | 0,703 | 0,713 | 0,760 | 0,774 |
| **+ filtros de metadado e polaridade (sistema final)** | 0,942 | 0,929 | 0,950 | 0,984 | 1,000 |

<!-- ablacao_recorte -->
| Etapa | P@10 sem recorte (20 perguntas) | P@10 com recorte (11 perguntas) |
|---|---|---|
| RAG ingênuo (pergunta crua, só vetor) | 0,755 | 0,209 |
| + reescrita da pergunta | 0,955 | 0,273 |
| + BM25 (busca híbrida, fusão RRF) | 0,960 | 0,236 |
| + filtros de metadado e polaridade (sistema final) | 0,945 | 0,900 |

<!-- descartadas -->
| Técnica testada | P@10 com | P@10 sem | Diferença (IC 95%) | Decisão |
|---|---|---|---|---|
| multi-query + HyDE no sistema completo | 0,916 | 0,929 | -0,013 [-0,061; +0,035] (empate) | descartada |
| reranker ordenando o resultado da busca híbrida | 0,655 | 0,703 | -0,048 [-0,106; +0,006] (empate) | descartada |
| reranker contra a consulta principal (em vez do máximo) | 0,674 | 0,703 | -0,029 [-0,084; +0,029] (empate) | descartada |
| sistema completo ordenado pelo reranker | 0,861 | 0,929 | -0,068 [-0,129; -0,013] | descartada |

<!-- embeddings -->
| Modelo de embedding | P@10 | nDCG@10 | MRR | P@10 contra o bge-m3 (IC 95%) |
|---|---|---|---|---|
| paraphrase-multilingual-MiniLM-L12-v2 | 0,632 | 0,645 | 0,715 | -0,081 [-0,145; -0,026] |
| multilingual-e5-base | 0,632 | 0,651 | 0,743 | -0,081 [-0,148; -0,023] |
| **bge-m3 (escolhido)** | 0,713 | 0,733 | 0,795 | referência |

<!-- metadados -->
| 11 perguntas com recorte por metadado | Sem filtros | Com filtros (sistema final) |
|---|---|---|
| Conformidade ao recorte (top-10) | 27,3% | **98,2%** |
| P@10 (juiz vê os metadados) | 0,236 | **0,900** |

<!-- geracao -->
| Métrica | Resultado |
|---|---|
| Decisão responder x abster correta | 100,0% (44 de 44) |
| Abstenções corretas (fora de escopo + sem evidência) | 13 de 13 (IC 95% [0,77; 1,00]) |
| Perguntas respondíveis recusadas indevidamente | 0 de 31 |
| Citações válidas (verificadas por código) | 100,0% de 714 |
| Avaliações citadas que o juiz marcou como evidência clara (relacionadas) | 93,2% (98,7%) de 632 julgadas |
| Fidelidade dos insights (juiz; sustentado = 1, parcial = 0,5) | 0,99 em 103 insights |
| Insights integralmente sustentados (critério estrito) | 101 de 103 (98,1%) |
| Resumos sustentados pelas evidências citadas | 96,8% |
| Precisão do contexto enviado ao LLM | 91,6% |
| Extração correta dos filtros de metadado | 100% |
| AUC do reranker contra o juiz | 0,833 |

<!-- abstencao -->
| Camada que recusou | Recusas | Perguntas |
|---|---|---|
| 1. Escopo (análise da pergunta, antes de buscar) | 7 | Q29, Q30, Q31, Q32, Q33, Q34, Q38 |
| 2. Relevância (porteiro: menos de 3 evidências acima do limiar) | 4 | Q36, Q37, Q40, Q44 |
| 3. Suficiência (geração: evidências não respondem) | 2 | Q35, Q39 |

<!-- retidas -->
| Métrica | Desenvolvimento (44 perguntas) | **Retidas (19 perguntas, rodadas uma vez)** |
|---|---|---|
| Decisão responder x abster correta | 44 de 44 (IC 95% [0,92; 1,00]) | **19 de 19** (IC 95% [0,83; 1,00]) |
| Recusas corretas | 13 de 13 | **7 de 7** |
| P@10 | 0,929 | **0,933** |
| Hit@5 | 1,000 | **1,000** |
| Conformidade ao recorte (top-10) | 98,2% | **100,0%** |
| Citações válidas | 100,0% de 714 | **100,0% de 277** |
| Insights integralmente sustentados (juiz) | 101 de 103 | **38 de 38** |
| Filtros de metadado extraídos corretamente | 11 de 11 | **5 de 5** |

<!-- multivendedor -->
pedidos com itens de **mais de um vendedor** (838 comentários) têm 61,3% de avaliações negativas, contra 25,7% na base de comentários

<!-- latencia -->
| Etapa (mediana, sem cache) | Segundos |
|---|---|
| Análise da pergunta (LLM) | 1,8 |
| Recuperação (embeddings, ChromaDB, BM25, reranker; GPU) | 1,4 |
| Geração (LLM) | 12,2 |
| **Total por pergunta** | **15,4** |
| Perguntas inéditas respondidas nesta medição | 5 de 5 |

<!-- concordancia -->
| Concordância entre juízes (626 pares rejulgados por `gemini-3.5-flash`) | Resultado |
|---|---|
| Concordância exata na escala 0/1/2 | 90,4% |
| Kappa de Cohen ponderado (0/1/2) | 0,887 |
| Concordância em "evidência clara" (decisão usada na P@10) | 96,0% |
| Kappa de Cohen nessa decisão | 0,916 |

<!-- exemplo -->
**Pergunta:** Quais avaliações sustentam a conclusão de que existem problemas recorrentes relacionados ao prazo de entrega?

> O problema de prazo de entrega é corroborado pelo quadro de frequências, que aponta atraso na entrega em 21,2% e produto não recebido em 33,0% das 14445 avaliações do recorte. Todas as 15 avaliações recuperadas sustentam essa conclusão, evidenciando falhas no cumprimento de datas prometidas [R1][R5][R10][R15]. Os clientes relatam insatisfação com a demora e com a falta de entrega dos itens [R2][R6][R11].
>
> - **Descumprimento de prazos de entrega**: Os clientes relatam recorrentemente que a loja não cumpre os prazos estabelecidos para a entrega das mercadorias [R1][R2][R5][R6]. Há queixas explícitas sobre o não cumprimento das datas prometidas no momento da compra [R3][R8][R10][R13]. *(apoio: 8 de 15 evidências)*
> - **Atrasos prolongados e produtos não entregues**: Várias avaliações apontam que os produtos estão atrasados e não chegaram aos endereços dos consumidores [R4][R7][R9][R11]. Também são relatados prazos longos e a ausência de recebimento definitivo dos itens [R12][R14]. *(apoio: 6 de 15 evidências)*
> - **Falta de comunicação sobre o atraso**: Os consumidores destacam a ausência de aviso prévio sobre os problemas de atraso na entrega [R13]. Além disso, é apontada a falta de satisfação ou justificativas por parte da empresa quanto à demora [R15]. *(apoio: 2 de 15 evidências)*
>
> *Limitações: O quadro de frequências indica a proporção na base completa de 14445 avaliações do recorte, enquanto as 15 evidências representam apenas uma amostra recuperada por relevância.*
>
> *Percentuais: estimativa do classificador de aspectos sobre as 14.445 avaliações com comentário do recorte (nota de 1 a 3).*

| id | sustenta o insight | review_id | nota | texto do cliente |
|---|---|---|---|---|
| R1 | 1 | `10467dc456e818c60bd750271b5d183e` | 1 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | 1 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | Não cumpriu com o prazo e o produto não chegou. |
| R3 | 1 | `48b3ce236ea9d35a4850ea94ca9ca38f` | 2 | Atraso. Produto não chegou no prazo |
| R4 | 2 | `4a7118b1f9c3d06869e0cd9d5c1b4ccb` | 1 | meu produto nao chegou esta atrasado. |
| R5 | 1 | `f2a8882c104b38310adaf0a9a521b42f` | 1 | Produto atrasado, loja não cumpre o q promete. |
| R6 | 1 | `7a37e297352c8a7b1652f721c861dcd6` | 1 | Não cumpriu o prazo de entrega. |
| R7 | 2 | `1bfec3e913196c72c1ea06fc8816bd9c` | 1 | entrega atrasada. o prazo terminou e nao recebi meu produto |
| R8 | 1 | `6bb17113a061e2e8bb65b706278b4d75` | 2 | Prazo de entrega não foi cumprido. Encomenda ainda não chegou. |
| R9 | 2 | `b28bfbd00dfd0c6d80e9cb524e0f205e` | 1 | Produto não chegou está com 2 dias de atraso |
| R10 | 1 | `986820c39b1a0f1c99bf0592080078bd` | 1 | Não cumpriram o prazo de entrega,ainda não recebi o produto |
| R11 | 2 | `4d2d379325d0b5d7e92ea25ac8d289c4` | 1 | Meu produto está atrasado e ainda não chegou |
| R12 | 2 | `170b122d01f94b40e901a7a1d22cf67a` | 1 | Não recebi. O produto não chegou ainda, está em atraso. |
| R13 | 1, 3 | `85a391b84d8e864de7190a2afb6f82e4` | 1 | não cumpre prazo. Não cumpriram prazo de entrega e nem avisaram o atraso. |
| R14 | 2 | `8b592f04ffb1115da4b08205a4f0f3b1` | 1 | prazo longo de entrega e não chegou no prazo |
| R15 | 3 | `c3039a71818e8c4ebe2f1a905ab1f863` | 1 | Demora muito e eles não dão satisfação pelo motivo do atraso |

<!-- aspectos -->
micro-F1 0,789 e macro-F1 0,744 em 600 rótulos de teste
