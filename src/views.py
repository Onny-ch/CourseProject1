import json

import pandas as pd

from src.utils import (
    card_information,
    exchange_rate,
    expenses_calculator,
    greetings,
    income_calculator,
    read_xls,
    stock_price,
    top_five_by_trans_amount,
)

with open("user_settings.json", "r") as file:
    user_data = json.load(file)

file_info = read_xls("data\\operations.xlsx")
file_info_pd = pd.read_excel("data\\operations.xlsx")


# Функция для страницы "Главная"
def home_page(date_time_string: str) -> str:  # готова
    """
    Принимает строку с датой и возвращает информацию в виде:
        1. Приветствие в соответствии с временем суток
        2. Общую информацию по каждой карте
        3. Топ-5 транзакций по сумме платежа
        4. Курс валют
        5. Стоимость акций из S&p500
    """

    greet_string = greetings(date_time_string)  # 1 Приветствие

    card_info = card_information(file_info)  # 2 Инфо по карте

    top_5 = top_five_by_trans_amount(date_time_string, file_info)  # 3 Топ 5 по сумме транзакций

    rate = exchange_rate(user_data)  # 4 Курс валют

    stocks_prices = stock_price(user_data)  # 5 Стоимость акций

    home_page_answer = {
        "greetings": greet_string,
        "cards": card_info,
        "top_transactions": top_5,
        "currency_rates": rate,
        "stock_prices": stocks_prices,
    }

    json_home_page = json.dumps(home_page_answer, ensure_ascii=False)

    return json_home_page


def event_page(actual_date_string: str, date_range: str = "M") -> str:
    """
    Принимает на вход дату и параметр диапазона, на выходе выдавая:
        1. Расходы
        2. Поступления
        3. Курс валют
        4. Стоимость акций из S&P 500
    """

    expenses = expenses_calculator(file_info_pd, actual_date_string, date_range)  # 1. Расходы

    income = income_calculator(file_info_pd, actual_date_string, date_range)  # 2. Поступления

    rate = exchange_rate(user_data)  # 3. Курс валют

    stock_prices = stock_price(user_data)  # 4. Стоимость акций

    event_page_answer = {
        "expenses": {
            "total amount": expenses["total_amount"],
            "main": expenses["main"],
            "transfers_and_cash": expenses["transfers_and_cash"],
        },
        "income": {"total_amount": income["total_amount"], "main": income["main"]},
        "currency_rates": rate,
        "stock_prices": stock_prices,
    }

    json_event_page = json.dumps(event_page_answer, ensure_ascii=False)

    return json_event_page
