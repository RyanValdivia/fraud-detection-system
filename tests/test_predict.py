from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SAMPLE_TRANSACTION = {
    "transaction_id": "tx_001",
    "cc_num": "4111111111111111",
    "amt": 120.50,
    "merchant": "fraud_Kirlin and Sons",
    "category": "shopping_pos",
    "gender": "F",
    "dob": "1990-05-14",
    "city_pop": 50000,
    "lat": -12.0464,
    "long": -77.0428,
    "merch_lat": -12.10,
    "merch_long": -77.05,
    "trans_time": "2026-08-05T14:30:00",
}


def test_predict_returns_valid_decision():
    response = client.post("/predict", json=SAMPLE_TRANSACTION)
    assert response.status_code == 200
    body = response.json()
    assert body["transaction_id"] == "tx_001"
    assert 0.0 <= body["fraud_probability"] <= 1.0
    assert body["decision"] in {"allow", "review", "block"}
    assert body["distance_km"] >= 0
