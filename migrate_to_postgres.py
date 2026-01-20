import sqlite3
import os
import psycopg2
from datetime import datetime

# Configuración
SQLITE_DB = os.path.join('instance', 'coworking.db')
POSTGRES_URL = os.environ.get('DATABASE_URL')

def migrate():
    if not POSTGRES_URL:
        print("Error: La variable de entorno DATABASE_URL no está configurada.")
        return

    print(f"Iniciando migración desde {SQLITE_DB} a PostgreSQL...")

    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_cursor = sqlite_conn.cursor()

    # Reemplazar postgres:// por postgresql:// si es necesario
    pg_url = POSTGRES_URL
    if pg_url.startswith("postgres://"):
        pg_url = pg_url.replace("postgres://", "postgresql://", 1)

    try:
        pg_conn = psycopg2.connect(pg_url)
        pg_cursor = pg_conn.cursor()
        print("Conexión a PostgreSQL establecida.")

        # Tablas en orden de dependencia
        tables = [
            'administradores',
            'usuarios',
            'espacios',
            'reservas',
            'registros_acceso'
        ]

        for table in tables:
            print(f"Migrando tabla: {table}...")
            
            # Leer de SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                print(f"La tabla {table} está vacía, saltando...")
                continue

            # Obtener nombres de columnas
            columns = [description[0] for description in sqlite_cursor.description]
            cols_str = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))

            # Limpiar tabla destino (opcional, cuidado con esto)
            pg_cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE")

            # Insertar en Postgres
            query = f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders})"
            pg_cursor.executemany(query, rows)
            
            print(f"Migrados {len(rows)} registros a {table}.")

        pg_conn.commit()
        print("\n¡Migración completada con éxito!")

    except Exception as e:
        print(f"\nError durante la migración: {e}")
    finally:
        sqlite_conn.close()
        if 'pg_conn' in locals():
            pg_conn.close()

if __name__ == "__main__":
    migrate()
