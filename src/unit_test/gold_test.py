import pytest
import pandas as pd
from gold.transform_gold_functions import GoldClass
from pytest import approx


@pytest.fixture
def silver_data() -> pd.DataFrame:
    """
    Fixture que simula datos de entrada tipo Silver para probar GoldClass.

    Returns:
        pd.DataFrame: DataFrame con datos simulados.
    """
    return pd.DataFrame({
        'CustomerID': ['12345', '12345', '67890', '0'],
        'DateColumn': ['01-12-2020', '15-12-2020', '02-12-2020', '03-12-2020'],
        'Quantity': [10, 5, 3, 1],
        'total_price_per_item': [25.0, 12.5, 9.0, 2.0],
        'Country': ['United Kingdom', 'United Kingdom', 'France', 'Spain']
    })


def test_grouping(silver_data: pd.DataFrame) -> None:
    """
    Test para el método grouping de GoldClass.
    Verifica que agrupe correctamente y elimine CustomerID == '0',
    así como la suma correcta de Quantity y total.
    """
    gold = GoldClass(silver_data)
    grouped = gold.grouping(silver_data)

    # Verificar que no existan CustomerID '0'
    assert all(grouped['CustomerID'] != '0')

    # Verificar que las columnas sean las esperadas
    assert set(grouped.columns) == {'CustomerID', 'DateColumn',
                                    'Quantity', 'total', 'Country'}

    # Verificar suma correcta de Quantity y total para CustomerID '12345'
    assert grouped.loc[
        grouped['CustomerID'] == '12345', 'Quantity'].sum() == 15
    assert grouped.loc[
        grouped['CustomerID'] == '12345', 'total'].sum() == approx(37.5)


def test_creating_target(silver_data: pd.DataFrame) -> None:
    """
    Test para el método creating_target de GoldClass.
    Verifica la creación correcta del
    target y la columna regroup_country binaria.
    """
    gold = GoldClass(silver_data)
    grouped = gold.grouping(silver_data)

    target_df = gold.creating_target(grouped)

    # Verificar columnas esperadas
    assert set(target_df.columns) == {
        'Quantity', 'total', 'Target_90Days', 'regroup_country'}

    # Verificar que regroup_country sea binario (0 o 1)
    assert target_df['regroup_country'].isin([0, 1]).all()

    # Verificar que Target_90Days solo contenga 0 o 1
    assert target_df['Target_90Days'].isin([0, 1]).all()


def test_all_gold_functions(silver_data: pd.DataFrame) -> None:
    """
    Test para el método all_gold_functions de GoldClass.
    Verifica que la salida sea consistente con creating_target y no esté vacía.
    """
    gold = GoldClass(silver_data)
    df_final = gold.all_gold_functions()

    # Verificar columnas esperadas
    assert set(df_final.columns) == {
        'Quantity', 'total',
        'Target_90Days', 'regroup_country'}

    # Verificar que el DataFrame no esté vacío
    assert df_final.shape[0] > 0
