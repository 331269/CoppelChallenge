from gold.bring_silver import silver_dataframe
from gold.transform_gold_functions import GoldClass
from gold.sending_gold import gold_table


def running_all_gold() -> None:
    """
    Ejecuta el pipeline completo de la etapa Gold del patrón Medallion:
    - Carga los datos Silver desde la base de datos.
    - Aplica las transformaciones Gold usando GoldClass.
    - Guarda el resultado final en la tabla Gold.

    No recibe parámetros ni retorna valor.
    """
    gold = silver_dataframe()
    gold_class = GoldClass(gold)
    df_silver = gold_class.all_gold_functions()
    gold_table(df_silver)
