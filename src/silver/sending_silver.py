import sqlite3
import pandas as pd

def silver_table(dataframe):
    # Crear conexión a base de datos (si no existe, se crea el archivo)
    conn = sqlite3.connect('coppelchallenge.db')

    # Crear cursor para ejecutar queries
    cursor = conn.cursor()

    # Crear tabla (si no existe)
    cursor.execute('''
        
    CREATE TABLE IF NOT EXISTS ventas_silver (
        CustomerID TEXT,
        DateColumn TEXT,
        Quantity INTEGER,
        total REAL,
        Country TEXT,
        NextPurchaseDate TEXT,
        days_since_last_purchase INTEGER,
        Target_90Days INTEGER
    );
    ''')

    # Insertar el DataFrame completo en la tabla 'ventas'
    dataframe.to_sql('ventas_silver', conn, if_exists='append', index=False)
