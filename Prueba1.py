import pandas as pd

file_path = 'PRECIOS_LAB_SJ1.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)
prices = pd.DataFrame(columns=['NAME', 'PRICE', 'QUANTITY'])
# Search and save an item that has been purchased
def get_price_p(item, data):
    prices = data
    # Check if the item exists in the DataFrame and if there are any null values in the subset
    if df.loc[df['NAME'] == item].isnull().any().any():
        new_df = df.loc[df['NAME'] == item].copy()  # Use .copy() to avoid SettingWithCopyWarning
        new_df['QUANTITY'] = 1
        return new_df
    else:
        if not prices.loc[prices['NAME'] == item].empty:
            times = prices.loc[prices['NAME'] == item, 'QUANTITY'].iloc[0]
            prices.loc[prices['NAME'] == item, 'QUANTITY'] = times + 1
        else:
            new_df = df.loc[df['NAME'] == item].copy()
            new_df['QUANTITY'] = 1
            prices = pd.concat([prices, new_df])
        return prices
# Example usage
prices = get_price_p('IgE ANTI BANANO',prices)
prices = get_price_p('IgE ANTI BANANO',prices)
prices = get_price_p('IgE ANTI BANANO',prices)
print(prices)