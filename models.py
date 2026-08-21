from sqlalchemy import Column, Integer, String, Text
from database import Base

class Persona(Base):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    identificacion = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)
    foto_perfil = Column(Text, nullable=True)
