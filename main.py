from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="API Gestión Personas")

# 1. Habilitar CORS para permitir peticiones desde Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. PEGA AQUÍ TU URI DE SUPABASE CON TU CONTRASEÑA
DATABASE_URL = "postgresql://postgres:27dedicde2007@db.otpyngnosdebzeoqyafd.supabase.co:5432/postgres"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# 3. Modelos de datos
class PersonaCreate(BaseModel):
    identificacion: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class PersonaResponse(PersonaCreate):
    id: int

# 4. Endpoints que consume Flutter

@app.get("/api/personas", response_model=List[PersonaResponse])
def get_personas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM persona ORDER BY id ASC")
    personas = cursor.fetchall()
    cursor.close()
    conn.close()
    return personas

@app.get("/api/personas/{identificacion}", response_model=PersonaResponse)
def get_persona_by_identificacion(identificacion: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM persona WHERE identificacion = %s", (identificacion,))
    persona = cursor.fetchone()
    cursor.close()
    conn.close()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@app.post("/api/personas", status_code=status.HTTP_201_CREATED, response_model=PersonaResponse)
def create_persona(persona: PersonaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO persona (identificacion, nombre, apellido, email, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
        """
        cursor.execute(query, (persona.identificacion, persona.nombre, persona.apellido, persona.email, persona.telefono, persona.direccion))
        nueva_persona = cursor.fetchone()
        conn.commit()
        return nueva_persona
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear persona: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.put("/api/personas/{id}", response_model=PersonaResponse)
def update_persona(id: int, persona: PersonaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE persona 
            SET nombre = %s, apellido = %s, email = %s, telefono = %s, direccion = %s
            WHERE id = %s RETURNING *;
        """
        cursor.execute(query, (persona.nombre, persona.apellido, persona.email, persona.telefono, persona.direccion, id))
        updated_persona = cursor.fetchone()
        if not updated_persona:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        conn.commit()
        return updated_persona
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.delete("/api/personas/{id}", status_code=status.HTTP_200_OK)
def delete_persona(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM persona WHERE id = %s RETURNING id;", (id,))
        deleted = cursor.fetchone()
        if not deleted:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        conn.commit()
        return {"message": "Persona eliminada correctamente"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar: {str(e)}")
    finally:
        cursor.close()
        conn.close()
