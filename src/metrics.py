import numpy as np
import pandas as pd


def calculate_metrics(results: pd.DataFrame) -> dict:
    returns = results["strategy_return"].dropna()
    equity = results["equity_curve"].dropna()

    total_return = equity.iloc[-1] / equity.iloc[0] - 1
    volatility = returns.std() * np.sqrt(252)

    sharpe = 0
    if returns.std() != 0:
        sharpe = returns.mean() / returns.std() * np.sqrt(252)

    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_drawdown = drawdown.min()

    wins = returns[returns > 0]
    losses = returns[returns < 0]

    win_rate = len(wins) / len(returns) if len(returns) > 0 else 0
    avg_win = wins.mean() if len(wins) > 0 else 0
    avg_loss = losses.mean() if len(losses) > 0 else 0

    profit_factor = 0
    if losses.sum() != 0:
        profit_factor = abs(wins.sum() / losses.sum())

    expectancy = (win_rate * avg_win) + ((1 - win_rate) * avg_loss)

    return {
        "Total Return": total_return,
        "Volatility": volatility,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_drawdown,
        "Win Rate": win_rate,
        "Average Win": avg_win,
        "Average Loss": avg_loss,
        "Profit Factor": profit_factor,
        "Expectancy": expectancy,
    }