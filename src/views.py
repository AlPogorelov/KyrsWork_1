import datetime
import json
import math
import os
import pandas as pd
import requests
import reviews
from dotenv import load_dotenv



def open_xlsx(file_name):
    """Функция открывет excel файл и преобразует его в список словарей"""
    df = pd.read_excel(file_name)
    excel_file = df.to_dict(orient="records")
    return excel_file


file_name = '../data/operations.xlsx'


def list_card_not_null(file_name):
    '''Функция принимает путь файла с транзакциями и отдает список карт
     исключающие пустые строки сталбца 'Номер карты'
    '''
    reviews = pd.read_excel(file_name)
    re_ = reviews['Номер карты']
    not_null = re_.loc[reviews['Номер карты'].notnull()]
    list_cards = pd.Series(not_null).unique().tolist()
    return list_cards


def summ(operations, list_card):
    '''Функция принимает список словарей с транзакциями, а выдает спискос ловарей с информацией по каждой карте
     '''
    cashback = 0
    total_spent = 0
    cards_total_info = []
    for card in list_card:
        card_info = [operation for operation in operations if operation['Номер карты'] == card]
        total_spent = sum(d.get('Сумма платежа', 0) for d in card_info)
        card_cashback_info = [info for info in card_info if not math.isnan(info['Кэшбэк'])]
        cashback = sum(d.get('Кэшбэк') for d in card_cashback_info)
        card_dict_info = {'last_digits': card[1:],
                          'total_spent': round(total_spent, 2),
                          'cashback': cashback
                          }
        cards_total_info.append(card_dict_info)
    return cards_total_info


def hello_user():
    '''Функция на оснвое реального приветствует пользователя'''

    time = datetime.datetime.now()
    format_time = time.strftime('%H')
    if format_time in ['22','23','0','1','2','3','4']:
        hello = 'Доброй ночи!'
    elif format_time in ['5','6','7','8','9','10','11']:
        hello = 'Доброе утро!'
    elif format_time in ['12','13','14','15','16']:
        hello = 'Добрый день!'
    elif format_time in ['17','18','19','20','21']:
        hello = 'Доброго вечера!'
    return hello


def top_five_transaction(operations):
    '''Функция принимает список словарей транзакций и
    выводит иформацию по топ 5 транзакций по сумму платежа'''

    operat_ = sorted(operations, key=lambda data: data["Сумма платежа"], reverse=True)
    top_five = operat_[:6]
    dict_top_five = []
    for i in top_five:
        dict_transaction = {'date': i['Дата платежа'],
                            'amount': i['Сумма платежа'],
                            'category': i['Категория'],
                            'descriction': i['Описание']
                            }
        dict_top_five.append(dict_transaction)
    return dict_top_five


def currency_rate():
    '''Функция выдает курс валют из списка user_settings.json'''

    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    currency_rates = []

    with open('../user_settings.json', encoding='utf-8') as f:
        user_settings = json.load(f)

    symbol = user_settings['user_currencies']
    for i in symbol:
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={i}&base=RUB"

        payload = {}
        headers = {
            "apikey": API_KEY
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        status_code = response.status_code
        result = response.json()
        currency = {'currency': i,
                          'rate': round(1/(result['rates'][i]), 2)
                          }

        currency_rates.append(currency)
    return currency_rates


def stock_prices():
    '''Функция по API получает данный о цене акций компаний указанных в user_settings.json'''

    load_dotenv()

    API_KEY = os.getenv("API_KEY_STACK")

    currency_rates = []

    with open('../user_settings.json') as f:
        user_settings = json.load(f)

    symbol = user_settings['user_stocks']

    for i in symbol:

        url = f"https://finnhub.io/api/v1/quote?symbol={i}&token={API_KEY}"

        response = requests.get(url)
        result = response.json()
        stock = {"stock": i,
                 "price": result['c']
                 }
        currency_rates.append(stock)
    return currency_rates


def sort_date_operations(operations, date):
    '''Функция отсортирвоала список словарей создав список словаряй со словарями входящими в
    промежуток времени от начала месца вводимой даты по дату'''

    date_ = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    date_new = date_.strftime("%d-%m-%Y %H:%M:%S")
    start_date = f'01{date_new[2:]}'
    date_new = pd.to_datetime(date_new, dayfirst=True)
    start_date = pd.to_datetime(start_date, dayfirst=True)
    sort_date_oper = []
    for i in operations:
        i['Дата операции'] = pd.to_datetime(i['Дата операции'], dayfirst=True)
        if i['Дата операции'] >= start_date and i['Дата операции'] <= date_new:
            sort_date_oper.append(i)
    for i in sort_date_oper:
        i['Дата операции'] = i['Дата операции'].strftime("%d-%m-%Y %H:%M:%S")

    return sort_date_oper


def web_main_def(date):
    file_name = '../data/operations.xlsx'
    operations = open_xlsx(file_name)
    operations = sort_date_operations(operations, date)
    card_list = list_card_not_null(file_name)
    cards = summ(operations, card_list)
    top_transactions = top_five_transaction(operations)
    currency_rates = currency_rate()
    stock_price = stock_prices()
    hello = hello_user()

    otvet_json = {'greeting': hello,
                  'cards': cards,
                  'top_transactions': top_transactions,
                  'currency_rates': currency_rates,
                  'stock_prices': stock_price
                  }

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(otvet_json, f)








if __name__ == '__main__':
    # print(list_card_not_null(file_name))
    # x = open_xlsx(file_name)
    # list_card = list_card_not_null(file_name)
    # print(summ(x,list_card))
    # print(hello_user())
    # print(top_five_transaction(x))
    # print(currency_rate())
    # print(stock_prices())
    web_main_def('2021-12-03 19:05:50')




