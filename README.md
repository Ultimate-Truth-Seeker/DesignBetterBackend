# Sprint Scrum I - Proyecto - Ingeniería Software I - Frontend

Este repositorio contiene el backend de la plataforma **Design Better**, una solución innovadora para el diseño y personalización de moda. La plataforma facilita a diseñadores y clientes la creación, simulación y personalización de prendas, optimizando el flujo de trabajo y mejorando la experiencia de usuario. Desarrollado con Django e integrado con Docker, el sistema ofrece un entorno robusto, seguro y escalable para el desarrollo ágil.

---

## Documentación y Recursos

- **Historial de Versiones:**  
  [Historial de versiones y documentación](https://uvggt-my.sharepoint.com/:w:/g/personal/piv23574_uvg_edu_gt/EZJRR6nZmgVLvWhW3ljZVaABUmeDmoFEFqZ2tBmaSOk5ng?e=v5Vjpr)

- **Presentación de la Entrega:**  
  [Accede a la presentación en Canva](https://www.canva.com/design/DAGj6A2ls68/VbwZEe7RZ4ySxEQi0gXDhA/edit?utm_content=DAGj6A2ls68&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---

## Estructura del Repositorio

La organización del repositorio es la siguiente, lo que facilita la rápida identificación de los distintos componentes del proyecto:

```
DesignBetterBackend/
├── docker-compose.yml         # Configuración de Docker Compose para levantar los contenedores
├── Dockerfile                 # Instrucciones para construir la imagen Docker del backend
├── src/                       # Código fuente del backend (aplicaciones, modelos, vistas, etc.)
├── docs/                      # Documentación adicional (manuales, historial de versiones, etc.)
├── tests/                     # Pruebas unitarias y de integración
└── README.md                  # Documentación general, instrucciones y estructura del proyecto
```

---

## Requisitos Previos

Antes de construir y ejecutar el proyecto, asegúrese de tener instalado lo siguiente:

- **Docker:** Versión 20.10 o superior.
- **Docker Compose:** Asegúrese de contar con la versión compatible con su instalación de Docker.
- **Git:** Para clonar el repositorio.
- Otros requisitos que se deban configurar en archivos de entorno o configuraciones específicas del proyecto (ver sección de Configuración).

---

## Configuración del Proyecto

- **Variables de Entorno:**  
  Algunos parámetros y variables de configuración (como la conexión a la base de datos, claves secretas, etc.) se administran mediante archivos de configuración o variables de entorno. Verifique el archivo `.env.example` (o documentación interna) para realizar los ajustes necesarios para su entorno de desarrollo o producción.

---

## Construcción y Ejecución con Contenedores Docker

Siga estos pasos para construir y ejecutar los contenedores Docker del proyecto:

1. **Clonar el Repositorio:**  
   Abra la terminal y ejecute:
   ```bash
   git clone https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend.git
   cd DesignBetterBackend
   ```

2. **Crear la Red de Docker:**  
   Desde la terminal, ejecute:
   ```bash
   docker network create devnetwork
   ```

3. **Construir y Levantar los Contenedores:**  
   En la carpeta del backend del proyecto, ejecute:
   ```bash
   docker compose up -d
   ```

---

## Gestión de Contenedores

Para facilitar la administración de los contenedores Docker, utilice los siguientes comandos:

### Detener los Contenedores
```bash
docker compose down
```

### Eliminar Contenedores, Imágenes y Volúmenes
```bash
docker compose down --rmi all --volumes --remove-orphans
```

---

## Notas Adicionales

- **Logs y Depuración:**  
  Para visualizar los logs de los contenedores, utilice:
  ```bash
  docker compose logs -f
  ```
- **Documentación Interna:**  
  Revise la carpeta `/docs` para obtener información más detallada sobre la configuración, dependencias y otros aspectos relevantes del proyecto.

---

Con esta estructura y documentación, se busca facilitar el desarrollo, despliegue y mantenimiento del proyecto, asegurando claridad y un flujo de trabajo eficiente para todos los colaboradores.
```
