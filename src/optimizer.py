import pandas as pd

from src.data import load_crypto_data
from src.indicators import add_indicators
from src.regime import add_market_regime
from src.strategies import ma_crossover_strategy
from src.backtest import run_backtest
from src.metrics import calculate_metrics


def optimize_ma(
    ticker="BTC-USD",
    start="2021-01-01",
    short_range=[10, 20, 30],
    long_range=[50, 100, 200]
):
    results = []

    for s in short_range:
        for l in long_range:
            if s >= l:
                continue

            df = load_crypto_data(ticker, start=start)
            df = add_indicators(df, short_window=s, long_window=l)
            df = add_market_regime(df)
            df = ma_crossover_strategy(df)

            bt = run_backtest(df)
            metrics = calculate_metrics(bt)

            results.append({
                "short_ma": s,
                "long_ma": l,
                "Sharpe": metrics["Sharpe Ratio"],
                "Return": metrics["Total Return"],
                "MaxDD": metrics["Max Drawdown"]
            })

    return pd.DataFrame(results).sort_values(by="Sharpe", ascending=False)