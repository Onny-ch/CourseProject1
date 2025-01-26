import datetime
import json
import logging
import re
from typing import Any
import pandas as pd
import numpy as np
import math


from src.utils import read_xls


def best_cashback_categories(file_info: pd.DataFrame, year: str, month: str) -> json:
    """
    Функция позволяет проанализировать, какие категории были наиболее выгодными
    для выбора в качестве категорий повышенного кэшбека
    """
    category_list = []

    nan_check_cashback = file_info["Кэшбэк"].notnull()

    year_datetime = datetime.datetime.strptime(f"{year}.{month}", "%Y.%m")

    year_datetime_range = datetime.datetime.strptime(f"{year}.{int(month)+1}", "%Y.%m")
    year_datetime_range = year_datetime_range - datetime.timedelta(seconds=1)

    for i in file_info.index:
        trans_datetime = datetime.datetime.strptime(file_info.loc[i, "Дата операции"], "%d.%m.%Y %H:%M:%S")

        if year_datetime < trans_datetime < year_datetime_range:
            if nan_check_cashback[i]:
                found = False

                for eel in category_list:
                    if file_info.loc[i, "Категория"] == eel["Категория"]:
                        eel["Кэшбэк"] += file_info.loc[i, "Кэшбэк"].item()

                        found = True

                if not found:
                    category_list.append({
                        "Категория": file_info.loc[i, "Категория"],
                        "Кэшбэк": file_info.loc[i, "Кэшбэк"].item()
                    })

    sorted_category_list = sorted(category_list, key=lambda x: x["Кэшбэк"], reverse=True)

    cashback_categories = {}

    for i in range(0, 3):
        try:
            cashback_categories.update({
                sorted_category_list[i]["Категория"]: sorted_category_list[i]["Кэшбэк"],
            })
        except IndexError:
            pass

    json_cashback_categories = json.dumps(cashback_categories, ensure_ascii=False)

    return json_cashback_categories


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int = 50) -> float:  # в работе
    """Функция, высчитывающая сумму денег, которую удалось бы отложить в 'Инвесткопилку'"""
    month_datetime = datetime.datetime.strptime(month, "%Y-%m")

    month_datetime_range = datetime.datetime.strptime(f"{month[0:5]}{int(month[-2:])+1}", "%Y-%m")
    month_datetime_range = month_datetime_range - datetime.timedelta(seconds=1)

    total_invest = 0

    for el in transactions:
        trans_datetime = datetime.datetime.strptime(el["Дата операции"], "%d.%m.%Y %H:%M:%S")

        if month_datetime < trans_datetime < month_datetime_range:
            if el["Сумма операции"] < 0:
                difference = math.ceil(-el["Сумма операции"] / limit) * limit
                total_invest += difference + el["Сумма операции"]

    # json, datetime, logging
    return round(total_invest, 2)


def simple_search(transactions, search_string: str) -> json:  # в работе
    """Функция, производящая поиск по запросу среди транзакций, содержащих запрос в описании или категории."""

    all_transactions = []

    for el in transactions:
        if not pd.isna(el["Категория"]):
            if search_string.lower() in el["Описание"].lower() or search_string.lower() in el["Категория"].lower():
                all_transactions.append(el)

    json_answer = json.dumps(all_transactions, ensure_ascii=False)

    # json, logging
    return json_answer  # возвращает корректный JSON-ответ


def phone_number_search(transactions_list: list[dict[str, Any]]) -> json:  # в работе
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""

    # json, logging, re
    return "correct json-answer"  # возвращает корректный JSON-ответ


def search_for_transfers_to_individuals(transactions_list: list[dict[str, Any]]) -> json:  # в работе
    """Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам."""
    transactions_data = read_xls('data\\operations.xlsx')
    pattern = re.compile(r'(а-я){+}')

    list_of_transfers = [elem
                         for elem in transactions_data
                         if elem["Категория"] == "Переводы"
                         and pattern.search(elem["Описание"], re.IGNORECASE)]
    json_with_cat = json.dumps(list_of_transfers, ensure_ascii=False, indent=4)

    # json, logging, re
    return json_with_cat
