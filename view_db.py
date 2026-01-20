import sqlite3
import os

# Path to the database
db_path = os.path.join('instance', 'coworking.db')

if not os.path.exists(db_path):
    print(f"No se encontró la base de datos en: {db_path}")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def print_table(table_name):
    print(f"\n--- Tabla: {table_name} ---")
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Get column names
        names = [description[0] for description in cursor.description]
        print(f"{' | '.join(names)}")
        print("-" * 50)
        
        for row in rows:
            print(f"{' | '.join(map(str, row))}")
    except sqlite3.OperationalError as e:
        print(f"Error leyendo tabla {table_name}: {e}")

print("Leyendo contenido de la base de datos...")
print_table('administradores')
print_table('usuarios')
print_table('registros_acceso')
print_table('espacios')
print_table('reservas')

conn.close()
