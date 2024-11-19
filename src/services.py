import json
import re
from typing import Any

from src.utils import read_xls


def best_cashback_categories(trans_data: json, year: str, month: str) -> json:
    """
    Функция позволяет проанализировать, какие категории были наиболее выгодными
    для выобора в качестве категорий повышенного кэшбека
    """

    # json, datetime, logging, pytest
    pass
# Формат выходных данных:
#
# {
#     "Категория 1": 1000,
#     "Категория 2": 2000,
#     "Категория 3": 500
# }


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int = 50) -> float:
    """Функция, высчитывающая сумму денег. которую удалось бы отложить в 'Инвесткопилку'"""
    pass


def simple_search(search_string: str) -> json:
    """Функция, производящая поиск по запросу среди транзакций, содержащими запрос в описании или категории."""
    # Пользователь передает строку для поиска, возвращается JSON - ответ со
    # всеми транзакциями, содержащими запрос в описании или категории.
    pass


def phone_number_search() -> json:
    """Функция возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""
    pass


def search_for_transfers_to_individuals():
    """Функция возвращает JSON со всеми транзакциями, которые относятся к переводам физлицам."""
    transactions_data = read_xls('data\\operations.xlsx')
    pattern = re.compile(r'(а-я){+}')

    list_of_transfers = [elem
                         for elem in transactions_data
                         if elem["Категория"] == "Переводы"
                         and pattern.search(elem["Описание"], re.IGNORECASE)]
    json_with_cat = json.dumps(list_of_transfers, ensure_ascii=False, indent=4)

    return json_with_cat
