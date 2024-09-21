import datetime
import os
from unittest.mock import patch

import pytest

from src.views import currency_rate, hello_user, list_card, open_xlsx, sort_date_operations, stock_prices, summ


@pytest.mark.parametrize(
    "mock_time, expected_greeting",
    [
        ("23:00", "Доброй ночи!"),
        ("06:00", "Доброе утро!"),
        ("14:00", "Добрый день!"),
        ("19:00", "Доброго вечера!"),
        ("03:00", "Доброй ночи!"),
        ("10:00", "Доброе утро!"),
        ("16:00", "Добрый день!"),
        ("21:00", "Доброго вечера!"),
    ],
)
def test_hello(mock_time, expected_greeting):

    time = datetime.datetime.strptime(mock_time, "%H:%M")

    mock_time = time

    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_time

        result = hello_user()
        assert result == expected_greeting


def tests_open_xlsx():
    file_name = "./tests/test.xlsx"
    full_file_name = os.path.abspath(file_name)

    df = open_xlsx(full_file_name)

    assert df == [
        {
            "Дата операции": "31.12.2021 16:44:00",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -160.89,
            "Валюта операции": "RUB",
            "Сумма платежа": -160.89,
            "Валюта платежа": "RUB",
            "Кэшбэк": 0,
            "Категория": "Супермаркеты",
            "MCC": 5411,
            "Описание": "Колхоз",
            "Бонусы (включая кэшбэк)": 3,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 160.89,
        },
        {
            "Дата операции": "31.12.2021 16:42:04",
            "Дата платежа": "31.12.2021",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -64.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -64.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 0,
            "Категория": "Супермаркеты",
            "MCC": 5411,
            "Описание": "Колхоз",
            "Бонусы (включая кэшбэк)": 1,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 64.0,
        },
    ]


def tests_list_card(operations):

    expected = ["*7197"]

    result = list_card(operations)
    assert result == expected


def test_summ(operations):

    list_card = ["*7197"]

    expect = [{"last_digits": "7197", "total_spent": -224.89, "cashback": 0}]

    result = summ(operations, list_card)
    assert result == expect


data_test = [
    {"Дата операции": "2023-05-05", "Сумма операции": 100, "Категория": "Продукты"},
    {"Дата операции": "2023-06-15", "Сумма операции": 150, "Категория": "Ресторан"},
    {"Дата операции": "2023-05-10", "Сумма операции": 200, "Категория": "Одежда"},
    {"Дата операции": "2023-05-11", "Сумма операции": 300, "Категория": "Продукты"},
    {"Дата операции": "2023-05-20", "Сумма операции": 250, "Категория": "Ресторан"},
    {"Дата операции": "2023-01-15", "Сумма операции": 120, "Категория": "Продукты"},
    {"Дата операции": "2023-01-20", "Сумма операции": 180, "Категория": "Ресторан"},
]


def test_sort_date_operations():
    result = sort_date_operations(data_test, "2023-01-30 00:00:00")
    expect = [
        {"Дата операции": "20-01-2023 00:00:00", "Сумма операции": 180, "Категория": "Ресторан"},
        {"Дата операции": "15-01-2023 00:00:00", "Сумма операции": 120, "Категория": "Продукты"},
    ]
    assert result == expect


# @patch('builtins.open', new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
@patch("requests.request")
def tests_currency_rate(mock_request):
    mock_response = mock_request.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "success": True,
        "timestamp": 1640995200,
        "base": "RUB",
        "rates": {"USD": 75.5, "EUR": 80.0},
    }
    result = currency_rate()
    expected = mock_response.json.return_value
    expected_result = [
        {"currency": "USD", "rate": round(1 / (expected["rates"]["USD"]), 2)},
        {"currency": "EUR", "rate": round(1 / (expected["rates"]["EUR"]), 2)},
    ]

    assert result == expected_result


@patch("requests.get")
def tests_stock_prices(mock_get):
    mock_response = {"c": 150.0}

    mock_get.return_value.json.return_value = mock_response

    result = stock_prices()

    expected_result = [
        {"price": 150.0, "stock": "AAPL"},
        {"price": 150.0, "stock": "AMZN"},
        {"price": 150.0, "stock": "GOOGL"},
        {"price": 150.0, "stock": "MSFT"},
        {"price": 150.0, "stock": "TSLA"},
    ]

    assert result == expected_result
