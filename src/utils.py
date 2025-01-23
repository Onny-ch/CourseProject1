import time
from typing import Any

import numpy as np
import pandas as pd
import requests


def read_xls(xls_file: str) -> list[Any]:  # готова
    """Функция считывания финансовых операций из Excel файла"""

    df = pd.read_excel(xls_file)
    transactions_data = df.to_dict(orient="records")

    return transactions_data


def greetings(time_string: str) -> str:  # готова
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


def card_information(transactions_data: list[dict[Any, Any]]) -> list[dict[str, Any]]:  # готова
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
                card_numbers.append(
                    transaction["Номер карты"]
                )  # Получаем список карт по которым будем искать информацию

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


def top_five_by_trans_amount(
    transactions_date: str, transactions_data: list[dict[Any, Any]]
) -> list[dict[Any, Any]]:  # готова
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


def expenses_calculator(df: pd.DataFrame, transactions_date: str) -> dict[Any, Any]:
    actual_date = time.strptime(transactions_date, "%Y-%m-%d %H:%M:%S")

    amount = 0

    category_list: list[dict[str, Any]] = []

    nan_check_summ = df["Сумма операции"].notnull()
    nan_check_cat = df["Категория"].notnull()

    for i in df.index:
        if time.strptime(df.loc[i, "Дата операции"].item(), "%d.%m.%Y %H:%M:%S") < actual_date:
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

    expenses = {
        "total_amount": total_amount,
        "main": main,
        "transfers_and_cash": [
            {
                "category": "Наличные",
                "amount": next(el["amount"] for el in transfers_and_cash if el["category"] == "Наличные"),
            },
            {
                "category": "Переводы",
                "amount": next(el["amount"] for el in transfers_and_cash if el["category"] == "Переводы"),
            },
        ],
    }

    return expenses


def income_calculator(df: pd.DataFrame, transactions_date: str) -> dict[Any, Any]:
    return dict()


def exchange_rate(user_data: dict[str, list[str]]) -> list[dict[str, float]]:  # готова (Спрятать API)
    """Информация по курсу валют"""

    url = "https://api.apilayer.com/currency_data/live"

    headers = {
        "apikey": "IQ5ua48io6VZzoknLyni9aMqSvhkPybg",
    }

    params = {
        "source": "RUB",
    }

    # currency_request = requests.get(url, headers=headers, params=params)
    # json_currency_data = currency_request.json()

    currency_list = []

    currencys = {
        "success": True,
        "timestamp": 1737614523,
        "source": "RUB",
        "quotes": {
            "RUBAED": 0.037009,
            "RUBAFN": 0.760069,
            "RUBALL": 0.952014,
            "RUBAMD": 4.057924,
            "RUBANG": 0.018228,
            "RUBAOA": 9.204359,
            "RUBARS": 10.552191,
            "RUBAUD": 0.016072,
            "RUBAWG": 0.018162,
            "RUBAZN": 0.017055,
            "RUBBAM": 0.018941,
            "RUBBBD": 0.02042,
            "RUBBDT": 1.233357,
            "RUBBGN": 0.018938,
            "RUBBHD": 0.003797,
            "RUBBIF": 29.926552,
            "RUBBMD": 0.010076,
            "RUBBND": 0.013686,
            "RUBBOB": 0.069885,
            "RUBBRL": 0.059889,
            "RUBBSD": 0.010114,
            "RUBBTC": 9.8209e-08,
            "RUBBTN": 0.874392,
            "RUBBWP": 0.139887,
            "RUBBYN": 0.033098,
            "RUBBYR": 197.488626,
            "RUBBZD": 0.020316,
            "RUBCAD": 0.014498,
            "RUBCDF": 28.66608,
            "RUBCHF": 0.009132,
            "RUBCLF": 0.000362,
            "RUBCLP": 9.988391,
            "RUBCNY": 0.073357,
            "RUBCNH": 0.073386,
            "RUBCOP": 42.933624,
            "RUBCRC": 5.086496,
            "RUBCUC": 0.010076,
            "RUBCUP": 0.267013,
            "RUBCVE": 1.067892,
            "RUBCZK": 0.243431,
            "RUBDJF": 1.800982,
            "RUBDKK": 0.072221,
            "RUBDOP": 0.620607,
            "RUBDZD": 1.364573,
            "RUBEGP": 0.507117,
            "RUBERN": 0.151139,
            "RUBETB": 1.293729,
            "RUBEUR": 0.009681,
            "RUBFJD": 0.023314,
            "RUBFKP": 0.008298,
            "RUBGBP": 0.008182,
            "RUBGEL": 0.028819,
            "RUBGGP": 0.008298,
            "RUBGHS": 0.153223,
            "RUBGIP": 0.008298,
            "RUBGMD": 0.735545,
            "RUBGNF": 87.426207,
            "RUBGTQ": 0.078175,
            "RUBGYD": 2.114963,
            "RUBHKD": 0.078497,
            "RUBHNL": 0.257482,
            "RUBHRK": 0.074356,
            "RUBHTG": 1.320739,
            "RUBHUF": 3.978484,
            "RUBIDR": 163.752833,
            "RUBILS": 0.035725,
            "RUBIMP": 0.008298,
            "RUBINR": 0.871041,
            "RUBIQD": 13.248654,
            "RUBIRR": 424.197506,
            "RUBISK": 1.414357,
            "RUBJEP": 0.008298,
            "RUBJMD": 1.586964,
            "RUBJOD": 0.007148,
            "RUBJPY": 1.577133,
            "RUBKES": 1.302316,
            "RUBKGS": 0.881141,
            "RUBKHR": 40.773716,
            "RUBKMF": 4.761876,
            "RUBKPW": 9.068356,
            "RUBKRW": 14.483826,
            "RUBKWD": 0.003106,
            "RUBKYD": 0.008429,
            "RUBKZT": 5.268521,
            "RUBLAK": 220.609648,
            "RUBLBP": 905.681101,
            "RUBLKR": 3.020199,
            "RUBLRD": 2.002503,
            "RUBLSL": 0.186857,
            "RUBLTL": 0.029752,
            "RUBLVL": 0.006095,
            "RUBLYD": 0.049751,
            "RUBMAD": 0.100917,
            "RUBMDL": 0.188621,
            "RUBMGA": 47.407463,
            "RUBMKD": 0.59561,
            "RUBMMK": 32.726294,
            "RUBMNT": 34.23808,
            "RUBMOP": 0.08113,
            "RUBMRU": 0.402833,
            "RUBMUR": 0.468732,
            "RUBMVR": 0.155273,
            "RUBMWK": 17.537372,
            "RUBMXN": 0.206556,
            "RUBMYR": 0.044773,
            "RUBMZN": 0.643958,
            "RUBNAD": 0.186857,
            "RUBNGN": 15.707603,
            "RUBNIO": 0.372193,
            "RUBNOK": 0.113698,
            "RUBNPR": 1.399058,
            "RUBNZD": 0.017785,
            "RUBOMR": 0.003879,
            "RUBPAB": 0.010114,
            "RUBPEN": 0.037724,
            "RUBPGK": 0.04118,
            "RUBPHP": 0.590939,
            "RUBPKR": 2.820205,
            "RUBPLN": 0.04089,
            "RUBPYG": 79.996299,
            "RUBQAR": 0.036913,
            "RUBRON": 0.04817,
            "RUBRSD": 1.133887,
            "RUBRWF": 14.18931,
            "RUBSAR": 0.037797,
            "RUBSBD": 0.085391,
            "RUBSCR": 0.149359,
            "RUBSDG": 6.055649,
            "RUBSEK": 0.110934,
            "RUBSGD": 0.013665,
            "RUBSHP": 0.008298,
            "RUBSLE": 0.228642,
            "RUBSLL": 211.287639,
            "RUBSOS": 5.779933,
            "RUBSRD": 0.353466,
            "RUBSTD": 208.551828,
            "RUBSVC": 0.0885,
            "RUBSYP": 131.007506,
            "RUBSZL": 0.186713,
            "RUBTHB": 0.341943,
            "RUBTJS": 0.110693,
            "RUBTMT": 0.035367,
            "RUBTND": 0.032101,
            "RUBTOP": 0.023599,
            "RUBTRY": 0.359331,
            "RUBTTD": 0.068704,
            "RUBTWD": 0.329811,
            "RUBTZS": 25.431699,
            "RUBUAH": 0.424784,
            "RUBUGX": 37.218617,
            "RUBUSD": 0.010076,
            "RUBUYU": 0.442599,
            "RUBUZS": 131.374067,
            "RUBVES": 0.561023,
            "RUBVND": 252.452935,
            "RUBVUV": 1.196237,
            "RUBWST": 0.028221,
            "RUBXAF": 6.352862,
            "RUBXAG": 0.000328,
            "RUBXAU": 3.65797e-06,
            "RUBXCD": 0.027231,
            "RUBXDR": 0.007792,
            "RUBXOF": 6.352801,
            "RUBXPF": 1.154996,
            "RUBYER": 2.509417,
            "RUBZAR": 0.186626,
            "RUBZMK": 90.695636,
            "RUBZMW": 0.281924,
            "RUBZWL": 3.244452,
        },
    }

    for currency in user_data["user_currencies"]:
        currency_list.append({"currency": currency, "rate": round(1 / currencys["quotes"][f"RUB{currency}"], 2)})

    return currency_list


def stock_price(user_data: dict[str, list[str]]) -> list[dict[str, str]]:  # готова (Спрятать API)
    """Стоимость акций из S&P500"""

    stock_prices = []
    stock_list = [
        {
            "Global Quote": {
                "01. symbol": "AAPL",
                "02. open": "219.7900",
                "03. high": "224.1200",
                "04. low": "219.7900",
                "05. price": "223.8300",
                "06. volume": "64126500",
                "07. latest trading day": "2025-01-22",
                "08. previous close": "222.6400",
                "09. change": "1.1900",
                "10. change percent": "0.5345%",
            }
        },
        {
            "Global Quote": {
                "01. symbol": "AMZN",
                "02. open": "232.0200",
                "03. high": "235.4400",
                "04. low": "231.1900",
                "05. price": "235.0100",
                "06. volume": "41448217",
                "07. latest trading day": "2025-01-22",
                "08. previous close": "230.7100",
                "09. change": "4.3000",
                "10. change percent": "1.8638%",
            }
        },
        {
            "Global Quote": {
                "01. symbol": "GOOGL",
                "02. open": "199.0600",
                "03. high": "200.4800",
                "04. low": "197.5300",
                "05. price": "198.3700",
                "06. volume": "26200617",
                "07. latest trading day": "2025-01-22",
                "08. previous close": "198.0500",
                "09. change": "0.3200",
                "10. change percent": "0.1616%",
            }
        },
        {
            "Global Quote": {
                "01. symbol": "MSFT",
                "02. open": "437.5600",
                "03. high": "447.2700",
                "04. low": "436.0000",
                "05. price": "446.2000",
                "06. volume": "27803811",
                "07. latest trading day": "2025-01-22",
                "08. previous close": "428.5000",
                "09. change": "17.7000",
                "10. change percent": "4.1307%",
            }
        },
        {
            "Global Quote": {
                "01. symbol": "TSLA",
                "02. open": "416.8100",
                "03. high": "428.0000",
                "04. low": "414.5900",
                "05. price": "415.1100",
                "06. volume": "58585801",
                "07. latest trading day": "2025-01-22",
                "08. previous close": "424.0700",
                "09. change": "-8.9600",
                "10. change percent": "-2.1129%",
            }
        },
    ]
    counter = 0

    for symbol in user_data["user_stocks"]:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=MGIXTPCAEN2ZSL0K"

        # request_data = requests.get(url)
        # json_stock_data = request_data.json()

        stock_prices.append(
            {
                "stock": stock_list[counter]["Global Quote"]["01. symbol"],
                "price": stock_list[counter]["Global Quote"]["02. open"],
            }
        )
        counter += 1

    return stock_prices
