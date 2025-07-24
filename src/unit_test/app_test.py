# tests/test_app.py

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_endpoint():
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
