import sqlite3
import pandas as pd


def bronze_table() -> None:
    """
    Carga un archivo CSV con datos de transacciones retail y lo inserta
    en una tabla SQLite llamada 'ventas_bronze' dentro de la base de datos
    'coppelchallenge.db'.

    La función crea la tabla si no existe, con las columnas especificadas.

    No recibe parámetros ni retorna valor.

    Raises:
        pd.errors.ParserError: Si hay problemas leyendo el archivo CSV.
        sqlite3.Error: Si hay errores en la conexión o ejecución SQL.
    """
    dataframe = pd.read_csv(
        'C:/Users/cleme/OneDrive/Documentos'
        '/ChallengeCoppel/CoppelChallenge'
        '/transacciones_retail.csv',
        encoding="latin1"
    )
    # Crear conexión a base de datos (si no existe, se crea el archivo)
    conn = sqlite3.connect('coppelchallenge.db')

    # Crear cursor para ejecutar queries
    cursor = conn.cursor()

    # Crear tabla (si no existe)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas_bronze (
        InvoiceNo TEXT,
        StockCode TEXT,
        Description TEXT,
        Quantity INTEGER,
        InvoiceDate TEXT,
        UnitPrice REAL,
        CustomerID REAL,
        Country TEXT
    );
    ''')

    # Insertar el DataFrame completo en la tabla 'ventas_bronze'
    dataframe.to_sql('ventas_bronze', conn, if_exists='append', index=False)

    # Cerrar conexión
    conn.close()
