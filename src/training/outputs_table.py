import sqlite3


def outputs():
    # Crear conexión a base de datos (si no existe, se crea el archivo)
    conn = sqlite3.connect('coppelchallenge.db')

    # Crear cursor para ejecutar queries
    cursor = conn.cursor()

    # Crear tabla (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS outputs_table (
        Quantity TEXT,
        total TEXT,
        regroup_country TEXT,
        prediction INTEGER
    );

    ''')
