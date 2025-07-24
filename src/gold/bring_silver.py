import sqlite3
import pandas as pd


def silver_dataframe() -> pd.DataFrame:
    """
    Lee todos los registros de la tabla
    'ventas_silver' de la base de datos
    SQLite 'coppelchallenge.db' y retorna
    un DataFrame de pandas con los datos.

    Returns:
        pd.DataFrame: DataFrame con todas las
        filas y columnas de la tabla 'ventas_silver'.

    Raises:
        sqlite3.Error: Si ocurre algún error
        al conectar o ejecutar la consulta.
    """
    conn = sqlite3.connect('coppelchallenge.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM ventas_silver')

    column_names = [description[0] for description in cursor.description]

    filas = cursor.fetchall()

    df = pd.DataFrame(filas, columns=column_names)

    conn.close()

    return df
