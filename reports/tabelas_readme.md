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
| RAG ingênuo (pergunta crua, só vetor) | 0,600 | 0,607 | 0,664 | 0,722 | 0,893 |
| + reescrita da pergunta | 0,821 | 0,800 | 0,817 | 0,863 | 0,893 |
| + BM25 (busca híbrida, fusão RRF) | 0,786 | 0,804 | 0,812 | 0,869 | 0,893 |
| **+ filtros de metadado, polaridade e reranker como porteiro (sistema final)** | 0,914 | 0,939 | 0,943 | 0,964 | 1,000 |

<!-- descartadas -->
| Técnica testada | P@10 com | P@10 sem | Decisão |
|---|---|---|---|
| multi-query + HyDE sobre a consulta reescrita | 0,750 | 0,800 | descartada |
| reranker ordenando o resultado da busca híbrida | 0,707 | 0,775 | descartada |
| reranker contra a consulta principal (em vez do máximo) | 0,757 | 0,775 | descartada |
| sistema completo ordenado pelo reranker | 0,857 | 0,939 | descartada |

<!-- embeddings -->
| Modelo de embedding | P@10 | nDCG@10 | MRR |
|---|---|---|---|
| paraphrase-multilingual-MiniLM-L12-v2 | 0,704 | 0,713 | 0,739 |
| multilingual-e5-base | 0,711 | 0,735 | 0,796 |
| **bge-m3 (escolhido)** | 0,800 | 0,817 | 0,863 |

<!-- metadados -->
| 8 perguntas com recorte por metadado | Sem filtros | Com filtros (sistema final) |
|---|---|---|
| Conformidade ao recorte (top-10) | 42,5% | **91,2%** |
| P@10 (juiz vê os metadados) | 0,388 | **0,850** |

<!-- geracao -->
| Métrica | Resultado |
|---|---|
| Decisão responder x abster correta | 100,0% (40 de 40) |
| Abstenções corretas (fora de escopo + sem evidência) | 12 de 12 |
| Perguntas respondíveis recusadas indevidamente | 0 de 28 |
| Citações válidas (verificadas por código) | 100,0% de 635 |
| Fidelidade dos insights (juiz; sustentado = 1, parcial = 0,5) | 0,96 em 84 insights |
| Precisão do contexto enviado ao LLM | 91,0% |
| Extração correta dos filtros de metadado | 100% |
| AUC do reranker contra o juiz | 0,727 |

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

> As 15 avaliações recuperadas sustentam a conclusão de problemas recorrentes no prazo de entrega, apontando atrasos severos e não recebimento dos produtos [R1][R2][R3][R5]. Os clientes relatam descumprimento de prazos estabelecidos e falhas na comunicação por parte da loja [R5][R15].
>
> - **Descumprimento geral de prazos**: Os consumidores afirmam de forma recorrente que a loja falha em cumprir as datas estabelecidas para o recebimento das mercadorias [R2][R4][R5][R13]. *(apoio: 5 de 15 evidências)*
> - **Atrasos prolongados e falta de entrega**: Várias avaliações apontam que os produtos ultrapassam o prazo limite e demoram dias a mais para chegar ou simplesmente não são entregues [R1][R3][R6][R8]. *(apoio: 6 de 15 evidências)*
> - **Ausência de comunicação e satisfação**: Clientes criticam a falta de aviso prévio sobre os atrasos e a ausência de justificativas por parte da empresa sobre a demora [R5][R15]. *(apoio: 2 de 15 evidências)*
> - **Pedidos cancelados e não recebidos**: Há registros de produtos que continuam sem entrega até o momento da avaliação, resultando em insatisfação e pedidos cancelados [R7][R9][R11]. *(apoio: 3 de 15 evidências)*
>
> *Limitações: As constatações utilizam exclusivamente a amostra recuperada de 15 avaliações, sem permitir extrapolações para a base completa de 14445 comentários.*

| id | review_id | nota | texto do cliente |
|---|---|---|---|
| R1 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | Não cumpriu com o prazo e o produto não chegou. |
| R2 | `10467dc456e818c60bd750271b5d183e` | 1 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R3 | `48b3ce236ea9d35a4850ea94ca9ca38f` | 2 | Atraso. Produto não chegou no prazo |

<!-- aspectos -->
micro-F1 0,789 e macro-F1 0,744 em 600 rótulos de teste
