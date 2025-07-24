from bronze.bronze_data import bronze_table
from silver.transform_silver_run import running_all_silver
from gold.transform_gold_run import running_all_gold


def running_complete_medallion() -> None:
    """
    Ejecuta el pipeline completo del patrón Medallion:
    - Carga datos bronce con `bronze_table()`
    - Ejecuta las transformaciones Silver con `running_all_silver()`
    - Ejecuta las transformaciones Gold con `running_all_gold()`

    Esta función orquesta las etapas principales del flujo de datos,
    garantizando que las tablas y transformaciones se apliquen en orden.

    No recibe parámetros ni retorna valor.
    """
    bronze_table()
    running_all_silver()
    running_all_gold()
