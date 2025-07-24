# tests/test_app.py
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


@patch("app.load")  # Parchea joblib.load que está en app.py
def test_predict_endpoint(mock_load):
    # Creamos un mock para el modelo con predict fijo
    mock_model = MagicMock()
    mock_model.predict.return_value = [0, 1]  # Respuesta simulada
    mock_load.return_value = mock_model  # load() devuelve este mock_model

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
    assert "prediction" in json_response
    assert json_response["prediction"] == [0, 1]
