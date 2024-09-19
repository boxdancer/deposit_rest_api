from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from starlette.responses import PlainTextResponse

from next_month_date import get_next_dates


# Задаем модель для входных данных
class Deposit(BaseModel):
    # todo мб тут можно прописать регулярку для проверки строки на формат даты и не делать try except на 33 строке
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
@app.post("/deposit")
async def deposit_calculation(deposit: Deposit):
    respond_dict = {}

    try:
        date_payments = get_next_dates(deposit.date, deposit.periods)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format")

    for i in range(deposit.periods):
        delta_money = deposit.amount * 0.01 * deposit.rate / 12
        deposit.amount += delta_money
        respond_dict[date_payments[i]] = round(deposit.amount, 2)

    return respond_dict
