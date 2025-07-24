from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@patch('app.load')  # mockeamos joblib.load que está usado en app.py
def test_predict_endpoint(mock_load):
    # Crear un mock para el modelo con método predict
    mock_model = MagicMock()
    mock_model.predict.return_value = [1, 0]  # ejemplo de predicciones
    mock_load.return_value = mock_model  # load() devolverá el mock_model

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
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], list)
