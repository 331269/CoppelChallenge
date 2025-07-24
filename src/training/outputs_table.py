import sqlite3


def outputs() -> None:
    """
    Crea la tabla 'outputs_table'
    en la base de datos SQLite 'coppelchallenge.db' si no existe.
    La tabla contiene columnas para los resultados del modelo y metadatos.

    No recibe parámetros ni retorna valor.

    Raises:
        sqlite3.Error: Si ocurre algún
        error al conectar o ejecutar la consulta SQL.
    """
    conn = sqlite3.connect('coppelchallenge.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS outputs_table (
        Quantity TEXT,
        total TEXT,
        regroup_country TEXT,
        predictions INTEGER,
        CustomerID TEXT,
        fecha_procesamiento TEXT
    );
    ''')

    conn.commit()
    conn.close()
