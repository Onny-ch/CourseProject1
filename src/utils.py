from typing import Any

import pandas as pd


def greetings(time_string: str) -> str:
    greetings_string = ''
    if '06:00' <= time_string < '10:00':
        greetings_string = 'Доброе утро'
    elif '10:00' <= time_string < '17:00':
        greetings_string = 'Доброе утро'
    elif '17:00' <= time_string < '22:00':
        greetings_string = 'Доброе утро'
    elif '22:00' <= time_string < '06:00':
        greetings_string = 'Доброе утро'
    return greetings_string


def read_xls(xls_file: str) -> list[dict[Any: Any]]:
    """Функция считывания финансовых операций из Excel файла"""
    df = pd.read_excel(xls_file)

    transactions_data = df.to_dict(orient="records")
    return transactions_data
