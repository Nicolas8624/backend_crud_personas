from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/api/personas",
    tags=["personas"]
)

@router.get("", response_model=List[schemas.PersonaResponse])
def get_personas(db: Session = Depends(get_db)):
    personas = db.query(models.Persona).all()
    return personas

@router.get("/{identificacion}", response_model=schemas.PersonaResponse)
def get_persona(identificacion: str, db: Session = Depends(get_db)):
    persona = db.query(models.Persona).filter(models.Persona.identificacion == identificacion).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@router.post("", response_model=schemas.PersonaResponse, status_code=status.HTTP_201_CREATED)
def create_persona(persona: schemas.PersonaCreate, db: Session = Depends(get_db)):
    # Validar duplicidad de identificación
    db_persona_id = db.query(models.Persona).filter(models.Persona.identificacion == persona.identificacion).first()
    if db_persona_id:
        raise HTTPException(status_code=400, detail="La identificación ya está registrada")
    
    # Validar duplicidad de email
    db_persona_email = db.query(models.Persona).filter(models.Persona.email == persona.email).first()
    if db_persona_email:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    nueva_persona = models.Persona(**persona.model_dump())
    db.add(nueva_persona)
    db.commit()
    db.refresh(nueva_persona)
    return nueva_persona

@router.put("/{id}", response_model=schemas.PersonaResponse)
def update_persona(id: int, persona_update: schemas.PersonaUpdate, db: Session = Depends(get_db)):
    db_persona = db.query(models.Persona).filter(models.Persona.id == id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    # Validar email duplicado si se está actualizando
    if persona_update.email:
        db_email_check = db.query(models.Persona).filter(models.Persona.email == persona_update.email, models.Persona.id != id).first()
        if db_email_check:
            raise HTTPException(status_code=400, detail="El email ya está en uso por otra persona")
            
    update_data = persona_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_persona, key, value)
        
    db.commit()
    db.refresh(db_persona)
    return db_persona

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(id: int, db: Session = Depends(get_db)):
    db_persona = db.query(models.Persona).filter(models.Persona.id == id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    
    db.delete(db_persona)
    db.commit()
    return None
