import pandas as pd
import time as t


file_path = 'PRECIOS_LAB_SJ1.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)
prices =  pd.DataFrame()
    
def get_price_p(item):
    if df.loc[df['NAME'] == item].isnull:
        new_df = df.loc[(df['NAME'] == item)]
        new_df['QUANTITY'] = 1
        return new_df
    else:
        print(prices)

prices = get_price_p('IgE ANTI BANANO')
print(prices)