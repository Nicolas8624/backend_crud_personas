# Backend CRUD Personas

API RESTful construida con **FastAPI** y **PostgreSQL (Supabase)** para la gestión de personas. Desarrollada como parte de la actividad del SENA "APP Gestión Personas".

## Requisitos Previos

- Python 3.9+
- Base de datos PostgreSQL (alojada en Supabase, Aiven u otro entorno)

## Configuración y Ejecución

Sigue estos pasos para levantar el entorno de desarrollo localmente:

### 1. Activar el entorno virtual

> **Nota:** Es indispensable activar el entorno virtual antes de ejecutar cualquier comando (`pip`, `python`, `uvicorn`) para utilizar los paquetes instalados en el proyecto.

```bash
# En Linux/Mac:
source venv/bin/activate   # o: source .venv/bin/activate

# En Windows:
venv\Scripts\activate
```

*(Si no has creado el entorno virtual previamente, créalo con `python -m venv .venv` y vuelve a activarlo).*

### 2. Instalar dependencias

Una vez activado el entorno virtual:

```bash
pip install -r requirements.txt
```

### 3. Configurar las variables de entorno (`.env`)

Crea o modifica el archivo `.env` en la raíz del proyecto con la URI de conexión a tu base de datos PostgreSQL:

```env
DATABASE_URL=postgresql://postgres.TU_PROYECTO:TU_CONTRASEÑA@aws-0-REGION.pooler.supabase.com:6543/postgres
```

> 💡 **Tip para Supabase:** Si experimentas errores de conexión o DNS (`could not translate host name`), utiliza la URL del **Connection Pooler IPv4** de Supabase en lugar del host directo (IPv6).

### 4. Poblar la base de datos con datos iniciales (Seed Data)

Ejecuta el siguiente script para crear automáticamente la tabla `persona` en la base de datos e insertar los registros de prueba iniciales:

```bash
python seed.py
```

### 5. Iniciar el servidor local

Arranca la API utilizando Uvicorn en el puerto 8000:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

También puedes ejecutarlo mediante:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

## Endpoints de la API

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/personas` | Obtener todas las personas |
| `GET` | `/api/personas/{identificacion}` | Obtener persona por número de identificación |
| `POST` | `/api/personas` | Crear una nueva persona |
| `PUT` | `/api/personas/{id}` | Actualizar datos de una persona por ID |
| `DELETE` | `/api/personas/{id}` | Eliminar una persona por ID |

---

## Documentación Interactiva

Una vez el servidor esté corriendo en `http://127.0.0.1:8000`, puedes acceder a:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
