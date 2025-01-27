import logging
import datetime
import json
import calendar

import pandas as pd


# def write_in_file():
#     def wrapper(func):
#         def inner():
#             with open("data\\reports.txt", "a") as file:
#                 file.write(func())
#         return inner
#     return wrapper


def expenses_by_category(
        df: pd.DataFrame,
        category_name: str,
        optional_date: str = datetime.datetime.isoformat(datetime.datetime.now(), sep=" ")
) -> str:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)"""

    starting_date = datetime.datetime.strptime(optional_date[:19], "%Y-%m-%d %H:%M:%S")
    ending_date = datetime.datetime.strptime(optional_date[:19], "%Y-%m-%d %H:%M:%S")

    suitable_transactions = []

    for i in range(0, 3):
        days_in_month = calendar.monthrange(ending_date.year, ending_date.month)[1]
        ending_date -= datetime.timedelta(days=days_in_month)

    for index, row in df.iterrows():
        transaction_date = datetime.datetime.strptime(df.loc[index, "Дата операции"], "%d.%m.%Y %H:%M:%S")

        if ending_date < transaction_date < starting_date:
            if df.loc[index, "Категория"] == category_name:
                if df.loc[index, "Сумма операции"] < 0:
                    suitable_transactions.append(row.to_dict())

    json_answer = json.dumps(suitable_transactions, ensure_ascii=False, indent=4)

    return json_answer


def spending_by_weekday(
        df: pd.DataFrame,
        optional_date: str = datetime.datetime.isoformat(datetime.datetime.now(), sep=" ")
) -> str:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты)"""

    starting_date = datetime.datetime.strptime(optional_date[:19], "%Y-%m-%d %H:%M:%S")
    ending_date = datetime.datetime.strptime(optional_date[:19], "%Y-%m-%d %H:%M:%S")

    for i in range(0, 3):
        days_in_month = calendar.monthrange(ending_date.year, ending_date.month)[1]
        ending_date -= datetime.timedelta(days=days_in_month)

    amount_of_days_of_the_week = [{0: 0}, {1: 0}, {2: 0}, {3: 0}, {4: 0}, {5: 0}, {6: 0}]  # траты в каждый из дней
    counter_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}  # кол-во трат в каждый из дней недели

    for i in df.index:
        transaction_date = datetime.datetime.strptime(df.loc[i, "Дата операции"], "%d.%m.%Y %H:%M:%S")

        if ending_date < transaction_date < starting_date:
            if df.loc[i, "Сумма операции"] < 0:
                actual_day_of_the_week = datetime.datetime.weekday(transaction_date)

                for day in amount_of_days_of_the_week:
                    for key in day.keys():
                        if key == actual_day_of_the_week:
                            day.update({key: day[key] + df.loc[i, "Сумма операции"].item()})
                            counter_dict.update({key: counter_dict[key] + 1})

    average_spending = [{
        "Понедельник": -round(amount_of_days_of_the_week[0][0] / counter_dict[0], 2),
        "Вторник": -round(amount_of_days_of_the_week[1][1] / counter_dict[1], 2),
        "Среда": -round(amount_of_days_of_the_week[2][2] / counter_dict[2], 2),
        "Четверг": -round(amount_of_days_of_the_week[3][3] / counter_dict[3], 2),
        "Пятница": -round(amount_of_days_of_the_week[4][4] / counter_dict[4], 2),
        "Суббота": -round(amount_of_days_of_the_week[5][5] / counter_dict[5], 2),
        "Воскресенье": -round(amount_of_days_of_the_week[6][6] / counter_dict[6], 2)
    }]  # средние траты в каждый из дней недели

    json_answer = json.dumps(average_spending, ensure_ascii=False, indent=4)

    return json_answer


def spending_of_wor_or_wee_days(
        df: pd.DataFrame,
        optional_date: str = datetime.datetime.isoformat(datetime.datetime.now(), sep=" ")
) -> str:
    """Функция выводит средние траты в рабочие и в выходные дни за последние три месяца (от переданной даты)"""

    starting_date = datetime.datetime.strptime(optional_date[:19], "%Y-%m-%d %H:%M:%S")
    ending_date = datetime.datetime.strptime(optional_date[:19], "%Y-%m-%d %H:%M:%S")

    for i in range(0, 3):
        days_in_month = calendar.monthrange(ending_date.year, ending_date.month)[1]
        ending_date -= datetime.timedelta(days=days_in_month)

    workdays_list = {"amount": 0, "counter": 0}  # количество и счетчик трат в рабочие дни
    weekdays_list = {"amount": 0, "counter": 0}  # количество и счетчик трат в выходные дни

    for i in df.index:
        transaction_date = datetime.datetime.strptime(df.loc[i, "Дата операции"], "%d.%m.%Y %H:%M:%S")

        if ending_date < transaction_date < starting_date:
            if df.loc[i, "Сумма операции"] < 0:
                actual_day_of_the_week = datetime.datetime.weekday(transaction_date)

                if actual_day_of_the_week < 5:
                    workdays_list.update({
                        "amount": workdays_list["amount"] + df.loc[i, "Сумма операции"].item(),
                        "counter": workdays_list["counter"] + 1
                    })
                else:
                    weekdays_list.update({
                        "amount": weekdays_list["amount"] + df.loc[i, "Сумма операции"].item(),
                        "counter": weekdays_list["counter"] + 1
                    })

    average_spending = [{
        "workdays": -round(workdays_list["amount"] / workdays_list["counter"], 2),
        "weekdays": -round(weekdays_list["amount"] / weekdays_list["counter"], 2)
    }]  # средние траты в рабочие и выходные дни

    json_answer = json.dumps(average_spending, ensure_ascii=False, indent=4)

    return json_answer
