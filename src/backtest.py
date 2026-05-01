import pandas as pd

def run_backtest(
    df: pd.DataFrame,
    initial_capital: float = 10000,
    transaction_cost: float = 0.001,
    slippage: float = 0.001,
    stop_loss_atr: float = 2.0,
    take_profit_atr: float = 3.0,
    risk_per_trade: float = 0.01
) -> pd.DataFrame:
    df = df.copy()

    df["market_return"] = df["Close"].pct_change()
    df["trade"] = df["position"].diff().abs().fillna(0)

    total_cost = transaction_cost + slippage

    df["entry_price"] = None
    df["stop_loss"] = None
    df["take_profit"] = None
    df["exit_reason"] = None
    df["position_size"] = 0.0

    in_trade = False
    entry_price = None
    stop_loss = None
    take_profit = None
    position_size = 0

    equity = initial_capital
    equity_values = []
    strategy_returns = []

    for i in range(len(df)):
        row = df.iloc[i]

        if i == 0:
            equity_values.append(equity)
            strategy_returns.append(0)
            continue

        prev_close = df.iloc[i - 1]["Close"]
        current_close = row["Close"]

        daily_return = 0

        if row["position"] == 1 and not in_trade:
            in_trade = True
            entry_price = current_close
            stop_loss = entry_price - (stop_loss_atr * row["atr"])
            take_profit = entry_price + (take_profit_atr * row["atr"])

            risk_amount = equity * risk_per_trade
            risk_per_unit = entry_price - stop_loss

            if risk_per_unit > 0:
                position_size = risk_amount / risk_per_unit
            else:
                position_size = 0

            cost_paid = equity * total_cost
            equity -= cost_paid

            df.at[df.index[i], "exit_reason"] = "Entry"

        if in_trade:
            pnl = position_size * (current_close - prev_close)
            equity += pnl

            df.at[df.index[i], "entry_price"] = entry_price
            df.at[df.index[i], "stop_loss"] = stop_loss
            df.at[df.index[i], "take_profit"] = take_profit
            df.at[df.index[i], "position_size"] = position_size

            if row["Low"] <= stop_loss:
                pnl = position_size * (stop_loss - current_close)
                equity += pnl
                equity -= equity * total_cost
                in_trade = False
                df.at[df.index[i], "exit_reason"] = "Stop Loss"

            elif row["High"] >= take_profit:
                pnl = position_size * (take_profit - current_close)
                equity += pnl
                equity -= equity * total_cost
                in_trade = False
                df.at[df.index[i], "exit_reason"] = "Take Profit"

            elif row["position"] == 0:
                equity -= equity * total_cost
                in_trade = False
                df.at[df.index[i], "exit_reason"] = "Signal Exit"

        daily_return = (equity / equity_values[-1]) - 1 if equity_values[-1] != 0 else 0

        equity_values.append(equity)
        strategy_returns.append(daily_return)

    df["strategy_return"] = strategy_returns
    df["equity_curve"] = equity_values
    df["buy_hold_curve"] = initial_capital * (1 + df["market_return"].fillna(0)).cumprod()

    return df


def generate_trade_log(results: pd.DataFrame) -> pd.DataFrame:
    trades = results[results["exit_reason"].notna()].copy()

    trade_log = trades[
        [
            "Date",
            "Close",
            "position",
            "strategy_return",
            "equity_curve",
            "entry_price",
            "stop_loss",
            "take_profit",
            "exit_reason",
            "position_size",
        ]
    ].copy()

    trade_log = trade_log.rename(
        columns={
            "Date": "Trade Date",
            "Close": "Price",
            "position": "Position",
            "strategy_return": "Return",
            "equity_curve": "Equity",
            "entry_price": "Entry Price",
            "stop_loss": "Stop Loss",
            "take_profit": "Take Profit",
            "exit_reason": "Exit Reason",
            "position_size": "Position Size",
        }
    )

    return trade_log