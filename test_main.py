from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_deposit_calculation_correct():
    response = client.post(
        "/deposit",
        json={
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 6
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "31.01.2021": 10050,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75
    }


def test_deposit_calculation_wrong_date_format():
    response = client.post(
        "/deposit",
        json={
            "date": "31/01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 6
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid date format"
    }


def test_deposit_calculation_wrong_period():
    response = client.post(
        "/deposit",
        json={
            "date": "31.01.2021",
            "periods": 300,
            "amount": 10000,
            "rate": 6
        },
    )
    assert response.status_code == 400


def test_deposit_calculation_wrong_amount():
    response = client.post(
        "/deposit",
        json={
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10,
            "rate": 6
        },
    )
    assert response.status_code == 400


def test_deposit_calculation_wrong_rate():
    response = client.post(
        "/deposit",
        json={
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": -6
        },
    )
    assert response.status_code == 400
