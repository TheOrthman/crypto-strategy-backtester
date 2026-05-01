import yfinance as yf
import pandas as pd


def load_crypto_data(ticker: str = "BTC-USD", start: str = "2020-01-01", end: str = None) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        raise ValueError("No data found. Please check ticker or date range.")

    df = df.reset_index()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    return df