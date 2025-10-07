# DynamoDB FastAPI – Exercício do Curso AWS (LinuxTips)

Este repositório contém uma **API FastAPI** simples que interage com o **Amazon DynamoDB** para criar, consultar e excluir registros de *hosts* (par `name` + `ip`).  
Projeto elaborado como atividade do curso de AWS da **LinuxTips**.

> **Stack:** Python 3.12 · FastAPI · Boto3 · DynamoDB · Poetry · Ruff · Pytest

---

## Objetivos da atividade

- Subir uma API mínima com FastAPI.
- Criar e consultar itens em uma tabela DynamoDB.
- Exercitar o fluxo de **criar tabela**, **inserir item**, **consultar item** e **excluir item** via endpoints HTTP.
- Configurar ambiente local usando **Poetry** e boas práticas (lint/format/test).

---

## Estrutura dos arquivos (esperada)

```text
dynamodb/
├─ __init__.py           # (opcional)
├─ main.py               # App FastAPI e endpoints
├─ controllers.py        # Classes de acesso ao DynamoDB (Core/Manager)
pyproject.toml           # Configuração Poetry, tasks e deps
README.md
```

> Observação: o `main.py` importa de `dynamodb.controllers`. Garanta que os arquivos estejam dentro do diretório `dynamodb/` (pacote Python) ou ajuste o import conforme sua estrutura.

---

## Requisitos

- Python **3.12**
- Conta AWS (chaves com permissão de acesso ao DynamoDB)
- [Poetry](https://python-poetry.org/) instalado
- Opcional: Docker (se desejar containerizar)

### Credenciais AWS

Defina as credenciais via variáveis de ambiente ou `~/.aws/credentials`:
```bash
export AWS_ACCESS_KEY_ID="SEU_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="SEU_SECRET"
export AWS_DEFAULT_REGION="us-east-1"
```
> A região usada no código é **`us-east-1`**.

---

## Instalação e execução

1) Instale as dependências com Poetry:
```bash
poetry install
```

2) Ative o ambiente:
```bash
poetry shell
```

3) Rode o servidor de desenvolvimento (FastAPI):
```bash
# pela task configurada
poetry run task run
# ou diretamente (caso não use a task)
fastapi dev dynamodb/main.py
```

> O servidor sobe por padrão em `http://127.0.0.1:8000`. A documentação interativa estará em `http://127.0.0.1:8000/docs` (Swagger) e `http://127.0.0.1:8000/redoc`.

---

## Endpoints

### `GET /`
Retorna uma mensagem simples de saúde da API.

**Resposta:**
```json
{"message": "Hello, World!"}
```

---

### `POST /dynamo?hostname=<name>&ip=<ip>` – Criar item
- Verifica se a **tabela `hosts`** existe. Se **não** existir, **cria** a tabela com:
  - **Partition key (HASH):** `name` (String)
  - **Sort key (RANGE):** `ip` (String)
  - **Throughput:** 5 RCU / 5 WCU
- Insere um item com os atributos `name` e `ip`.

**Exemplo:**
```bash
curl -X POST "http://127.0.0.1:8000/dynamo?hostname=web-01&ip=10.0.0.5"
```
**Resposta (exemplo):**
```json
{"message": "Host created successfully!"}
```

> ⚠️ Nota: no código existe um `breakpoint()` antes da criação da tabela (modo debug). Se o servidor “pausar” na primeira chamada quando a tabela não existir, comente essa linha para ambientes não interativos.

---

### `GET /dynamo?hostname=<name>&ip=<ip>` – Consultar item
Busca um item (`name`, `ip`) na tabela `hosts` via `GetItem`.

**Exemplo:**
```bash
curl "http://127.0.0.1:8000/dynamo?hostname=web-01&ip=10.0.0.5"
```
**Resposta (exemplo Amazon SDK):**
```json
{
  "item": {
    "Item": {
      "name": {"S": "web-01"},
      "ip":   {"S": "10.0.0.5"}
    },
    "ResponseMetadata": { "...": "..." }
  }
}
```

---

### `DELETE /dynamo?hostname=<name>&ip=<ip>` – Excluir item **e** tabela
- Remove o item (`name`, `ip`).
- Em seguida **exclui a tabela `hosts`**.

**Exemplo:**
```bash
curl -X DELETE "http://127.0.0.1:8000/dynamo?hostname=web-01&ip=10.0.0.5"
```
**Resposta (exemplo):**
```json
{"message": "Host deleted successfully!"}
```

> ⚠️ Importante: este endpoint **apaga a tabela inteira** após excluir o item. Isso condiz com a proposta didática (criar/usar/apagar), mas **não é recomendado** em cenários reais.

---

## Implementação (resumo)

As classes principais estão em `controllers.py`:

- **`DynamoDBCore`** – Funções administrativas da tabela
  - `get_table()`: chama `describe_table` e retorna `True` caso exista, `None` se não existir.
  - `create_table()`: cria a tabela `hosts` com `name` (HASH) e `ip` (RANGE).  
  - `delete_table()`: exclui a tabela.
- **`DynamoDBManager`** – Operações de dados
  - `get_item(name, ip)`: obtém um item por chave composta.
  - `create_item(data)`: insere um item (`name`, `ip`).
  - `delete_item(data)`: remove um item (`name`, `ip`).

O app FastAPI (`main.py`) expõe os endpoints e orquestra as chamadas às classes acima.

---

## Tasks, Lint e Testes

No `pyproject.toml` há tasks úteis (via **taskipy**):

```toml
[tool.taskipy.tasks]
run = "fastapi dev dynamodb/main.py"
pre_test = "task lint"
test = "pytest -s -x --cov=dynamodb -vv"
post_test = "coverage html"
lint = "ruff check . ; ruff check . --diff"
format = "ruff check . --fix ; ruff format ."
```

- **Lint/Format:** `poetry run task format` (autofix + format)  
- **Testes:** `poetry run task test` (gera cobertura em `htmlcov/`)
- **Tipos Boto3:** `boto3-stubs` está configurado para alguns serviços (ec2, iam, route53, sts).

---

## Esquema da Tabela DynamoDB

- **Nome:** `hosts`
- **Chave primária composta:**
  - `name` – String (`S`) – **Partition key (HASH)**
  - `ip` – String (`S`) – **Sort key (RANGE)**
- **Provisioned Throughput:** 5 **RCU** / 5 **WCU**  
  > Para produção, considere **On-Demand** (Pay-Per-Request) ou ajuste de capacidade conforme uso.

---

## Exemplos rápidos com `httpie` (opcional)

```bash
http POST :8000/dynamo hostname==web-02 ip==10.0.0.9
http :8000/dynamo hostname==web-02 ip==10.0.0.9
http DELETE :8000/dynamo hostname==web-02 ip==10.0.0.9
```

---

## Boas práticas e próximos passos (sugestões)

- Trocar `ProvisionedThroughput` por **`BillingMode='PAY_PER_REQUEST'`** para simplicidade.
- Remover o `breakpoint()` do `POST /dynamo`.
- Tratar exceções do `ClientError` com respostas HTTP amigáveis (`HTTPException`).
- Validar entrada (`pydantic`/FastAPI) para `hostname`/`ip`.
- Adicionar **Dockerfile** e compose para rodar localmente (ou usar **LocalStack**).
- Adicionar **CI** (lint/test) com GitHub Actions.
- Criar testes de integração usando `moto` ou LocalStack.

---

## Créditos

- Atividade proposta no **curso de AWS da LinuxTips**.
- Autor do exercício: *Gabriel Cristian* (`pyproject.toml`).  
- Adaptações/README: você 🙂

---

## Licença

Use livremente para fins educacionais. Para produção, revise e ajuste as práticas recomendadas de segurança e escalabilidade.