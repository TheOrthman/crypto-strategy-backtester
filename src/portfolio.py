import pandas as pd

from src.data import load_crypto_data
from src.indicators import add_indicators
from src.regime import add_market_regime
from src.strategies import ma_crossover_strategy
from src.backtest import run_backtest
from src.metrics import calculate_metrics


def run_multi_asset(
    tickers,
    start="2021-01-01",
    short_window=20,
    long_window=50,
    stop_loss_atr=2,
    take_profit_atr=3,
    risk_per_trade=0.01
):
    results_list = []

    for t in tickers:
        df = load_crypto_data(t, start=start)
        df = add_indicators(df, short_window=short_window, long_window=long_window)
        df = add_market_regime(df)
        df = ma_crossover_strategy(df)

        bt = run_backtest(
            df,
            stop_loss_atr=stop_loss_atr,
            take_profit_atr=take_profit_atr,
            risk_per_trade=risk_per_trade
        )

        metrics = calculate_metrics(bt)
        metrics["Asset"] = t

        results_list.append(metrics)

    return pd.DataFrame(results_list)