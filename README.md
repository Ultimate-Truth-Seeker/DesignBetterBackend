# Sprint Scrum I - Proyecto - Ingeniería Software I - Backend

Este repositorio contiene el backend de la plataforma **Design Better**, una solución innovadora para el diseño y personalización de moda. La plataforma busca facilitar a diseñadores y clientes la creación, simulación y personalización de prendas, optimizando el flujo de trabajo y mejorando la experiencia de usuario. Desarrollado con Django e integrado con Docker, el sistema ofrece un entorno robusto, seguro y escalable para un desarrollo ágil.

---

## Documentación y Recursos

- **Historial de Versiones:**  
  [Historial de versiones y documentación](https://uvggt-my.sharepoint.com/:w:/g/personal/piv23574_uvg_edu_gt/EZJRR6nZmgVLvWhW3ljZVaABUmeDmoFEFqZ2tBmaSOk5ng?e=v5Vjpr)

- **Presentación de la Entrega:**  
  [Accede a la presentación en Canva](https://www.canva.com/design/DAGj6A2ls68/VbwZEe7RZ4ySxEQi0gXDhA/edit?utm_content=DAGj6A2ls68&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---

## Estructura del Repositorio

La siguiente estructura permite comprender rápidamente la organización del proyecto:

```
DesignBetterBackend/
├── docker-compose.yml         # Archivo principal de orquestación de contenedores
├── Dockerfile                 # Instrucciones para construir la imagen Docker de Django
├── src/                       # Código fuente del backend (apps, modelos, vistas, urls, etc.)
├── docs/                      # Documentación interna adicional
├── tests/                     # Pruebas automatizadas del backend
└── README.md                  # Instrucciones generales del proyecto
```

---

## Requisitos Previos

Antes de construir y ejecutar el proyecto, asegúrese de tener instalado lo siguiente:

- **Docker:** Versión 20.10 o superior.
- **Docker Compose:** Compatible con la versión de Docker instalada.
- **Git:** Para clonar el repositorio.
- Se recomienda configurar un archivo `.env` basado en el archivo `.env.example` si está disponible.

---

## Construcción y Ejecución del Proyecto con Docker

Siga estos pasos para construir y levantar el entorno del backend usando contenedores:

1. **Clonar el Repositorio:**  
   ```bash
   git clone https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend.git
   cd DesignBetterBackend
   ```

2. **Crear la Red de Docker (si no existe):**  
   ```bash
   docker network create devnetwork
   ```

3. **Construir y Levantar los Contenedores:**  
   ```bash
   docker compose up -d
   ```

Esto iniciará el contenedor del backend y cualquier otro servicio definido en `docker-compose.yml` (como base de datos, etc.).

---

## Administración de Contenedores

Para detener o eliminar los contenedores y recursos asociados, utilice los siguientes comandos:

### Detener los Contenedores
```bash
docker compose down
```

### Eliminar Contenedores, Imágenes y Volúmenes
```bash
docker compose down --rmi all --volumes --remove-orphans
```

---

## Otros Comandos Útiles

- **Ver Logs del Backend:**
  ```bash
  docker compose logs -f
  ```

- **Ejecutar Migraciones de Django:**
  ```bash
  docker compose exec web python manage.py migrate
  ```

- **Crear Superusuario (administrador):**
  ```bash
  docker compose exec web python manage.py createsuperuser
  ```

---

Este proyecto está diseñado para facilitar la colaboración en equipo mediante contenedores, asegurando entornos consistentes y facilidad de despliegue en distintos sistemas. Cualquier contribución o sugerencia puede registrarse en la sección de Issues del repositorio.
