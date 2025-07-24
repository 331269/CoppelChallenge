from bronze.bronze_data import bronze_table
from silver.transform_silver_run import running_all_silver
from gold.transform_gold_run import running_all_gold


def running_complete_medallion():
    bronze_table()
    running_all_silver()
    running_all_gold()
