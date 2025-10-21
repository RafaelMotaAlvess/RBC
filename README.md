# RBC


# Instalar as dependencias do projeto: 

```sh
uv sync
```
# Executar:

```sh
uv run main.py
```

# Caso não esteja funcionando o interpreter:

* ```CTRL+SHIFT+P```
* Busque por “Python: Select Interpreter”.
* escolha o interpreter da `.venv/`

### 🧱 UV TIPS

Criação e gerenciamento de projetos Python — ou seja, aqueles que possuem um arquivo `pyproject.toml`.

- **`uv init`** — Cria um novo projeto Python.  
- **`uv add`** — Adiciona uma dependência ao projeto.  
- **`uv remove`** — Remove uma dependência do projeto.  
- **`uv sync`** — Sincroniza as dependências do projeto com o ambiente.  
- **`uv lock`** — Gera o arquivo de bloqueio (`uv.lock`) com as versões exatas das dependências.  
- **`uv run`** — Executa um comando dentro do ambiente do projeto.  
- **`uv tree`** — Exibe a árvore de dependências do projeto.  
- **`uv build`** — Compila o projeto em arquivos de distribuição (ex: `.whl`, `.tar.gz`).  
- **`uv publish`** — Publica o projeto em um índice de pacotes (como o PyPI).



## Atributos e Pesos do Sistema RBC (Artrite)

| Atributo | Valores possíveis | Significado clínico | Peso sugerido |
|-----------|------------------|----------------------|----------------|
| **DL (Dor Localizada)** | sim, não | Indica presença de dor articular. É um dos primeiros sintomas de artrite, mas não é específico, pois pode ocorrer em outras doenças musculoesqueléticas. | **0.7** |

| **RC (Rigidez Corporal / Rigidez Matinal)** | sim, não | A rigidez matinal é característica de artrite reumatoide e inflamatória. Alta relevância diagnóstica. | **0.8** |

| **DC (Deformidade Crônica)** | sim, não | Indica dano articular irreversível e crônico. Altamente indicativo de estágios avançados de artrite. | **0.9** |

| **Mob (Mobilidade)** | limitado, normal | Mede a capacidade funcional do paciente. Mobilidade limitada indica perda funcional associada à inflamação e rigidez. | **0.85** |

| **DTS (Duração dos Sintomas)** | curta, moderada, prolongada, ausente | Indica há quanto tempo os sintomas persistem. Casos mais duradouros indicam cronicidade e importância clínica maior. | **0.6** |

| **IL (Inflamação Local)** | ausente, leve, moderado, importante, muito_importante, não | Grau de inflamação nas articulações. Quanto mais severa a inflamação, maior a probabilidade de artrite inflamatória ativa. | **0.95** |

| **ER (Erosão Óssea)** | ausente, leve, moderado, importante, muito_importante, não | Presença de erosão óssea em exames de imagem indica destruição articular — marcador de dano irreversível e diagnóstico de artrite reumatoide. | **1.0** |

| **TCSE (Tempo de Comprometimento Sintomático / Evolução Clínica)** | não, moderado, importante, sim | Mede a duração e gravidade do comprometimento clínico geral. Casos mais longos ou importantes indicam cronicidade. | **0.7** |

| **ART (Artrite / Articulações Acometidas)** | sim, não | Indica se há inflamação articular ativa. Fundamental no diagnóstico de artrite, mas presente em vários tipos. | **0.8** |

| **RM (Remissão Clínica)** | sim, não | Indica se o paciente apresenta melhora clínica. Valor diagnóstico inverso — presença de remissão indica resposta terapêutica. | **0.6** |

| **Bur (Bursite)** | sim, não | Inflamação das bursas (sacos sinoviais). Pode coexistir com artrite, mas não é determinante. | **0.5** |

| **Tof (Tofos / Depósitos de Ácido Úrico)** | sim, não | Depósitos subcutâneos de cristais de ácido úrico, típicos da gota — útil para diferenciar artrite reumatoide de gota. | **0.5** |

| **Sin (Sinovite)** | sim, não | Inflamação da membrana sinovial. Achado clínico essencial na artrite inflamatória. | **0.9** |

| **ATG (Antígeno / Marcador Genético)** | sim, não | Indica presença de antígenos como HLA-B27. Útil para diferenciar espondiloartrites e artrites soronegativas. | **0.7** |

| **NR (Número de Regiões / Articulações Acometidas)** | baixo, moderado, alto | Mede o número de articulações envolvidas. Quanto mais regiões, mais severa a doença. | **0.8** |

| **HLA-B27** | 0, 0.5, 1, não | Marcador genético associado a espondiloartrites. O valor maior representa maior predisposição genética. | **0.7** |


## Explicação dos Pesos

Os pesos foram definidos com base em importância diagnóstica e valor discriminativo clínico:

Peso 1.0 – Muito Alto → Indicadores estruturais ou patognomônicos (como erosão óssea).

Peso 0.9 – Alto → Marcadores inflamatórios diretos e clínicos importantes (ex: sinovite, deformidade).

Peso 0.8 – Moderado-Alto → Sinais clínicos relevantes, mas menos específicos (ex: rigidez, artrite ativa).

Peso 0.6–0.7 – Médio → Variáveis de apoio, com correlação clínica útil mas indireta (ex: dor, remissão, TCSE).

Peso 0.5 – Baixo → Indicadores auxiliares ou diferenciais (ex: bursite, tofos).