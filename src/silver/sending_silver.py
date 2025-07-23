import sqlite3
import pandas as pd

# #['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate',
#        'UnitPrice', 'CustomerID', 'Country', 'DateColumn',
#        'total_price_per_item'],

def silver_table(dataframe):
    # Crear conexión a base de datos (si no existe, se crea el archivo)
    conn = sqlite3.connect('coppelchallenge.db')

    # Crear cursor para ejecutar queries
    cursor = conn.cursor()

    # Crear tabla (si no existe)
    cursor.execute('''
        
    CREATE TABLE IF NOT EXISTS ventas_silver (
        InvoiceNo TEXT,
        StockCode TEXT,
        Description TEXT,
        Quantity REAL,
        InvoiceDate TEXT,
        UnitPrice REAL,
        CustomerID TEXT,
        Country TEXT,
        DateColumn TEXT,
        total_price_per_item REAL
    );
    ''')

    # Insertar el DataFrame completo en la tabla 'ventas'
    dataframe.to_sql('ventas_silver', conn, if_exists='append', index=False)
