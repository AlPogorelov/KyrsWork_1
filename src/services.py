import datetime

import pandas as pd

from src.views import open_xlsx


def investment_bank(month, transactions, limit):
    '''Функция принимает дату в вормате 'YYYY-MM', список словарей транзакций и
     шаг окгугления суммы операцииб на выходе получаем сумму которую
      можно было бы отложить в инвест копилку в этом месяце '''

    sum_invest_month = 0
    start_month_ = month+'-01'
    start_month = datetime.datetime.strptime(start_month_, "%Y-%m-%d")

    end_month_ = month+'-31'
    end_month = datetime.datetime.strptime(end_month_, "%Y-%m-%d")

    df = pd.DataFrame(operations)

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

    sort_trans_date = df[df['Дата операции'].between(start_month, end_month)]

    for i in sort_trans_date['Сумма операции']:
        sum_point = 0

        while round(i, 0) % limit != 0:
            i += 1
            sum_point += 1

        sum_invest_month += sum_point
    return sum_invest_month


if __name__ == '__main__':
    operations = open_xlsx('../data/operations.xlsx')
    print(investment_bank('2020-03', operations, 10))
    # print(x)
