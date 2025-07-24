import pytest
import pandas as pd
from silver.transform_silver_functions import SilverClass
# Ajusta la ruta si es necesario


@pytest.fixture
def raw_data():
    return pd.DataFrame({
        'InvoiceNo': ['A123', 'C456', 'B789'],
        'StockCode': ['X1', 'X2', 'X3'],
        'Description': ['Item A', 'Item B', 'Item C'],
        'Quantity': [10, -5, 3],
        'InvoiceDate': ['12/01/2020 08:26',
                        '12/01/2020 08:26', '12/02/2020 09:00'],
        'UnitPrice': [2.5, 0, 3.0],
        'CustomerID': [12345.0, None, 67890.0],
        'Country': ['United Kingdom', 'United Kingdom', 'France']
    })


def test_all_functions(raw_data):
    silver = SilverClass(raw_data)
    result_df = silver.all_functions()

    # Deben quedar 2 filas válidas
    assert result_df.shape[0] == 2

    # Verifica CustomerID se convirtió a string y se llenó
    assert result_df['CustomerID'].tolist() == ['12345', '67890']

    # Verifica que las fechas estén correctamente formateadas
    assert result_df['DateColumn'].tolist() == ['01-12-2020', '02-12-2020']

    # Verifica que el cálculo de total_price_per_item sea correcto
    assert result_df['total_price_per_item'].tolist() == [25.0, 9.0]
