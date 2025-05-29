# API de Gerenciamento de Lanches

API REST desenvolvida com FastAPI para gerenciamento de usuários e produtos.

## 🚀 Tecnologias Utilizadas

- Python 3.13
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- JWT (Autenticação)
- Pydantic (Validação de dados)
- Passlib (Criptografia de senhas)
- Bcrypt (Hash de senhas)

## 📋 Pré-requisitos

- Python 3.13 ou superior
- PostgreSQL
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd Lanches
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
.venv\Scripts\activate
```
- Linux/Mac:
```bash
source .venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/database_name
JWT_SECRET=seu_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🏃‍♂️ Executando o Projeto

1. Inicie o servidor:
```bash
uvicorn main:app --reload
```

2. Acesse a documentação da API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📚 Endpoints da API

### Usuários

- `POST /api/v1/users/create_user` - Criar novo usuário
- `GET /api/v1/users/get_users` - Listar todos os usuários
- `GET /api/v1/users/get_user_by_id/{user_id}` - Buscar usuário por ID
- `PUT /api/v1/users/update_user/{user_id}` - Atualizar usuário
- `DELETE /api/v1/users/delete_user/{user_id}` - Deletar usuário
- `POST /api/v1/users/login` - Login de usuário
- `GET /api/v1/users/check_user` - Verificar usuário autenticado

### Produtos

- `POST /api/v1/products/create_product` - Criar novo produto
- `GET /api/v1/products/get_products` - Listar todos os produtos
- `GET /api/v1/products/get_product_by_id/{product_id}` - Buscar produto por ID
- `PUT /api/v1/products/update_product/{product_id}` - Atualizar produto
- `DELETE /api/v1/products/delete_product/{product_id}` - Deletar produto

## 🔐 Autenticação

A API utiliza autenticação JWT (JSON Web Token). Para acessar endpoints protegidos:

1. Faça login usando o endpoint `/api/v1/users/login`
2. Use o token retornado no header das requisições:
```
Authorization: Bearer seu_token_jwt
```

## 📦 Estrutura do Projeto

```
├── api/
│   ├── v1/
│   │   ├── user.py
│   │   └── product.py
│   └── api.py
├── core/
│   ├── configs.py
│   └── deps.py
├── models/
│   ├── users.py
│   ├── products.py
│   └── __all_models.py
├── schemas/
│   ├── user_schema.py
│   └── product_schema.py
├── security/
│   ├── auth.py
│   └── security.py
├── .env
├── main.py
├── requirements.txt
└── README.md
```

## 🔄 Fluxo de Dados

1. **Criação de Usuário**:
   - Recebe dados via `UserSchemaCreate`
   - Valida dados com Pydantic
   - Criptografa senha
   - Salva no banco
   - Retorna usuário criado

2. **Autenticação**:
   - Recebe email/senha
   - Verifica credenciais
   - Gera token JWT
   - Retorna token

3. **Operações com Produtos**:
   - Valida token JWT
   - Verifica permissões
   - Executa operação
   - Retorna resultado

## 🔒 Segurança

- Senhas criptografadas com bcrypt
- Autenticação JWT
- Validação de dados com Pydantic
- Proteção contra SQL Injection (SQLAlchemy)
- Headers de segurança configurados

