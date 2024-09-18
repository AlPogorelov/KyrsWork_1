import csv
import datetime
import logging
import os

import pandas as pd
from dateutil.relativedelta import relativedelta

current_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем путь до файла логов относительно текущей директории
rel_file_path = os.path.join(current_dir, "../logs/reports.log")
abs_file_path = os.path.abspath(rel_file_path)

reports_logger = logging.getLogger("reports.py")
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(funcName)s: %(message)s")
file_handler.setFormatter(file_formatter)
reports_logger.addHandler(file_handler)
reports_logger.setLevel(logging.DEBUG)


def save_result_func(file_name="reports.csv"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_name, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(result)
            return result

        return wrapper

    return decorator


@save_result_func()
def spending_by_category(transaction, category, date=None):
    """Функция принимает дата фрейм c транзакциями, название категории
    и опциональную дату (по умолчанию настоящее время) на выходе
     Датафрейм с тратами по заданной категории за последние 3 месяца с введенной даты"""

    reports_logger.info("Начало работы функции.")

    df = pd.DataFrame(transaction)

    if date is None:
        date_ = datetime.datetime.now()
        start_date = date_ - relativedelta(months=3)
    else:
        date_ = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_date = date_ - relativedelta(months=3)

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    sort_trans_date = df[df["Дата операции"].between(start_date, date_)]
    filter_df_category = sort_trans_date[sort_trans_date["Категория"].apply(lambda x: category in x)]

    reports_logger.info("Конец работы функции.")

    return filter_df_category
