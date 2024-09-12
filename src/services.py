import datetime
import json
import logging
import os

import pandas as pd

from src.views import open_xlsx

current_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем путь до файла логов относительно текущей директории
rel_file_path = os.path.join(current_dir, "../logs/services.log")
abs_file_path = os.path.abspath(rel_file_path)

services_logger = logging.getLogger("services.py")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
services_logger.addHandler(file_handler)
services_logger.setLevel(logging.DEBUG)


def investment_bank(month, transactions, limit):
    """Функция принимает дату в вормате 'YYYY-MM', список словарей транзакций и
    шаг окгугления суммы операций на выходе получаем сумму которую
     можно было бы отложить в инвест копилку в этом месяце"""

    services_logger.info("Функция начала работу")

    sum_invest_month = 0
    start_month_ = month + "-01"
    start_month = datetime.datetime.strptime(start_month_, "%Y-%m-%d")

    end_month_ = month + "-31"
    end_month = datetime.datetime.strptime(end_month_, "%Y-%m-%d")

    df = pd.DataFrame(transactions)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    sort_trans_date = df[df["Дата операции"].between(start_month, end_month)]

    for i in sort_trans_date["Сумма операции"]:
        sum_point = 0

        while round(i, 0) % limit != 0:
            i += 1
            sum_point += 1

        sum_invest_month += sum_point

    sum_invest_month_json = json.dumps(sum_invest_month)

    services_logger.info("Функция закончила работу и получила сумму в Инвесткопилку в формате JSON")

    return sum_invest_month_json
