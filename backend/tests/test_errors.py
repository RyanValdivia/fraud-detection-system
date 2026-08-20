from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_HEADERS = {"x-api-key": "fraud-dev-key-123"}

SAMPLE_TRANSACTION = {
    "transaction_id": "test-error-001",
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


def test_predict_rejects_invalid_api_key():
    response = client.post(
        "/predict",
        json=SAMPLE_TRANSACTION,
        headers={"x-api-key": "wrong-key"},
    )
    assert response.status_code == 401


def test_predict_rejects_missing_api_key():
    response = client.post("/predict", json=SAMPLE_TRANSACTION)
    assert response.status_code == 422


def test_predict_rejects_invalid_amount():
    invalid_transaction = {**SAMPLE_TRANSACTION, "amt": -10}
    response = client.post(
        "/predict",
        json=invalid_transaction,
        headers=VALID_HEADERS,
    )
    assert response.status_code == 422


def test_get_transaction_not_found():
    response = client.get(
        "/transactions/does-not-exist-xyz",
        headers=VALID_HEADERS,
    )
    assert response.status_code == 404


def test_get_transaction_rejects_invalid_api_key():
    response = client.get(
        "/transactions/does-not-exist-xyz",
        headers={"x-api-key": "wrong-key"},
    )
    assert response.status_code == 401
