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

A continuación se muestra la estructura principal del repositorio y una breve descripción de cada archivo o carpeta:

```
DesignBetterBackend/
├── backend_django/           # Aplicación principal de Django
├── designbetter/             # Configuración del proyecto Django (settings, urls, wsgi, etc.)
├── init_db/                  # Scripts de inicialización de base de datos
├── Dockerfile                # Instrucciones para construir la imagen Docker
├── docker-compose.yml        # Orquestación de contenedores (Django, base de datos, etc.)
├── manage.py                 # Script de administración de Django
├── requirements.txt          # Dependencias del proyecto
├── LICENSE                   # Licencia del proyecto
└── README.md                 # Documentación principal
```

---

## Requisitos Previos

Antes de construir y ejecutar el proyecto, asegúrese de tener instalado lo siguiente:

- **Docker:** Versión 20.10 o superior.
- **Docker Compose:** Compatible con la versión de Docker instalada.
- **Git:** Para clonar el repositorio.

> Nota: Puede ser necesario configurar un archivo `.env` si el sistema lo requiere.

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

Esto iniciará el contenedor del backend de Django y cualquier otro servicio definido en `docker-compose.yml`.

---

## Administración de Contenedores

### Detener los Contenedores
```bash
docker compose down
```

### Eliminar Contenedores, Imágenes y Volúmenes
```bash
docker compose down --rmi all --volumes --remove-orphans
```


---

## Notas Finales

Este proyecto está diseñado para facilitar la colaboración en equipo mediante contenedores, asegurando entornos consistentes y facilidad de despliegue. Para cualquier duda o contribución, utiliza la sección de Issues del repositorio.
