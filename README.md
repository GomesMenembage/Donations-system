# Donations System API

Sistema de gerenciamento de doações com autenticação JWT, perfis de doador/centro/admin, campanhas e notificações.

## Stack

- **FastAPI** — framework web
- **SQLAlchemy 2.0** — ORM
- **PostgreSQL** (produção) / **SQLite** (desenvolvimento)
- **JWT** — autenticação via `python-jose`
- **bcrypt + passlib** — hash de senhas
- **Alembic** — migrações de banco
- **Gunicorn + Uvicorn** — servidor ASGI

## Estrutura

```
app/
├── api/v1/          # Rotas (auth, donors, centers, admin)
├── models/          # Modelos SQLAlchemy
├── schemas/         # Schemas Pydantic
├── services/        # Lógica de negócio
├── utils/           # Segurança, notificações
├── config.py        # Settings via .env
├── database.py      # Engine e sessão
└── main.py          # App FastAPI
alembic/             # Migrations
scripts/             # Scripts de setup e start
```

## Quick Start

```bash
git clone <repo>
cd donations

# Criar ambiente e instalar dependências
./scripts/setup.sh

# Configurar variáveis de ambiente
cp .env.example .env

# Rodar em desenvolvimento
./scripts/start.sh
```

Acessar em `http://localhost:8000/docs` (Swagger UI).

## Configuração

Variáveis de ambiente (`.env`):

| Variável | Default | Descrição |
|---|---|---|
| `ENVIRONMENT` | `development` | `development` ou `production` |
| `DATABASE_URL` | `sqlite:///./donations.db` | Connection string |
| `SECRET_KEY` | — | Chave para JWT |
| `ALGORITHM` | `HS256` | Algoritmo JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Expiração do token |
| `HOST` | `0.0.0.0` | Host do servidor |
| `PORT` | `8000` | Porta do servidor |
| `CORS_ORIGINS` | `*` | Origens permitidas (`,` separado) |

Para PostgreSQL em produção:
```
DATABASE_URL=postgresql://usuario:senha@host:5432/donations
```

## Migrações (Alembic)

```bash
# Criar nova migration
alembic revision --autogenerate -m "descricao"

# Aplicar migrations
alembic upgrade head

# Reverter última
alembic downgrade -1
```

## API Endpoints

### Auth (`/api/auth`)

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | `/register` | Registrar usuário | — |
| POST | `/login` | Login (retorna JWT) | — |
| POST | `/password-reset-request` | Solicitar reset de senha | — |
| POST | `/password-reset` | Resetar senha com token | — |

**POST /api/auth/register**
```json
{ "name": "João", "email": "joao@email.com", "password": "123456", "role": "donor" }
```

**POST /api/auth/login**
```json
{ "email": "joao@email.com", "password": "123456" }
```
Resposta:
```json
{ "access_token": "eyJ...", "token_type": "bearer" }
```

### Donors (`/api/donors`)

Requer token Bearer + role `donor`.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/centers` | Listar centros aprovados |
| POST | `/donations` | Registrar doação |
| GET | `/donations` | Listar minhas doações |
| GET | `/notifications` | Listar notificações |
| PATCH | `/notifications/{id}/read` | Marcar notificação como lida |

### Centers (`/api/centers`)

Requer token Bearer + role `center`.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/me` | Perfil do centro |
| PATCH | `/me` | Atualizar perfil |
| POST | `/campaigns` | Criar campanha |
| GET | `/campaigns` | Listar campanhas |
| GET | `/donations` | Listar doações (filtro `?status=`) |
| PATCH | `/donations/{id}/confirm` | Confirmar doação |
| GET | `/stock` | Ver estoque |

### Admin (`/api/admin`)

Requer token Bearer + role `admin`.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/centers/pending` | Centros pendentes |
| PATCH | `/centers/{id}/approve` | Aprovar centro |
| PATCH | `/centers/{id}/reject` | Rejeitar centro |
| GET | `/users` | Listar usuários (`?role=`) |
| PATCH | `/users/{id}/suspend` | Suspender usuário |
| PATCH | `/users/{id}/reactivate` | Reativar usuário |
| DELETE | `/users/{id}` | Deletar usuário |
| GET | `/dashboard` | Estatísticas |
| POST | `/notifications/send` | Enviar notificação global |

### Health

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | `{"status":"ok", "environment":"..."}` |

## Modelos

### User
`users` — `id`, `name`, `email` (unique), `password_hash`, `location`, `role` (donor/center/admin), `status` (active/pending/suspended), `created_at`

### DonationCenter
`donation_centers` — `id`, `user_id`, `name`, `address`, `phone`, `schedule`, `status` (pending/approved/rejected), `created_at`

### Donation
`donations` — `id`, `donor_id`, `center_id`, `campaign_id?`, `type`, `quantity`, `date`, `status` (pending/confirmed), `created_at`

### Campaign
`campaigns` — `id`, `center_id`, `title`, `donation_type`, `goal`, `deadline`, `status` (active/inactive), `created_at`

### Stock
`stock` — `id`, `center_id`, `donation_type`, `quantity`, `updated_at`

### Notification
`notifications` — `id`, `user_id`, `title`, `body`, `read`, `created_at`

## Deploy no Render

1. Crie um PostgreSQL no Render e copie a Internal Database URL
2. Conecte seu repositório GitHub ao Render como Web Service
3. Configure:

   | Variável | Valor |
   |---|---|
   | `ENVIRONMENT` | `production` |
   | `DATABASE_URL` | Internal Database URL do PostgreSQL |
   | `SECRET_KEY` | string aleatória |
   | `CORS_ORIGINS` | URL do frontend |

4. **Build Command**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Start Command**:
   ```bash
   gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
   ```
6. **Pre-Deploy Command** (rodar migrations):
   ```bash
   alembic upgrade head
   ```
