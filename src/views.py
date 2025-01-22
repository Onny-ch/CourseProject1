import json
from typing import Any

from src.utils import card_information, exchange_rate, greetings, read_xls, stock_price, top_five_by_trans_amount


# Функция для страницы "Главная"
def home_page(date_time_string: str) -> dict[str, Any]:  # готова
    """
    Принимает строку с датой и возвращает информацию в виде:
        1. Приветствие в соответствии с временем суток
        2. Общую информацию по каждой карте
        3. Топ-5 транзакций по сумме платежа
        4. Курс валют
        5. Стоимость акций из S&p500
    """

    file_info = read_xls("data\\operations.xlsx")

    greet_string = greetings(date_time_string)  # 1 Приветствие

    card_info = card_information(file_info)  # 2 Инфо по карте

    top_5 = top_five_by_trans_amount(date_time_string, file_info)  # 3 Top 5 by summ

    with open("user_settings.json", "r") as file:
        data = json.load(file)
        user_data = data

    rate = exchange_rate(user_data)  # 4 Курс валют

    stocks_prices = stock_price(user_data)  # 5 Стоимость акций

    home_page_answer = {
        "greetings": greet_string,
        "cards": card_info,
        "top_transactions": top_5,
        "currency_rates": rate,
        "stock_prices": stocks_prices,
    }

    return home_page_answer  # возвращается корректный JSON-ответ


# ---------------------------------------------------------------------------------------------------------------------


#def event_page(dataframe):  # на вход идет датафрейм
def event_page(date_time_string: str, data_range: str = "M") -> json:  # на вход идет дата и необязательный параметр
    """
    Принимает на вход дату и параметр диапазона, на выходе выдавая:
        1. Расходы
        2. Поступления
        3. Курс валют
        4. Стоимость акций из S&P 500
    """

    expenses = None  # 1. Расходы
    total_outcome = 0
    transfer_and_cash = None

    receipts = None  # 2. Поступления
    total_income = 0

    rate = exchange_rate()  # 3. Курс валют

    stock_prices = stock_price()  # 4. Стоимость акций

    event_page_answer = {
        "expenses": {
            "total amount": total_outcome,
            "main": [expenses],
            "transfers_and_cash": [transfer_and_cash]
        },
        "income": {
            "total_amount": total_income,
            "main": [receipts]
        },
        "currency_rates": [rate],
        "stock_prices": [stock_prices]

    }

    return event_page_answer  # возвращается корректный JSON-ответ согласно ТЗ
