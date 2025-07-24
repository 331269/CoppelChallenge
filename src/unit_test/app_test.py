from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient
from app import app

# Aquí parcheamos joblib.load para que no intente cargar el archivo real


@pytest.fixture(autouse=True)
def mock_joblib_load():
    with patch("app.load", return_value=MagicMock()) as mock_load:
        yield mock_load


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
            "Country": "United Kingdom",
        }
    ]

    response = client.post("/predict/", json=sample_input)
    assert response.status_code == 200
    assert "prediction" in response.json()
