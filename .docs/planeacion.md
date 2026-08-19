# Planeación y Arquitectura del Backend

## 1. Arquitectura del Proyecto
El proyecto se desarrollará utilizando una arquitectura de N-capas (N-Tier Architecture), promoviendo la separación de responsabilidades y facilitando el mantenimiento y escalabilidad.

Las capas principales serán:
- **Routers (Controladores):** Manejan las peticiones HTTP y las respuestas.
- **Servicios:** Contienen la lógica de negocio.
- **Repositorios:** Capa de acceso a datos (interacción con SQLAlchemy).
- **Modelos (SQLAlchemy):** Representación de las tablas de la base de datos.
- **Schemas (Pydantic):** Validación y serialización de datos de entrada/salida para la API.
- **Configuración:** Manejo de variables de entorno y conexión a la base de datos (PostgreSQL).

## 2. Modelos de Base de Datos
Se utilizará PostgreSQL alojada en Aiven, utilizando SQLAlchemy como ORM y `psycopg2-binary` como controlador.

### Tabla `persona`
- **id:** Integer, Primary Key, Autoincrement
- **identificacion:** String(50), Unique, Not Null
- **nombre:** String(100), Not Null
- **apellido:** String(100), Not Null
- **email:** String(100), Unique, Not Null
- **telefono:** String(20), Nullable
- **direccion:** String(255), Nullable

## 3. Endpoints de la API (Prefijo `/api/personas`)
El backend expondrá una API RESTful desarrollada en FastAPI que correrá sobre Uvicorn en el puerto `127.0.0.1:8000`.

| Método | Endpoint                     | Descripción                                                                 |
|--------|------------------------------|-----------------------------------------------------------------------------|
| GET    | `/api/personas`              | Lista de todas las personas.                                                |
| GET    | `/api/personas/{identificacion}` | Obtener persona específica por su número de identificación.               |
| POST   | `/api/personas`              | Registrar nueva persona (valida duplicidad de identificación y email).      |
| PUT    | `/api/personas/{id}`         | Actualizar los datos de una persona por su ID.                              |
| DELETE | `/api/personas/{id}`         | Eliminar una persona por su ID.                                             |

## 4. Configuración y Base de Datos (Aiven PostgreSQL)
- **Base de Datos:** PostgreSQL en la nube (Aiven).
- **Tecnologías:** `FastAPI`, `Uvicorn`, `SQLAlchemy`, `psycopg2-binary`.
- **String de Conexión:** Se inyectará a través de variables de entorno (`.env`) para seguridad.

## 5. Configuración de CORS
Para permitir que la aplicación cliente (Flutter Web) consuma la API sin problemas, se habilitará y configurará totalmente CORS:
- **Orígenes permitidos:** `http://localhost:*` y `http://127.0.0.1:*` (y los puertos que requiera Flutter Web).
- **Métodos permitidos:** Todos (`GET, POST, PUT, DELETE, OPTIONS, etc.`).
- **Cabeceras permitidas:** Todas (`*`).

## 6. Flujo de Trabajo (GitFlow)
El desarrollo seguirá la convención GitFlow y commits semánticos:
- **`main`:** Producción (código probado y liberado).
- **`develop`:** Integración principal de desarrollo.
- **`feature/*`:** Ramas de características (ej. `feature/endpoints-crud`).
- **`hotfix/*`:** Para correcciones críticas rápidas.
- **Commits Semánticos:** Se utilizarán prefijos como `feat:`, `fix:`, `docs:`, `chore:`, `refactor:` en los mensajes de commit.
