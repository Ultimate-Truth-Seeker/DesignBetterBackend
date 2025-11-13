
<div  align="center">

  

# 🎨 DesignBetter Backend

  

### Backend robusto para la plataforma Design Better

  

[![Last Commit](https://img.shields.io/github/last-commit/Ultimate-Truth-Seeker/DesignBetterBackend?color=blue&label=last%20commit)](https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend)

[![Python](https://img.shields.io/badge/python-97.7%25-blue)](https://www.python.org/)

[![Languages](https://img.shields.io/github/languages/count/Ultimate-Truth-Seeker/DesignBetterBackend?color=brightgreen&label=languages)](https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend)

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

  

**[Documentación](https://designbetterbackend.onrender.com/admin/)** • **[Demo en Producción](https://designbetterbackend.onrender.com/)** • **[Reportar Bug](https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend/issues)**

  

</div>

  

---

  

## 📋 Tabla de Contenidos

  

- [Características](#-características)

- [Stack Tecnológico](#️-stack-tecnológico)

- [Inicio Rápido](#-inicio-rápido)

- [Instalación](#-instalación)

- [Configuración](#️-configuración)

- [Uso](#-uso)

- [Testing](#-testing)

- [Estructura del Proyecto](#️-estructura-del-proyecto)

- [API Endpoints](#-api-endpoints)

- [Contribuir](#-contribuir)

- [Licencia](#-licencia)

  

---

  

## ✨ Características

  

🔐 **Autenticación Robusta**

- Sistema de usuarios personalizado con Django

- JWT (JSON Web Tokens) para autenticación stateless

- Integración con django-allauth para login social (Google, Facebook, etc.)

- Tokens de acceso (30 min) y refresh (1 día)

  

🛍️ **Motor de E-commerce**

- Sistema completo de gestión de órdenes

- Motor de precios dinámico (`pricing_engine.py`)

- APIs REST para procesamiento de pedidos

  

🎯 **Recomendaciones Inteligentes**

- Base de datos vectorial con pgvector

- Sistema de recomendación de patrones/templates

- Búsqueda por similitud semántica

  

🐳 **Containerización**

- Completamente dockerizado

- Docker Compose para desarrollo local

- Red personalizada `devnetwork`

  

📧 **Sistema de Mensajería**

- Integración con Gmail SMTP

- App de mensajería interna

  

---

  

## 🛠️ Stack Tecnológico

  

<div  align="center">

  

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

![Django REST](https://img.shields.io/badge/Django_REST-ff1709?style=for-the-badge&logo=django&logoColor=white)

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)

  

</div>

  

### Dependencias Principales

  

-  **Django 4.x** - Framework web

-  **Django REST Framework** - APIs RESTful

-  **SimpleJWT** - Autenticación JWT

-  **django-allauth** - Autenticación social

-  **PostgreSQL + pgvector** - Base de datos con búsqueda vectorial

-  **NumPy** - Procesamiento numérico para recomendaciones

-  **Docker & Docker Compose** - Containerización

  

---

  

## 🚀 Inicio Rápido

  

```bash

# 1. Clonar el repositorio

git  clone  https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend.git

cd  DesignBetterBackend

  

# 2. Crear la red de Docker

docker  network  create  devnetwork

  

# 3. Iniciar servicios

docker  compose  up  --build

  

# 4. Acceder a la aplicación

# Backend API: http://localhost:8000

# Admin Panel: http://localhost:8000/admin/

```

  

¡Listo! El backend estará ejecutándose con migraciones y fixtures cargados automáticamente.

  

---

  

## 💾 Instalación

  

### Opción A: Con Docker (Recomendado)

  

**Prerequisitos:**

- Docker 20.x+

- Docker Compose 2.x+

- Git

  

**Pasos:**

  

```bash

# Crear red de Docker

docker  network  create  devnetwork

  

# Construir e iniciar contenedores

docker  compose  up  --build

```

  

El servicio backend:

- ✅ Ejecuta migraciones automáticamente

- ✅ Carga fixtures iniciales

- ✅ Inicia servidor en `0.0.0.0:8000`

  

**Servicios disponibles:**

- 🌐 Backend: `http://localhost:8000`

- 🗄️ PostgreSQL: `localhost:5434` (host) / `db:5432` (contenedor)

  

---

  

### Opción B: Instalación Local

  

**Prerequisitos:**

- Python 3.11+

- PostgreSQL 14+ con extensión pgvector

- pip y virtualenv

  

**Pasos:**

  

```bash

# 1. Crear entorno virtual

python  -m  venv  venv

source  venv/bin/activate  # En Windows: venv\Scripts\activate

  

# 2. Instalar dependencias

pip  install  -r  requirements.txt

  

# 3. Configurar variables de entorno (ver sección Configuración)

cp  .env.example  .env

# Editar .env con tus valores

  

# 4. Ejecutar migraciones

python  manage.py  makemigrations

python  manage.py  migrate

  

# 5. Cargar datos iniciales (opcional)

python  manage.py  shell < fixtures.py

  

# 6. Crear superusuario

python  manage.py  createsuperuser

  

# 7. Iniciar servidor

python  manage.py  runserver  0.0.0.0:8000

```

  

---

  

## ⚙️ Configuración

  

### Variables de Entorno

  

Crea un archivo `.env` en la raíz del proyecto:

  

| Variable | Descripción | Ejemplo | Requerido |

|----------|-------------|---------|-----------|

| `SECRET_KEY` | Clave secreta de Django | `your-secret-key-here` | ✅ |

| `DEBUG` | Modo debug (auto-detectado) | `True` / `False` | ⚠️ |

| `DATABASE_NAME` | Nombre de la BD (modo DEBUG) | `designbetter_db` | ✅ |

| `DATABASE_USER` | Usuario PostgreSQL | `postgres` | ✅ |

| `DATABASE_PASSWORD` | Contraseña PostgreSQL | `yourpassword` | ✅ |

| `DATABASE_HOST` | Host de la BD | `localhost` / `db` | ✅ |

| `DATABASE_PORT` | Puerto de PostgreSQL | `5432` | ✅ |

| `DB_URL` | URL completa (producción) | `postgresql://user:pass@host:port/db` | Producción |

| `EMAIL_HOST_DIR` | Email del remitente | `noreply@example.com` | ✅ |

| `EMAIL_HOST_PASSWORD` | Contraseña SMTP Gmail | `your-app-password` | ✅ |

| `FRONTEND_DOMAIN` | Dominio del frontend | `http://localhost:3000` | ⚠️ |

  

**Notas:**

-  `DEBUG` es `True` cuando `RENDER` no está configurado

- En producción, usa `DB_URL` en lugar de `DATABASE_*`

-  `FRONTEND_DOMAIN` por defecto: `http://localhost:3000` (dev) / `https://designbetter.vercel.app` (prod)

  

### Configuración de JWT

  

```python

# Token de acceso: 30 minutos

# Token de refresh: 1 día

# Algoritmo: HS256

```

  

### CORS y CSRF

  

- CORS habilitado para `FRONTEND_DOMAIN`

- Credenciales permitidas

- Cookies SameSite=None en producción

  

---

  

## 📖 Uso

  

### Panel de Administración

  

Accede al admin de Django:

  

```

URL: http://localhost:8000/admin/

Usuario: (creado con createsuperuser)

```

  

### Endpoints Principales

  

#### Autenticación (`/auth/`)

```bash

# Registro

POST  /auth/register/

  

# Login

POST  /auth/login/

  

# Refresh token

POST  /auth/token/refresh/

```

  

#### Autenticación Social (`/accounts/`)

```bash

# Login con Google, Facebook, etc.

GET  /accounts/google/login/

```

  

#### Órdenes (`/orders/`)

```bash

# Listar órdenes

GET  /orders/

  

# Crear orden

POST  /orders/

  

# Detalle de orden

GET  /orders/{id}/

```

  

#### Templates (`/templates/`)

```bash

# Listar templates

GET  /templates/

  

# Recomendaciones basadas en vectores

GET  /templates/recommendations/

```

  

### Archivos Media

  

En desarrollo, los archivos media se sirven desde:

```

http://localhost:8000/media/

```

  

---

  

## 🧪 Testing

  

### Ejecutar Tests

  

```bash

# Todos los tests

python  manage.py  test

  

# Tests de una app específica

python  manage.py  test  designbetter

python  manage.py  test  ecommerce

python  manage.py  test  patronaje

  

# Tests de integración

python  manage.py  test  backend_django.test_integration

```

  

### Estructura de Tests

  

```

designbetter/tests.py # Tests de autenticación y usuarios

ecommerce/tests.py # Tests del motor de e-commerce

patronaje/tests.py # Tests de templates y recomendaciones

backend_django/test_integration.py # Tests de integración

```

  

### Coverage (opcional)

  

```bash

pip  install  coverage

coverage  run  --source='.'  manage.py  test

coverage  report

coverage  html  # Genera reporte HTML en htmlcov/

```

  

---

  

## 🗂️ Estructura del Proyecto

  

```

DesignBetterBackend/

│

├── 📁 backend_django/ # Configuración principal

│ ├── settings.py # Configuración Django (env-driven)

│ ├── urls.py # Rutas principales

│ ├── wsgi.py / asgi.py # Entry points WSGI/ASGI

│ └── test_integration.py # Tests de integración

│

├── 📁 designbetter/ # App principal - Usuarios y Auth

│ ├── models.py # Modelo de usuario personalizado

│ ├── serializers.py # Serializers DRF

│ ├── views.py # Vistas de autenticación

│ ├── urls.py # Rutas de auth

│ ├── admin.py # Configuración admin

│ └── tests.py # Tests unitarios

│

├── 📁 ecommerce/ # Sistema de órdenes

│ ├── models.py # Modelos de Order, OrderItem

│ ├── serializers.py # Serializers de órdenes

│ ├── views.py # API de órdenes

│ ├── urls.py # Rutas de órdenes

│ ├── pricing_engine.py # Lógica de precios

│ └── tests.py # Tests de e-commerce

│

├── 📁 patronaje/ # Templates y Recomendaciones

│ ├── models.py # Modelos con campos vectoriales

│ ├── views.py # API de templates

│ ├── urls.py # Rutas de templates

│ ├── recomendation_utils.py # Algoritmos de recomendación

│ ├── tests.py # Tests de patronaje

│ ├── 📁 management/

│ │ └── 📁 commands/

│ │ └── backfill_vectors.py # Comando para poblar vectores

│ └── 📁 migrations/

│ └── pgvector setup

│

├── 📁 mensajeria/ # Sistema de mensajería

│ ├── models.py

│ ├── views.py

│ └── urls.py

│

├── 📁 templates/

│ └── 📁 admin/ # Templates personalizados del admin

│

├── 📁 media/ # Archivos subidos (gitignored)

├── 📁 static/ # Archivos estáticos

│

├── 🐳 docker-compose.yml # Orquestación de contenedores

├── 🐳 Dockerfile # Imagen Python 3.11-slim

├── 📦 requirements.txt # Dependencias Python

├── 🔧 manage.py # CLI de Django

├── 📋 fixtures.py # Datos iniciales

└── 📄 README.md # Esta documentación

```

  

---

  

## 🌐 API Endpoints

  

### Resumen de Rutas

  

| Categoría | Ruta Base | Descripción |

|-----------|-----------|-------------|

| Admin | `/admin/` | Panel de administración Django |

| Autenticación Custom | `/auth/` | Registro, login, JWT |

| Autenticación Social | `/accounts/` | django-allauth (Google, Facebook) |

| Órdenes | `/orders/` | CRUD de órdenes |

| Templates | `/templates/` | Gestión de patrones y recomendaciones |

| Media | `/media/` | Archivos estáticos subidos |

  

### Documentación Detallada

  

Para documentación completa de la API, considera integrar:

-  **Swagger/OpenAPI**: Agrega `drf-spectacular`

-  **Redoc**: UI alternativa para docs

  

```bash

# Instalar (opcional)

pip  install  drf-spectacular

  

# Acceder a docs

http://localhost:8000/api/schema/swagger-ui/

```

  

---

  

## 🏗️ Arquitectura

  

```

┌─────────────────┐

│ Frontend │ (Next.js/React en Vercel)

│ designbetter │

└────────┬────────┘

│ HTTPS/REST

▼

┌─────────────────┐

│ Django Backend │ (Este Repositorio)

│ + DRF + JWT │

└────────┬────────┘

│

┌────┴────┐

▼ ▼

┌─────────┐ ┌──────────┐

│PostgreSQL│ │ Gmail │

│+ pgvector│ │ SMTP │

└──────────┘ └──────────┘

```

  

**Flujo de Datos:**

1. Frontend envía peticiones REST con JWT

2. Django valida token y procesa request

3. PostgreSQL almacena datos + vectores para ML

4. Sistema de recomendación usa pgvector para búsqueda semántica

5. Notificaciones vía Gmail SMTP

  

---

  

## 🤝 Contribuir

  

¡Las contribuciones son bienvenidas! Sigue estos pasos:

  

### 1. Fork y Clone

  

```bash

git  clone  https://github.com/TU_USUARIO/DesignBetterBackend.git

cd  DesignBetterBackend

```

  

### 2. Crea una Rama

  

```bash

git  checkout  -b  feature/nueva-funcionalidad

```

  

### 3. Haz tus Cambios

  

- Escribe código limpio y documentado

- Agrega tests para nuevas funcionalidades

- Sigue PEP 8 para Python

- Actualiza documentación si es necesario

  

### 4. Ejecuta Tests

  

```bash

python  manage.py  test

```

  

### 5. Commit y Push

  

```bash

git  add  .

git  commit  -m  "✨ Agrega nueva funcionalidad X"

git  push  origin  feature/nueva-funcionalidad

```

  

### 6. Crea un Pull Request

  

Ve a GitHub y crea un PR describiendo tus cambios.

  

### Guías de Estilo

  

-  **Python**: PEP 8

-  **Commits**: [Conventional Commits](https://www.conventionalcommits.org/)

-  **Branches**: `feature/`, `bugfix/`, `hotfix/`

  

---

  

## 📄 Licencia

  

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

  

```

MIT License

  

Copyright (c) 2025 DesignBetter Team

  

Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files...

```

  

---

  

## 👥 Autores

  

-  **Ultimate Truth Seeker** - [GitHub](https://github.com/Ultimate-Truth-Seeker)

  

---

  

## 🙏 Agradecimientos

  

- Django y Django REST Framework community

- PostgreSQL y pgvector maintainers

- Todos los colaboradores del proyecto

  

---

  

## 📞 Soporte

  

- 🐛 **Issues**: [GitHub Issues](https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend/issues)

- 📧 **Email**: support@designbetter.com

- 💬 **Discussions**: [GitHub Discussions](https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend/discussions)

  

---

  

## 🔗 Enlaces Útiles

  

- [Documentación de Django](https://docs.djangoproject.com/)

- [Django REST Framework](https://www.django-rest-framework.org/)

- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)

- [Docker Docs](https://docs.docker.com/)

  

---

  

<div  align="center">

  

**⭐ Si este proyecto te resultó útil, considera darle una estrella en GitHub ⭐**


  

</div>