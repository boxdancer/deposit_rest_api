import pytest
from datetime import datetime
from main import deposit_calculation, Deposit


@pytest.fixture
def deposit():
    return Deposit(date='31.01.2021', periods=3, amount=10000, rate=6)


@pytest.fixture
def first_payment_date():
    return datetime(2021, 1, 31)


def test_deposit_calculation(deposit, first_payment_date):
    result = deposit_calculation(deposit, first_payment_date)
    assert result['28.02.2021'] == 10100.25
    assert result['31.01.2021'] == 10050.0
    assert result['31.03.2021'] == 10150.75

