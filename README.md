# Sprint Scrum I - Proyecto - Ingeniería Software I - Backend

Este repositorio contiene el backend de la plataforma **Design Better**, una solución innovadora para el diseño y personalización de moda. La plataforma busca facilitar a diseñadores y clientes la creación, simulación y personalización de prendas; optimizando el flujo de trabajo y mejorando la experiencia de usuario. Desarrollado con Django, e integrándose con Docker, el sistema ofrece un entorno robusto, seguro y escalable para un desarrollo ágil.

## Documentación - Historial Versiones

El historial de versiones del documento se encuentra en el siguiente enlace:  
https://uvggt-my.sharepoint.com/:w:/g/personal/piv23574_uvg_edu_gt/EZJRR6nZmgVLvWhW3ljZVaABUmeDmoFEFqZ2tBmaSOk5ng?e=v5Vjpr

La presentación correspondiente a esta entrega se encuentra en el siguiente enlace:  
https://www.canva.com/design/DAGj6A2ls68/VbwZEe7RZ4ySxEQi0gXDhA/edit?utm_content=DAGj6A2ls68&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Contenedores - Construcción y Ejecución

Por favor, siga los siguientes pasos para construir y ejecutar los contenedores Docker correspondientes al proyecto:

1. **Clonar el repositorio**  
   Abra la terminal y clone el repositorio:
   ```cmd
   git clone https://github.com/Ultimate-Truth-Seeker/DesignBetterBackend.git
   cd DesignBetterBackend

2. **Crear la red de Docker**  
   Desde la terminal ejecute:
   ```cmd
   docker network create devnetwork

3. **Construir y levantar los contenedores**  
   En la carpeta del backend del proyecto ejecute:
   ```cmd
   docker compose up -d

## Contenedores - Detención y Eliminación

Por favor, utilice los siguientes comandos para facilitar la gestión de los contenedores Docker correspondientes al proyecto:

1. **Detener los contenedores**  
   En la terminal ejecute:
   ```cmd
   docker compose down

2. **Eliminar contenedores, imágenes y volúmenes**  
   Ejecute:
   ```cmd
   docker compose down --rmi all --volumes --remove-orphans
