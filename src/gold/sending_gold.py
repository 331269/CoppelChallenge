import sqlite3
import pandas as pd


def gold_table(dataframe: pd.DataFrame) -> None:
    """
    Inserta los datos contenidos en el DataFrame proporcionado en la tabla
    'ventas_gold' dentro de la base de datos SQLite 'coppelchallenge.db'.

    La función crea la tabla si no existe, con las columnas:
    Quantity, total, Target_90Days y regroup_country.

    Args:
        dataframe (pd.DataFrame): DataFrame que contiene los datos a insertar.
            Debe incluir las columnas:
            'Quantity', 'total', 'Target_90Days', 'regroup_country'.

    Returns:
        None

    Raises:
        sqlite3.Error: Si ocurre
        algún error al conectar o ejecutar la consulta SQL.
    """
    conn = sqlite3.connect('coppelchallenge.db')

    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas_gold (
        Quantity REAL,
        total REAL,
        Target_90Days INTEGER,
        regroup_country TEXT
    );
    ''')

    dataframe.to_sql('ventas_gold', conn, if_exists='append', index=False)

    conn.close()
