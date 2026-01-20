import sqlite3
import os

db_path = os.path.join('instance', 'coworking.db')

if not os.path.exists(db_path):
    print("Base de datos no encontrada.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("INSERT OR IGNORE INTO espacios (id, nombre, tipo, activo) VALUES (1, 'Coworking General', 'puesto', 1)")
    conn.commit()
    print("Espacio predeterminado verificado/creado.")
except sqlite3.OperationalError as e:
    print(f"Error al sembrar espacio: {e}")
finally:
    conn.close()
