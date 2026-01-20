# CoworkingManager

Sistema de gestión para espacios de Coworking, construido con Flask y Vanilla CSS.

## Requisitos

- Python 3.8+
- SQLite (incluido en Python)

## Instalación

1.  Clonar el repositorio o descargar el código.
2.  Entrar en la carpeta del proyecto:
    ```bash
    cd CoworkingManager
    ```
3.  Instalar las dependencias:
    ```bash
    python -m pip install -r requirements.txt
    ```
    > **Nota**: Si tienes problemas con `pip`, asegúrate de usar `python -m pip` como se muestra arriba.

## Ejecución

Para iniciar la aplicación, ejecuta:

```bash
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5001`.

## Funcionalidades

- **Administrador**: Gestión de usuarios, registros y vistas de acceso.
- **Usuario**: Registro de entradas y salidas (Check-in/Check-out).

## Usuarios de Prueba (Generados automáticamente)

Si ejecutaste el script de verificación, el administrador es:
- **Usuario**: `AdminVerify`
- **Contraseña**: `admin`

También puedes intentar con:
- **Usuario**: `Admin`
- **Contraseña**: `admin`

## Usuarios de Prueba
- **Admin**: Puede crearse al inicio en `/admin/registro_inicial`.
## Despliegue en Render

Para desplegar este proyecto en [Render](https://render.com/):

1.  **Subir a GitHub**: Sube tu carpeta `CoworkingManager` a un repositorio de GitHub.
2.  **Crear Web Service**: En Render, selecciona "New" > "Web Service".
3.  **Conectar repositorio**: Vincula tu repositorio de GitHub.
4.  **Configuración**:
    - **Runtime**: `Python 3`
    - **Build Command**: `python -m pip install -r requirements.txt`
    - **Start Command**: `gunicorn "app:create_app()"`
5.  **Variables de Entorno**:
    - `SECRET_KEY`: Una cadena aleatoria para seguridad.
    - `DATABASE_URL`: Si usas PostgreSQL (opcional, por defecto usa SQLite en `instance/`).
