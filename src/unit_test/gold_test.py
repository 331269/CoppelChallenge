import pytest
import pandas as pd
from gold.transform_gold_functions import GoldClass
from pytest import approx
# ajusta ruta si es necesario


@pytest.fixture
def silver_data():
    # Datos simulados para probar GoldClass,
    # imitando salida esperada de SilverClass
    return pd.DataFrame({
        'CustomerID': ['12345', '12345', '67890', '0'],
        'DateColumn': ['01-12-2020', '15-12-2020', '02-12-2020', '03-12-2020'],
        'Quantity': [10, 5, 3, 1],
        'total_price_per_item': [25.0, 12.5, 9.0, 2.0],
        'Country': ['United Kingdom', 'United Kingdom', 'France', 'Spain']
    })


def test_grouping(silver_data):
    gold = GoldClass(silver_data)
    grouped = gold.grouping(silver_data)

    # Debería agrupar por CustomerID y DateColumn, eliminar CustomerID == '0'
    assert all(grouped['CustomerID'] != '0')

    # Revisar columnas y tipos
    assert set(grouped.columns) == {'CustomerID',
                                    'DateColumn', 'Quantity',
                                    'total', 'Country'}

    # Quantity y total sumados correctamente
    assert grouped.loc[
        grouped['CustomerID'] == '12345', 'Quantity'].sum() == 15
    assert grouped.loc[grouped['CustomerID'] == '12345',
                       'total'].sum() == approx(37.5)


def test_creating_target(silver_data):
    gold = GoldClass(silver_data)
    grouped = gold.grouping(silver_data)

    target_df = gold.creating_target(grouped)

    # Columnas que deben estar
    assert set(target_df.columns) == {'Quantity', 'total',
                                      'Target_90Days', 'regroup_country'}

    # regroup_country debe ser binario (0 o 1)
    assert target_df['regroup_country'].isin([0, 1]).all()

    # Target_90Days debe tener valores 0 o 1
    assert target_df['Target_90Days'].isin([0, 1]).all()


def test_all_gold_functions(silver_data):
    gold = GoldClass(silver_data)
    df_final = gold.all_gold_functions()

    # Debe ser igual que el output de crear_target
    assert set(df_final.columns) == {'Quantity',
                                     'total',
                                     'Target_90Days', 'regroup_country'}
    assert df_final.shape[0] > 0
