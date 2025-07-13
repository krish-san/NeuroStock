import pandas as pd
from datetime import datetime

def load_data(path):
    df = pd.read_csv(path)
    df["expiry_date"] = pd.to_datetime(df["expiry_date"])
    df["days_to_expiry"] = (df["expiry_date"] - datetime.today()).dt.days
    return df

def analyze_stock(df):
    discount_df = df[df["days_to_expiry"] <= 3].copy()
    restock_df = df[df["stock"] < df["min_stock_threshold"]].copy()
    return discount_df, restock_df
