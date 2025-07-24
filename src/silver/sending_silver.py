import sqlite3
import pandas as pd


def silver_table(dataframe: pd.DataFrame) -> None:
    """
    Inserta los datos contenidos en el DataFrame proporcionado en la tabla
    'ventas_silver' dentro de la base de datos SQLite 'coppelchallenge.db'.

    La función crea la tabla si no existe, con las columnas correspondientes
    a los datos de Silver layer.

    Args:
        dataframe (pd.DataFrame): DataFrame que contiene los datos a insertar.
            Debe incluir las columnas:
            ['InvoiceNo', 'StockCode', 'Description',
            'Quantity', 'InvoiceDate',
             'UnitPrice', 'CustomerID', 'Country', 'DateColumn',
             'total_price_per_item'].

    Returns:
        None

    Raises:
        sqlite3.Error: Si ocurre algún error al
        conectar o ejecutar la consulta SQL.
    """
    conn = sqlite3.connect('coppelchallenge.db')

    cursor = conn.cursor()

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

    dataframe.to_sql('ventas_silver', conn, if_exists='append', index=False)

    conn.close()
