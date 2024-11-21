# Claims API

Claims API es un sistema diseñado para la gestión de reclamos, permitiendo que los usuarios interactúen con la plataforma y que los diferentes roles gestionen los reclamos según sus permisos.

## Roles del Sistema

1. **Usuario:** Puede crear y consultar sus propios reclamos.
2. **Empleado:** A implementar.
3. **Jefe:** A implementar.
4. **Administrador:** Control total sobre usuarios y reclamos.

## Instalación

1. Clona el repositorio:
   ```bash
    git clone https://github.com/nicolasrodriguez3/fastapi-itu.git
    cd fastapi-itu
    ```

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Configura las variables de entorno necesarias. Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

    ```env
    # App
    PORT=8000
    DEV=True

    # Logs
    DEBUG=False

    # Database
    DB_CONN=postgresql://{user}:{password}@{host}:{port}/{db_name}

    # JWT
    JWT_SECRET_KEY="supersecretstring"
    JWT_ALGORITHM="HS256"
    JWT_EXPIRATION_TIME_MINUTES=60
    ```
Reemplaza {user}, {password}, {host}, {port}, y {db_name} con los valores correspondientes a tu base de datos PostgreSQL.

4. Ejecuta la aplicación
    ```bash
    python main.py
    ```

## Uso
### Endpoints principales
- **/users:** Gestión de usuarios.
- **/claims:** Creación y manejo de reclamos.
- **/auth:** Registrarse e iniciar sesión.

### Autenticación
Se utiliza JWT para manejar la autenticación y los permisos. Los tokens deben enviarse en el header Authorization como ```Bearer <token>```.

## Características
- Manejo de roles y permisos.
- Registro detallado de logs para depuración.
- Protección de rutas sensibles.
- Middleware para captura de errores y validación de acceso.

## Logs
Los logs se almacenan en ./logs y se rotan diariamente. El nivel de log puede configurarse según el entorno.

## Agradecimientos
Una mención especial para nuestro profesor, [Juan Panasiti](https://github.com/juanpanasiti), que puso lo mejor de sí en cada clase. Se nota la pasión y dedicación para enseñar y su amor por la programación. ¡Muchas gracias profe!