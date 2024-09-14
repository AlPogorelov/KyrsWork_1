import pandas as pd

from src.reports import spending_by_category
from src.services import investment_bank
from src.views import web_main_def, open_xlsx


file_name = './data/operations.xlsx'
transactions = open_xlsx(file_name)
month = '2020-02'
limit = 100
category = 'Супермаркеты'
df = pd.DataFrame(transactions)


print(web_main_def('2020-02-10 11:10:10'))
print(investment_bank(month, transactions, limit))
print(spending_by_category(df, category, '2020-02-10 11:10:10'))
