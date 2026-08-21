from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class PersonaBase(BaseModel):
    identificacion: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    foto_perfil: Optional[str] = None

class PersonaCreate(PersonaBase):
    pass

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
