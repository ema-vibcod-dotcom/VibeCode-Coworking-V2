from app import create_app
from database import db
from models import Espacio

def seed():
    app = create_app()
    with app.app_context():
        print("Verificando espacios...")
        
        # Lista de espacios a crear
        spaces_to_add = [
            {'id': 1, 'nombre': 'Sala 1', 'tipo': 'sala'},
            {'id': 2, 'nombre': 'Sala 2', 'tipo': 'sala'},
            {'id': 3, 'nombre': 'Sala 3', 'tipo': 'sala'},
            {'id': 4, 'nombre': 'Sala 4', 'tipo': 'sala'},
            {'id': 5, 'nombre': 'Sala 5', 'tipo': 'sala'},
            {'id': 6, 'nombre': 'Sala 6', 'tipo': 'sala'},
            {'id': 7, 'nombre': 'Sala 7', 'tipo': 'sala'}
        ]

        for s_data in spaces_to_add:
            # Verificar si ya existe
            exist = Espacio.query.get(s_data['id'])
            if not exist:
                nuevo_espacio = Espacio(
                    id=s_data['id'],
                    nombre=s_data['nombre'],
                    tipo=s_data['tipo'],
                    activo=True
                )
                db.session.add(nuevo_espacio)
                print(f"Agregado: {s_data['nombre']}")
            else:
                print(f"Ya existe: {s_data['nombre']}")
        
        db.session.commit()
        print("Proceso completado.")

if __name__ == "__main__":
    seed()
