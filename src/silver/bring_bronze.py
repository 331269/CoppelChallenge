import sqlite3
import pandas as pd

def bronze_dataframe():

    conn = sqlite3.connect('coppelchallenge.db')
    cursor = conn.cursor()  # ✅ Define the cursor here

    cursor.execute('SELECT * FROM ventas_bronze')

    column_names = [description[0] for description in cursor.description]

    # Obtener los datos
    filas = cursor.fetchall()

    # Crear el DataFrame
    df = pd.DataFrame(filas, columns=column_names)

    # Cerrar la conexión
    conn.close()

    return df