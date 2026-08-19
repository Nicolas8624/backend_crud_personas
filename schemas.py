from pydantic import BaseModel, EmailStr
from typing import Optional

class PersonaBase(BaseModel):
    identificacion: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class PersonaResponse(PersonaBase):
    id: int

    class Config:
        from_attributes = True
