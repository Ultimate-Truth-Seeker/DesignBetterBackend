<div align="center">

# DesignBetter Backend

### Robust backend for the Design Better platform

[![Last Commit](https://img.shields.io/github/last-commit/Ultimate-Truth-Seeker/DesignBetterBackend?color=blue&label=last%20commit)](https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend)
[![Python](https://img.shields.io/badge/python-97.7%25-blue)](https://www.python.org/)
[![Languages](https://img.shields.io/github/languages/count/Ultimate-Truth-Seeker/DesignBetterBackend?color=brightgreen&label=languages)](https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**[Documentation](https://designbetterbackend.onrender.com/admin/)** • **[Production Demo](https://designbetterbackend.onrender.com/)** • **[Report Bug](https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend/issues)**

</div>

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## Features

**Robust Authentication**
- Custom user system with Django
- JWT (JSON Web Tokens) for stateless authentication
- Integration with django-allauth for social login (Google, Facebook, etc.)
- Access tokens (30 min) and refresh tokens (1 day)

**E-commerce Engine**
- Complete order management system
- Dynamic pricing engine (`pricing_engine.py`)
- REST APIs for order processing

**Intelligent Recommendations**
- Vector database with pgvector
- Pattern/template recommendation system
- Semantic similarity search

**Containerization**
- Fully dockerized
- Docker Compose for local development
- Custom `devnetwork` network

**Messaging System**
- Gmail SMTP integration
- Internal messaging app

---

## Tech Stack

<div align="center">

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)

</div>

### Main Dependencies

- **Django 4.x** - Web framework
- **Django REST Framework** - RESTful APIs
- **SimpleJWT** - JWT authentication
- **django-allauth** - Social authentication
- **PostgreSQL + pgvector** - Database with vector search
- **NumPy** - Numerical processing for recommendations
- **Docker & Docker Compose** - Containerization

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend.git
cd DesignBetterBackend

# 2. Create Docker network
docker network create devnetwork

# 3. Start services
docker compose up --build

# 4. Access the application
# Backend API: http://localhost:8000
# Admin Panel: http://localhost:8000/admin/
```

Ready! The backend will be running with migrations and fixtures loaded automatically.

---

## Installation

### Option A: With Docker (Recommended)

**Prerequisites:**
- Docker 20.x+
- Docker Compose 2.x+
- Git

**Steps:**

```bash
# Create Docker network
docker network create devnetwork

# Build and start containers
docker compose up --build
```

The backend service:
- Runs migrations automatically
- Loads initial fixtures
- Starts server on `0.0.0.0:8000`

**Available services:**
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5434` (host) / `db:5432` (container)

---

### Option B: Local Installation

**Prerequisites:**
- Python 3.11+
- PostgreSQL 14+ with pgvector extension
- pip and virtualenv

**Steps:**

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables (see Configuration section)
cp .env.example .env
# Edit .env with your values

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Load initial data (optional)
python manage.py shell < fixtures.py

# 6. Create superuser
python manage.py createsuperuser

# 7. Start server
python manage.py runserver 0.0.0.0:8000
```

---

## Configuration

### Environment Variables

Create a `.env` file at the project root:

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | `your-secret-key-here` | Yes |
| `DEBUG` | Debug mode (auto-detected) | `True` / `False` | Warning |
| `DATABASE_NAME` | DB name (DEBUG mode) | `designbetter_db` | Yes |
| `DATABASE_USER` | PostgreSQL user | `postgres` | Yes |
| `DATABASE_PASSWORD` | PostgreSQL password | `yourpassword` | Yes |
| `DATABASE_HOST` | DB host | `localhost` / `db` | Yes |
| `DATABASE_PORT` | PostgreSQL port | `5432` | Yes |
| `DB_URL` | Complete URL (production) | `postgresql://user:pass@host:port/db` | Production |
| `EMAIL_HOST_DIR` | Sender email | `noreply@example.com` | Yes |
| `EMAIL_HOST_PASSWORD` | Gmail SMTP password | `your-app-password` | Yes |
| `FRONTEND_DOMAIN` | Frontend domain | `http://localhost:3000` | Warning |

**Notes:**
- `DEBUG` is `True` when `RENDER` is not configured
- In production, use `DB_URL` instead of `DATABASE_*`
- `FRONTEND_DOMAIN` defaults to: `http://localhost:3000` (dev) / `https://designbetter.vercel.app` (prod)

### JWT Configuration

```python
# Access token: 30 minutes
# Refresh token: 1 day
# Algorithm: HS256
```

### CORS and CSRF

- CORS enabled for `FRONTEND_DOMAIN`
- Credentials allowed
- SameSite=None cookies in production

---

## Usage

### Admin Panel

Access Django admin:

```
URL: http://localhost:8000/admin/
User: (created with createsuperuser)
```

### Main Endpoints

#### Authentication (`/auth/`)
```bash
# Registration
POST /auth/register/

# Login
POST /auth/login/

# Refresh token
POST /auth/token/refresh/
```

#### Social Authentication (`/accounts/`)
```bash
# Login with Google, Facebook, etc.
GET /accounts/google/login/
```

#### Orders (`/orders/`)
```bash
# List orders
GET /orders/

# Create order
POST /orders/

# Order detail
GET /orders/{id}/
```

#### Templates (`/templates/`)
```bash
# List templates
GET /templates/

# Vector-based recommendations
GET /templates/recommendations/
```

### Media Files

In development, media files are served from:
```
http://localhost:8000/media/
```

---

## Testing

### Run Tests

```bash
# All tests
python manage.py test

# Tests for a specific app
python manage.py test designbetter
python manage.py test ecommerce
python manage.py test patronaje

# Integration tests
python manage.py test backend_django.test_integration
```

### Test Structure

```
designbetter/tests.py    # Authentication and user tests
ecommerce/tests.py       # E-commerce engine tests
patronaje/tests.py       # Template and recommendation tests
backend_django/test_integration.py  # Integration tests
```

### Coverage (optional)

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML report in htmlcov/
```

---

## Project Structure

```
DesignBetterBackend/
│
├── backend_django/             # Main configuration
│   ├── settings.py             # Django config (env-driven)
│   ├── urls.py                 # Main routes
│   ├── wsgi.py / asgi.py       # WSGI/ASGI entry points
│   └── test_integration.py     # Integration tests
│
├── designbetter/               # Main app - Users and Auth
│   ├── models.py               # Custom user model
│   ├── serializers.py          # DRF serializers
│   ├── views.py                # Authentication views
│   ├── urls.py                 # Auth routes
│   ├── admin.py                # Admin configuration
│   └── tests.py                # Unit tests
│
├── ecommerce/                  # Order system
│   ├── models.py               # Order, OrderItem models
│   ├── serializers.py          # Order serializers
│   ├── views.py                # Order API
│   ├── urls.py                 # Order routes
│   ├── pricing_engine.py       # Pricing logic
│   └── tests.py                # E-commerce tests
│
├── patronaje/                  # Templates and Recommendations
│   ├── models.py               # Models with vector fields
│   ├── views.py                # Template API
│   ├── urls.py                 # Template routes
│   ├── recomendation_utils.py  # Recommendation algorithms
│   ├── tests.py                # Pattern tests
│   ├── management/
│   │   └── commands/
│   │       └── backfill_vectors.py  # Command to populate vectors
│   └── migrations/
│       └── pgvector setup
│
├── mensajeria/                 # Messaging system
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── templates/
│   └── admin/                  # Custom admin templates
│
├── media/                      # Uploaded files (gitignored)
├── static/                     # Static files
│
├── docker-compose.yml          # Container orchestration
├── Dockerfile                  # Python 3.11-slim image
├── requirements.txt            # Python dependencies
├── manage.py                   # Django CLI
├── fixtures.py                 # Initial data
└── README.md                   # This documentation
```

---

## API Endpoints

### Route Summary

| Category | Base Route | Description |
|----------|------------|-------------|
| Admin | `/admin/` | Django admin panel |
| Custom Auth | `/auth/` | Registration, login, JWT |
| Social Auth | `/accounts/` | django-allauth (Google, Facebook) |
| Orders | `/orders/` | Order CRUD |
| Templates | `/templates/` | Pattern and recommendation management |
| Media | `/media/` | Uploaded static files |

### Detailed Documentation

For complete API documentation, consider integrating:
- **Swagger/OpenAPI**: Add `drf-spectacular`
- **Redoc**: Alternative docs UI

```bash
# Install (optional)
pip install drf-spectacular

# Access docs
http://localhost:8000/api/schema/swagger-ui/
```

---

## Architecture

```
┌─────────────────┐
│   Frontend      │ (Next.js/React on Vercel)
│  designbetter   │
└────────┬────────┘
         │ HTTPS/REST
         ▼
┌─────────────────┐
│  Django Backend │ (This Repository)
│   + DRF + JWT   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────┐
│PostgreSQL│ │  Gmail   │
│+ pgvector│ │  SMTP    │
└──────────┘ └──────────┘
```

**Data Flow:**
1. Frontend sends REST requests with JWT
2. Django validates token and processes request
3. PostgreSQL stores data + vectors for ML
4. Recommendation system uses pgvector for semantic search
5. Notifications via Gmail SMTP

---

## Contributing

Contributions are welcome! Follow these steps:

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/DesignBetterBackend.git
cd DesignBetterBackend
```

### 2. Create a Branch

```bash
git checkout -b feature/new-feature
```

### 3. Make Your Changes

- Write clean and documented code
- Add tests for new features
- Follow PEP 8 for Python
- Update documentation if needed

### 4. Run Tests

```bash
python manage.py test
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: add new feature X"
git push origin feature/new-feature
```

### 6. Create a Pull Request

Go to GitHub and create a PR describing your changes.

### Style Guidelines

- **Python**: PEP 8
- **Commits**: [Conventional Commits](https://www.conventionalcommits.org/)
- **Branches**: `feature/`, `bugfix/`, `hotfix/`

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 DesignBetter Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...
```

---

## Authors

- Pablo Méndez
- Roberto Nájera
- Luis Palacios
- André Pivaral

---

## Acknowledgments

- Django and Django REST Framework community
- PostgreSQL and pgvector maintainers
- All project contributors

---

## Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)
- [Docker Docs](https://docs.docker.com/)

---

<div align="center">

**If you found this project useful, consider giving it a star on GitHub**

Made with love by the DesignBetter team

</div>