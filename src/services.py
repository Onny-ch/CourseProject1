import datetime
import json
import logging
import re
from typing import Any

from src.utils import read_xls


def best_cashback_categories(trans_data: json, year: str, month: str) -> json:  # в работе
    """
    Функция позволяет проанализировать, какие категории были наиболее выгодными
    для выбора в качестве категорий повышенного кэшбека
    """

    # json, datetime, logging
    return "ass"  # возвращает корректный JSON-ответ
# Формат выходных данных:
#
# {
#     "Категория 1": 1000,
#     "Категория 2": 2000,
#     "Категория 3": 500
# }


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int = 50) -> json:  # в работе
    """Функция, высчитывающая сумму денег, которую удалось бы отложить в 'Инвесткопилку'"""

    # json, datetime, logging
    return "sas"  # возвращает корректный JSON-ответ


def simple_search(search_string: str) -> json:  # в работе
    """Функция, производящая поиск по запросу среди транзакций, содержащих запрос в описании или категории."""

    # Пользователь передает строку для поиска, возвращается JSON - ответ со
    # всеми транзакциями, содержащими запрос в описании или категории.
    # json, logging
    return "json-answer"  # возвращает корректный JSON-ответ


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
