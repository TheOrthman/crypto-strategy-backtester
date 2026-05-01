import pandas as pd


def ma_crossover_strategy(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["signal"] = 0
    df.loc[df["short_ma"] > df["long_ma"], "signal"] = 1

    df["position"] = df["signal"].shift(1).fillna(0)

    return df