import pandas as pd


def add_indicators(df: pd.DataFrame, short_window: int = 20, long_window: int = 50, atr_window: int = 14) -> pd.DataFrame:
    df = df.copy()

    df["return"] = df["Close"].pct_change()

    df["short_ma"] = df["Close"].rolling(short_window).mean()
    df["long_ma"] = df["Close"].rolling(long_window).mean()

    df["high_low"] = df["High"] - df["Low"]
    df["high_close"] = (df["High"] - df["Close"].shift()).abs()
    df["low_close"] = (df["Low"] - df["Close"].shift()).abs()

    df["true_range"] = df[["high_low", "high_close", "low_close"]].max(axis=1)
    df["atr"] = df["true_range"].rolling(atr_window).mean()

    df = df.dropna()

    return df