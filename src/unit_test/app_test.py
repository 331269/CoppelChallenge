from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_predict_endpoint():
    """
    Test para el endpoint /predict/ de la API.
    Envía una lista de datos de entrada y verifica que:
    - La respuesta sea status 200.
    - La respuesta contenga una clave 'data'.
    - 'data' sea una lista.
    - Cada elemento de 'data' contenga las columnas esperadas.
    """
    sample_input = [
        {
            "InvoiceNo": "536365",
            "StockCode": "85123A",
            "Description": "WHITE HANGING HEART T-LIGHT HOLDER",
            "Quantity": 6,
            "InvoiceDate": "12/1/2010 8:26",
            "UnitPrice": 2.55,
            "CustomerID": 17850.0,
            "Country": "United Kingdom"
        },
        {
            "InvoiceNo": "536365",
            "StockCode": "71053",
            "Description": "WHITE METAL LANTERN",
            "Quantity": 6,
            "InvoiceDate": "12/1/2010 8:26",
            "UnitPrice": 3.39,
            "CustomerID": 17850.0,
            "Country": "France"
        }
    ]

    response = client.post("/predict/", json=sample_input)
    assert response.status_code == 200

    json_response = response.json()

    # Verificar que la respuesta contenga 'data' y que sea una lista
    assert "data" in json_response
    assert isinstance(json_response["data"], list)

    # Verificar que cada registro tenga las claves esperadas
    expected_keys = {
        "Quantity",
        "total",
        "regroup_country",
        "predictions",
        "CustomerID",
        "fecha_procesamiento"
    }

    for record in json_response["data"]:
        assert expected_keys.issubset(record.keys())
