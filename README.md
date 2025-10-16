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
