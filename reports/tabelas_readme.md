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
| **+ filtros de metadado, polaridade e reranker como porteiro (sistema final)** | 0,923 | 0,926 | 0,941 | 0,968 | 1,000 |

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
| Precisão do contexto enviado ao LLM | 92,3% |
| Extração correta dos filtros de metadado | 100% |
| AUC do reranker contra o juiz | 0,707 |

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

| id | review_id | nota | texto do cliente |
|---|---|---|---|
| R1 | `10467dc456e818c60bd750271b5d183e` | 1 | atraso na entrega da mercadoria,não cumpre prazo determinado. |
| R2 | `a4f9f285b2ed89a616d93dea024eb31b` | 1 | Não cumpriu com o prazo e o produto não chegou. |
| R3 | `48b3ce236ea9d35a4850ea94ca9ca38f` | 2 | Atraso. Produto não chegou no prazo |

<!-- aspectos -->
micro-F1 0,789 e macro-F1 0,744 em 600 rótulos de teste
