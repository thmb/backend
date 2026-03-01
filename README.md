# Backend API

FastAPI application with PostgreSQL, deployable to Kubernetes.

## Features

- **FastAPI** - Python web framework
- **SQLAlchemy** - ORM with PostgreSQL
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Kubernetes** - Terraform deployment

## Project Structure

```
backend/
├── fastapi/
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # API routes
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   ├── config.py      # Settings
│   ├── database.py    # DB connection
│   └── main.py        # FastAPI app
├── alembic/
│   ├── versions/      # Migration files
│   └── env.py         # Alembic config
├── alembic.ini        # Alembic settings
├── kubernetes.tf      # Terraform resources
└── Dockerfile
```

## Local Development

### Prerequisites

- Python 3.14+
- PostgreSQL
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with database credentials

# Run migrations
uv run alembic upgrade head

# Start server
uv run uvicorn fastapi.main:app --reload
```

## Database Migrations

```bash
# Apply all migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1

# Create new migration
uv run alembic revision -m "description"

# Auto-generate from model changes
uv run alembic revision --autogenerate -m "description"

# View current revision
uv run alembic current

# View migration history
uv run alembic history
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/products/` | Create product |
| GET | `/products/` | List products |
| GET | `/products/{id}` | Get product |
| PUT | `/products/{id}` | Update product |
| DELETE | `/products/{id}` | Delete product |
| GET | `/health` | Health check |
| GET | `/docs` | API documentation |

## Kubernetes Deployment

### Build & Push

```bash
docker build -t ghcr.io/thmb/backend:latest .
docker push ghcr.io/thmb/backend:latest
```

### Deploy

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit with your values

terraform init
terraform apply
```

### Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `kubernetes_namespace` | Namespace | `backend` |
| `image_repository` | Image repo | `ghcr.io/thmb/backend` |
| `image_tag` | Image tag | `latest` |
| `replicas` | Pod replicas | `1` |
| `ingress_host` | Ingress host | `api.localhost` |
| `database_host` | PostgreSQL host | - |
| `database_port` | PostgreSQL port | `5432` |
| `database_name` | Database name | - |
| `database_user` | Database user | - |
| `database_password` | Database password | - |

### Outputs

| Output | Description |
|--------|-------------|
| `ingress_url` | API URL |
| `docs_endpoint` | Swagger UI URL |
| `health_endpoint` | Health check URL |

## Monitoring

```bash
kubectl get pods -n backend
kubectl logs -n backend -l app=backend -f
```

## Cleanup

```bash
terraform destroy
```
