import sqlite3
import pandas as pd

# ['Quantity', 'total', 'Target_90Days', 'regroup_country']

def gold_table(dataframe):
    # Crear conexión a base de datos (si no existe, se crea el archivo)
    conn = sqlite3.connect('coppelchallenge.db')

    # Crear cursor para ejecutar queries
    cursor = conn.cursor()

    # Crear tabla (si no existe)
    cursor.execute('''
        
    CREATE TABLE IF NOT EXISTS ventas_gold (
        Quantity REAL,
        total REAL,
        Target_90Days INTEGER,
        regroup_country TEXT
    );
    ''')

    # Insertar el DataFrame completo en la tabla 'ventas'
    dataframe.to_sql('ventas_gold', conn, if_exists='append', index=False)
