from app import app
from database import db
from models import Espacio, Reserva
import sqlite3

def migrate():
    with app.app_context():
        # SQLite doesn't support sophisticated migrations easily, 
        # but since we are adding new tables, db.create_all() works for them.
        # For the new column in RegistroAcceso, we might need a manual alter if table exists.
        
        print("Creating new tables (if any)...")
        db.create_all()
        
        # Check if reserva_id column exists in RegistroAcceso
        # We use raw sqlite for this check/update
        conn = sqlite3.connect('instance/coworking.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT reserva_id FROM registros_acceso LIMIT 1")
            print("Columna 'reserva_id' ya existe.")
        except sqlite3.OperationalError:
            print("Agregando columna 'reserva_id' a registros_acceso...")
            cursor.execute("ALTER TABLE registros_acceso ADD COLUMN reserva_id INTEGER REFERENCES reservas(id)")
            conn.commit()
            
        conn.close()

        # Seed Spaces
        if not Espacio.query.first():
            print("Sembrando espacios iniciales...")
            espacios = [
                Espacio(nombre="Sala Juntas A", tipo="sala"),
                Espacio(nombre="Sala Juntas B", tipo="sala"),
                Espacio(nombre="Puesto 1", tipo="puesto"),
                Espacio(nombre="Puesto 2", tipo="puesto"),
                Espacio(nombre="Puesto 3", tipo="puesto"),
                Espacio(nombre="Puesto 4", tipo="puesto"),
                Espacio(nombre="Puesto 5", tipo="puesto"),
            ]
            for e in espacios:
                db.session.add(e)
            db.session.commit()
            print("Espacios creados.")
        else:
            print("Espacios ya existen.")

if __name__ == "__main__":
    migrate()
