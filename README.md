# TCC API

 Este repositório contém a API do site TrustLink desenvolvida com FastAPI para o nosso TCC. Ela será responsável por gerenciar e fornecer os dados utilizados no sistema que estamos construindo.

## Como rodar o projeto

#### Clone o repositório

```bash
  git clone https://github.com/GuhLoyola/tcc-api.git
  cd tcc-api
```

#### Crie e ative o ambiente virtual

*Windows*

```bash
    python -m venv .venv
    .venv\Scripts\activate
```

*Linux*

```bash
    python -m venv .venv
    source .venv/bin/activate
```

Caso estiver utilizando *Git Bash*, substitua o **bin** por **Scripts** no comando acima.

#### Instale as dependências

```bash
    pip install -r requirements.txt
```

#### Crie um arquivo .env e adicione as variáveis ​​env necessárias a ele (o exemplo de variáveis ​​obrigatórias pode ser visto em .env.local):

```bash
    cp .env.local .env
```

#### Crie as tabelas no banco de dados

Antes de iniciar o servidor, execute o comando abaixo para criar as tabelas no banco de dados através do Alembic:

OBS: É necessário ter o banco criado no editor (PgAdmin, DBeaver, etc).

```bash
    alembic upgrade head
```

#### Treine o modelo de Machine Learning

Antes de iniciar a aplicação é necessário treinar o modelo de Machine Learning, para isso execute o código abaixo:

```bash
   python -m  ml.model.train_model
```

#### Rode a aplicação local

```bash
    fastapi dev main.py
```

### Tecnologias 🧰

- Python 3.11+

- FastAPI

- Alembic

- SQLAlchemy

- Uvicorn


### Status do projeto 🚧

Em desenvolvimento