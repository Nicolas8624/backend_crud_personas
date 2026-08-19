from database import SessionLocal, engine, Base
import models

def seed_data():
    # Asegurar que las tablas existan
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    initial_personas = [
        {
            "identificacion": "123456789",
            "nombre": "Carlos",
            "apellido": "Ramírez",
            "email": "carlos.ramirez@example.com",
            "telefono": "3001234567",
            "direccion": "Calle 1 # 2-3"
        },
        {
            "identificacion": "987654321",
            "nombre": "María",
            "apellido": "González",
            "email": "maria.gonzalez@example.com",
            "telefono": "3109876543",
            "direccion": "Carrera 4 # 5-6"
        },
        {
            "identificacion": "456123789",
            "nombre": "Luis",
            "apellido": "Fernández",
            "email": "luis.fernandez@example.com",
            "telefono": "3154567890",
            "direccion": "Avenida 7 # 8-9"
        }
    ]
    
    try:
        print("Iniciando inserción de datos semilla...")
        for data in initial_personas:
            # Validar si ya existe la identificación
            exists = db.query(models.Persona).filter_by(identificacion=data["identificacion"]).first()
            if not exists:
                new_persona = models.Persona(**data)
                db.add(new_persona)
                print(f" -> Agregado: {data['nombre']} {data['apellido']}")
            else:
                print(f" -> Omitido (ya existe): {data['nombre']} {data['apellido']}")
        
        db.commit()
        print("Población de datos iniciales finalizada correctamente.")
    except Exception as e:
        db.rollback()
        print(f"Error durante la inserción: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
