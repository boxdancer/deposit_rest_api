from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from starlette.responses import PlainTextResponse

from date_processing import get_next_dates, validate_date_string


# Задаем модель для входных данных
class Deposit(BaseModel):
    date: Annotated[str, Field(min_length=10, max_length=10)]
    periods: Annotated[int, Field(ge=1, le=60)]
    amount: Annotated[int, Field(ge=10 ** 4, le=3 * 10 ** 6)]
    rate: Annotated[float, Field(ge=1, le=8)]


app = FastAPI()


# Переопределение исключений проверки запроса, чтобы код ошибки был 400 (по условию), а не 422
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


# Определяем маршрут для обработки запроса
@app.get("/deposit")
async def deposit_calculation_api(deposit: Deposit):
    date_validation = validate_date_string(deposit.date)
    if not date_validation:
        raise HTTPException(status_code=400, detail="Invalid date format")
    # Преобразуем строку в объект даты
    first_payment_date = datetime.strptime(deposit.date, "%d.%m.%Y")

    return deposit_calculation(deposit, first_payment_date)


def deposit_calculation(deposit: Deposit, first_payment_date: datetime):
    respond_dict = {}
    date_payments = get_next_dates(first_payment_date, deposit.periods)
    for i in range(deposit.periods):
        delta_money = deposit.amount * 0.01 * deposit.rate / 12
        deposit.amount += delta_money
        respond_dict[date_payments[i]] = round(deposit.amount, 2)

    return respond_dict


@app.get("/")
async def alive_status():
    return {"message": "Hello World, I'm alive"}
