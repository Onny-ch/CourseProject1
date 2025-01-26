import datetime
import time
from typing import Any

import pandas as pd
import requests


def read_xls(xls_file: str) -> list[Any]:
    """Функция считывания финансовых операций из Excel файла"""

    df = pd.read_excel(xls_file)
    transactions_data = df.to_dict(orient="records")

    return transactions_data


def greetings(time_string: str) -> str:
    """Функция приветствия пользователя, меняющаяся от времени суток"""

    greetings_string = ""
    ttt = time.strptime(time_string, "%Y-%m-%d %H:%M:%S")

    if 6 <= ttt[3] < 10:
        greetings_string = "Доброе утро"
    elif 10 <= ttt[3] < 17:
        greetings_string = "Добрый день"
    elif 17 <= ttt[3] < 22:
        greetings_string = "Добрый вечер"
    elif 22 <= ttt[3] < 24 or 00 <= ttt[3] < 6:
        greetings_string = "Доброй ночи"

    return greetings_string


def card_information(transactions_data: list[dict[Any, Any]]) -> list[dict[str, Any]]:
    """
    Информация по каждой карте:
        1. Последние 4 цифры карты,
        2. Общая сумма расходов,
        3. Кэшбек (1 рубль на каждые 100 рублей)
    """

    expenses_amount = list()
    card_numbers = list()

    for transaction in transactions_data:
        if type(transaction["Номер карты"]) is str:
            if transaction["Номер карты"] not in card_numbers:
                card_numbers.append(transaction["Номер карты"])

    for card in card_numbers:
        total_spent = float()
        cashback = float()
        for transaction in transactions_data:
            if card is transaction["Номер карты"]:
                if int(transaction["Сумма операции"]) < 0:
                    total_spent += float(transaction["Сумма операции"])
                    cashback += float(transaction["Сумма операции"]) / 100
        expenses_amount.append(
            {"last_digits": card[1:], "total_spent": round(total_spent, 1), "cashback": round(cashback, 1)}
        )

    return expenses_amount


def top_five_by_trans_amount(transactions_date: str, transactions_data: list[dict[Any, Any]]) -> list[dict[Any, Any]]:
    """
    Сортировка списка транзакций по 'Сумме платежа' и возврат 5 самых дорогих в виде:
        {
        "date": "21.12.2021",
        "amount": 1198.23,
        "category": "Переводы",
        "description": "Перевод Кредитная карта. ТП 10.2 RUR"      2020-12-17 05:00:00
        }
    """

    sorted_transactions_by_time = []
    actual_data = []

    start_month_date = time.strptime(f"{transactions_date[:8]}01{transactions_date[10:]}", "%Y-%m-%d %H:%M:%S")
    actual_date = time.strptime(transactions_date, "%Y-%m-%d %H:%M:%S")

    for transaction in transactions_data:
        transaction_date = time.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")

        if actual_date > transaction_date > start_month_date:
            actual_data.append(transaction)

    sorted_data = sorted(actual_data, key=lambda x: x["Сумма платежа"])

    for transaction in sorted_data[:5]:
        sorted_transactions_by_time.append(
            {
                "date": transaction["Дата операции"][:10],
                "amount": transaction["Сумма операции"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )

    return sorted_transactions_by_time


def expenses_calculator(df: pd.DataFrame, transactions_date: str, date_range: str) -> dict[Any, Any]:
    """Расчет всех расходов в заданном диапазоне (неделя, месяц, год или за все время"""

    actual_date_time = time.strptime(transactions_date, "%Y-%m-%d %H:%M:%S")

    actual_date_datetime = datetime.datetime.strptime(transactions_date, "%Y-%m-%d %H:%M:%S")

    range_date_datetime = datetime.datetime.strptime(transactions_date, "%Y-%m-%d %H:%M:%S")

    if date_range == "W":
        range_date_datetime = range_date_datetime - datetime.timedelta(days=actual_date_time.tm_wday)
        range_date_datetime = range_date_datetime.replace(hour=0, minute=0, second=0)

    elif date_range == "M":
        range_date_datetime = range_date_datetime.replace(day=1, hour=0, minute=0, second=0)

    elif date_range == "Y":
        range_date_datetime = range_date_datetime.replace(month=1, day=1, hour=0, minute=0, second=0)

    elif date_range == "ALL":
        range_date_datetime = range_date_datetime.replace(year=1970, month=1, day=1, hour=0, minute=0, second=0)

    amount = 0

    category_list: list[dict[str, Any]] = []

    nan_check_summ = df["Сумма операции"].notnull()
    nan_check_cat = df["Категория"].notnull()

    for i in df.index:
        datetime_for_i = datetime.datetime.strptime(df.loc[i, "Дата операции"], "%d.%m.%Y %H:%M:%S")

        if range_date_datetime < datetime_for_i < actual_date_datetime:
            if df.loc[i, "Сумма операции"] < 0:
                amount += df.loc[i, "Сумма операции"].item()

                if nan_check_summ[i] and nan_check_cat[i]:

                    found = False

                    for cat in category_list:
                        if df.loc[i, "Категория"] == cat["category"]:
                            cat["amount"] += df.loc[i, "Сумма операции"].item()
                            found = True
                            break

                    if not found:
                        category_list.append(
                            {"category": df.loc[i, "Категория"], "amount": df.loc[i, "Сумма операции"].item()}
                        )

                else:
                    found = False

                    for cat in category_list:
                        if cat["category"] == "Остальное":
                            cat["amount"] += df.loc[i, "Сумма операции"].item()
                            found = True
                            break

                    if not found:
                        category_list.append({"category": "Остальное", "amount": df.loc[i, "Сумма операции"].item()})

    total_amount = round(amount, 2)

    transfers_and_cash = []

    category_other = dict()

    for el in category_list:
        if el["category"] == "Наличные" or el["category"] == "Переводы":
            el["amount"] = round(el["amount"], 2)
            transfers_and_cash.append(el)
            category_list.remove(el)

        elif el["category"] == "Остальное":
            el["amount"] = round(el["amount"], 2)
            category_other = el
            category_list.remove(el)

    category_list.sort(key=lambda x: x["amount"])

    main = []

    for elem in category_list[:7]:
        main.append({"category": elem["category"], "amount": round(elem["amount"], 2)})

    main.append(category_other)

    try:
        transfers = next(el["amount"] for el in transfers_and_cash if el["category"] == "Переводы")
    except StopIteration:
        transfers = 0

    try:
        cash = next(el["amount"] for el in transfers_and_cash if el["category"] == "Наличные")
    except StopIteration:
        cash = 0

    expenses = {
        "total_amount": total_amount,
        "main": main,
        "transfers_and_cash": [
            {
                "category": "Наличные",
                "amount": cash,
            },
            {
                "category": "Переводы",
                "amount": transfers,
            },
        ],
    }

    return expenses


def income_calculator(df: pd.DataFrame, transactions_date: str, date_range: str) -> dict[Any, Any]:
    """Расчет всех приходов в заданном диапазоне (неделя, месяц, год или за все время"""

    actual_date_time = time.strptime(transactions_date, "%Y-%m-%d %H:%M:%S")
    actual_date_datetime = datetime.datetime.strptime(transactions_date, "%Y-%m-%d %H:%M:%S")
    range_date_datetime = datetime.datetime.strptime(transactions_date, "%Y-%m-%d %H:%M:%S")

    if date_range == "W":
        range_date_datetime = range_date_datetime - datetime.timedelta(days=actual_date_time.tm_wday)
        range_date_datetime = range_date_datetime.replace(hour=0, minute=0, second=0)
    elif date_range == "M":
        range_date_datetime = range_date_datetime.replace(day=1, hour=0, minute=0, second=0)
    elif date_range == "Y":
        range_date_datetime = range_date_datetime.replace(month=1, day=1, hour=0, minute=0, second=0)
    elif date_range == "ALL":
        range_date_datetime = range_date_datetime.replace(year=1970, month=1, day=1, hour=0, minute=0, second=0)

    amount = 0

    category_list: list[dict[str, Any]] = []

    nan_check_summ = df["Сумма операции"].notnull()
    nan_check_cat = df["Категория"].notnull()

    for i in df.index:
        datetime_for_i = datetime.datetime.strptime(df.loc[i, "Дата операции"], "%d.%m.%Y %H:%M:%S")

        if range_date_datetime < datetime_for_i < actual_date_datetime:
            if df.loc[i, "Сумма операции"] > 0:
                amount += df.loc[i, "Сумма операции"].item()

                if nan_check_summ[i] and nan_check_cat[i]:

                    found = False

                    for cat in category_list:
                        if df.loc[i, "Категория"] == cat["category"]:
                            cat["amount"] += df.loc[i, "Сумма операции"].item()
                            found = True
                            break

                    if not found:
                        category_list.append(
                            {"category": df.loc[i, "Категория"], "amount": df.loc[i, "Сумма операции"].item()}
                        )

                else:
                    found = False

                    for cat in category_list:
                        if cat["category"] == "Остальное":
                            cat["amount"] += df.loc[i, "Сумма операции"].item()
                            found = True
                            break

                    if not found:
                        category_list.append({"category": "Остальное", "amount": df.loc[i, "Сумма операции"].item()})

    total_amount = round(amount, 2)

    category_list.sort(key=lambda x: x["amount"], reverse=True)

    income = {
        "total_amount": total_amount,
        "main": category_list,
    }

    return income


def exchange_rate(user_data: dict[str, list[str]]) -> list[dict[str, float]]:  # готова (Спрятать API)
    """Информация по курсу валют"""

    url = "https://api.apilayer.com/currency_data/live"

    headers = {
        "apikey": "IQ5ua48io6VZzoknLyni9aMqSvhkPybg",
    }

    params = {
        "source": "RUB",
    }

    currency_request = requests.get(url, headers=headers, params=params)
    json_currency_data = currency_request.json()

    currency_list = []

    for currency in user_data["user_currencies"]:
        currency_list.append(
            {"currency": currency, "rate": round(1 / json_currency_data["quotes"][f"RUB{currency}"], 2)}
        )

    return currency_list


def stock_price(user_data: dict[str, list[str]]) -> list[dict[str, str]]:  # готова (Спрятать API)
    """Стоимость акций из S&P500"""

    stock_prices = []

    for symbol in user_data["user_stocks"]:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=MGIXTPCAEN2ZSL0K"

        request_data = requests.get(url)
        json_stock_data = request_data.json()

        stock_prices.append(
            {
                "stock": json_stock_data["Global Quote"]["01. symbol"],
                "price": json_stock_data["Global Quote"]["02. open"],
            }
        )

    return stock_prices
