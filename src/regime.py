import pandas as pd


def add_market_regime(
    df: pd.DataFrame,
    trend_window: int = 50,
    volatility_window: int = 20
) -> pd.DataFrame:
    df = df.copy()

    df["trend_ma"] = df["Close"].rolling(trend_window).mean()
    df["volatility"] = df["return"].rolling(volatility_window).std()

    vol_median = df["volatility"].median()

    df["trend_regime"] = "Sideways"
    df.loc[df["Close"] > df["trend_ma"], "trend_regime"] = "Bullish"
    df.loc[df["Close"] < df["trend_ma"], "trend_regime"] = "Bearish"

    df["volatility_regime"] = "Low Volatility"
    df.loc[df["volatility"] > vol_median, "volatility_regime"] = "High Volatility"

    df = df.dropna()

    return df