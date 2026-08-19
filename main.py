from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import persona_routes

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend CRUD Personas",
    description="API REST para gestionar personas",
    version="1.0.0"
)

# Configuración CORS para Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite todos los orígenes en desarrollo (http://localhost:*, http://127.0.0.1:*)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(persona_routes.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Gestión de Personas"}
