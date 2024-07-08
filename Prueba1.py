import pandas as pd

# Load the Excel file
file_path = r'C:\Users\yangr\Desktop\Programa\PRECIOS_LAB_SJ1.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Convert the DataFrame to a dictionary
prices_dict = df.set_index('NAME')['PRICE'].to_dict()

def get_price(item):
    return prices_dict.get(item, "Item not found")

d = int(get_price('IgE ANTI BANANO'))
print (d * 1.04)