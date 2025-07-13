import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def analyze_stock(df):
    discount_items = []
    restock_items = []

    for _, row in df.iterrows():
        if row['expiry_days'] <= 2 and row['stock_left'] > row['daily_sales'] * 2:
            discount_items.append(row)
        elif row['stock_left'] < row['daily_sales'] * 1.5:
            restock_items.append(row)

    return pd.DataFrame(discount_items), pd.DataFrame(restock_items)
