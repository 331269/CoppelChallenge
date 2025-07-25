from silver.transform_silver_functions import SilverClass
from silver.bring_bronze import bronze_dataframe
from silver.sending_silver import silver_table


def running_all_silver() -> None:
    """
    Ejecuta el pipeline completo de la etapa Silver del patrón Medallion:
    - Carga los datos Bronze desde la base de datos.
    - Aplica las transformaciones Silver usando SilverClass.
    - Guarda el resultado final en la tabla Silver.

    No recibe parámetros ni retorna valor.
    """
    silver = bronze_dataframe()
    sil_class = SilverClass(silver)
    df_silver = sil_class.all_functions()
    silver_table(df_silver)
