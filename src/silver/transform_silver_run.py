from transform_silver_functions import SilverClass
from bring_bronze import bronze_dataframe
from sending_silver import silver_table

def running_all_silver():
    silver = bronze_dataframe()

    sil_class = SilverClass(silver)

    df_silver = sil_class.all_functions()

    silver_table(df_silver)


