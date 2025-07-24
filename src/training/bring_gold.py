import sqlite3
import pandas as pd


def gold_dataframe() -> pd.DataFrame:
    """
    Consulta todos los registros de la tabla 'ventas_gold' de la base de datos
    SQLite 'coppelchallenge.db' y devuelve un DataFrame con los datos.

    Returns:
        pd.DataFrame: DataFrame con los datos completos de 'ventas_gold'.

    Raises:
        sqlite3.Error:
        Si ocurre algún error al conectar o ejecutar la consulta.
    """
    conn = sqlite3.connect('coppelchallenge.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM ventas_gold')

    column_names = [description[0] for description in cursor.description]

    filas = cursor.fetchall()

    df = pd.DataFrame(filas, columns=column_names)

    conn.close()

    return df
