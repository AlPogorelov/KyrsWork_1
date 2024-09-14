import pandas as pd

from src.reports import spending_by_category
from src.views import open_xlsx

test_data = {'Дата операции': ['2021-10-22', '2021-07-15', '2021-08-09', '2021-09-01'],
             'Категория': ['Перевод', 'Супер маркет', 'Цветы', 'Фастфуд'],
             'Сумма': [10, 20, 30, 40]}

df = pd.DataFrame(test_data)

def test_reports():
    result = spending_by_category(df, 'Перевод', '2021-11-22 10:10:10')
    expected = {'Дата операции': '2021-10-22', 'Категория': 'Перевод', 'Сумма': 10}
    assert (result == expected).all().all()
