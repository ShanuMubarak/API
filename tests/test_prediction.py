from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_endpoint():
    payload = {
        "customers": [
            {
                "CustomerID": "C001",
                "Total_Spent": 5000.0,
                "Total_Quantity": 10,
                "Num_Orders": 5,
                "Customer_Age": 35,
                "Gender_Code": 1,
                "Num_Recommendations": 2
            },
            {
                "CustomerID": "C002",
                "Total_Spent": 12000.0,
                "Total_Quantity": 20,
                "Num_Orders": 8,
                "Customer_Age": 42,
                "Gender_Code": 0,
                "Num_Recommendations": 3
            }
        ]
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    for item in result:
        assert "customer_id" in item
        assert "cluster" in item
        assert "recommended_products" in item
        assert isinstance(item["recommended_products"], list)
        assert len(item["recommended_products"]) > 0
