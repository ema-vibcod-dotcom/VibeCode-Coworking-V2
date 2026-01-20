import sqlite3
import os

db_path = os.path.join('instance', 'coworking.db')

if not os.path.exists(db_path):
    print("Base de datos no encontrada.")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# We use 7 spaces named Sala 1 to Sala 7
spaces = [
    (1, 'Sala 1', 'sala', 1),
    (2, 'Sala 2', 'sala', 1),
    (3, 'Sala 3', 'sala', 1),
    (4, 'Sala 4', 'sala', 1),
    (5, 'Sala 5', 'sala', 1),
    (6, 'Sala 6', 'sala', 1),
    (7, 'Sala 7', 'sala', 1)
]

try:
    # First, let's clear existing spaces to ensure we only have these 7
    cursor.execute("DELETE FROM espacios")
    
    for s in spaces:
        cursor.execute("INSERT INTO espacios (id, nombre, tipo, activo) VALUES (?, ?, ?, ?)", s)
    
    conn.commit()
    print("7 salas (Sala 1-7) sembradas exitosamente.")
except sqlite3.OperationalError as e:
    print(f"Error al sembrar salas: {e}")
finally:
    conn.close()
