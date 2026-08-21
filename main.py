from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="API Gestión Personas")

# 1. Habilitar CORS para permitir peticiones desde Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Lee la URL de conexión desde el archivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# 3. Modelos de datos
class PersonaCreate(BaseModel):
    identificacion: str
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    foto_perfil: Optional[str] = None

class PersonaUpdate(BaseModel):
    identificacion: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    foto_perfil: Optional[str] = None

class PersonaResponse(BaseModel):
    id: int
    identificacion: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    foto_perfil: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

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
            INSERT INTO persona (identificacion, nombre, apellido, email, telefono, direccion, foto_perfil)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;
        """
        cursor.execute(query, (persona.identificacion, persona.nombre, persona.apellido, persona.email, persona.telefono, persona.direccion, persona.foto_perfil))
        nueva_persona = cursor.fetchone()
        conn.commit()
        return nueva_persona
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Error al crear persona: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@app.put("/api/personas/{persona_id}", response_model=PersonaResponse)
def update_persona(persona_id: int, persona: PersonaUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE persona 
            SET identificacion = %s,
                nombre = %s,
                apellido = %s,
                email = %s,
                telefono = %s,
                direccion = %s,
                foto_perfil = %s
            WHERE id = %s
            RETURNING id, identificacion, nombre, apellido, email, telefono, direccion, foto_perfil;
            """,
            (
                persona.identificacion,
                persona.nombre,
                persona.apellido,
                persona.email,
                persona.telefono,
                persona.direccion,
                persona.foto_perfil,
                persona_id
            )
        )
        updated = cursor.fetchone()
        conn.commit()
        
        if not updated:
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        
        # Soporte tanto si cursor devuelve dict (RealDictCursor) o tupla
        if isinstance(updated, dict):
            return updated
        else:
            return {
                "id": updated[0],
                "identificacion": updated[1],
                "nombre": updated[2],
                "apellido": updated[3],
                "email": updated[4],
                "telefono": updated[5],
                "direccion": updated[6],
                "foto_perfil": updated[7]
            }
    except Exception as e:
        conn.rollback()
        print(f"ERROR EN PUT PERSONA: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/api/personas/{id}", status_code=status.HTTP_200_OK)
def delete_persona(id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM persona WHERE (id::text = %s OR identificacion = %s) RETURNING id;", (str(id), str(id)))
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

