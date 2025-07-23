from bring_silver import silver_dataframe
from transform_gold_functions import GoldClass
from sending_gold import gold_table

def running_all_gold():
    gold = silver_dataframe()

    gold_class = GoldClass(gold)

    df_silver = gold_class.all_gold_functions()

    gold_table(df_silver)

