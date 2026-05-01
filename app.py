import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data import load_crypto_data
from src.indicators import add_indicators
from src.regime import add_market_regime
from src.strategies import ma_crossover_strategy
from src.backtest import run_backtest, generate_trade_log
from src.metrics import calculate_metrics
from src.portfolio import run_multi_asset
from src.optimizer import optimize_ma


st.set_page_config(
    page_title="Crypto Strategy Backtester",
    layout="wide"
)

st.title("₿ Crypto Strategy Backtester")
st.caption("A risk-aware crypto backtesting platform with ATR exits, position sizing, slippage, regime analysis, optimization, and downloadable trade logs.")

st.markdown("""
### What this app does
- Tests a Moving Average Crossover strategy on crypto assets
- Includes transaction cost and slippage
- Uses ATR-based stop-loss and take-profit exits
- Applies risk-based position sizing
- Calculates professional performance metrics
- Shows trade logs and regime performance
""")

# Sidebar controls
st.sidebar.header("Backtest Settings")

ticker = st.sidebar.selectbox(
    "Select Asset",
    ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "ADA-USD"],
    index=0
)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))

initial_capital = st.sidebar.number_input(
    "Initial Capital",
    min_value=1000,
    value=10000,
    step=1000
)

short_window = st.sidebar.slider("Short MA Window", 5, 50, 20)
long_window = st.sidebar.slider("Long MA Window", 20, 250, 50)

transaction_cost = st.sidebar.slider(
    "Transaction Cost",
    min_value=0.0,
    max_value=0.01,
    value=0.001,
    step=0.0005
)

slippage = st.sidebar.slider(
    "Slippage",
    min_value=0.0,
    max_value=0.01,
    value=0.001,
    step=0.0005
)

stop_loss_atr = st.sidebar.slider("Stop Loss ATR Multiplier", 0.5, 5.0, 2.0, 0.5)
take_profit_atr = st.sidebar.slider("Take Profit ATR Multiplier", 0.5, 8.0, 3.0, 0.5)

risk_per_trade = st.sidebar.slider(
    "Risk Per Trade",
    min_value=0.001,
    max_value=0.05,
    value=0.01,
    step=0.001
)

run_button = st.sidebar.button("Run Backtest")


def format_metrics(metrics: dict) -> pd.DataFrame:
    return pd.DataFrame({
        "Metric": list(metrics.keys()),
        "Value": list(metrics.values())
    })


if run_button:
    try:
        if short_window >= long_window:
            st.error("Short MA must be smaller than Long MA.")
        else:
            df = load_crypto_data(ticker, start=str(start_date))
            df = add_indicators(df, short_window=short_window, long_window=long_window)
            df = add_market_regime(df)
            df = ma_crossover_strategy(df)

            results = run_backtest(
                df,
                initial_capital=initial_capital,
                transaction_cost=transaction_cost,
                slippage=slippage,
                stop_loss_atr=stop_loss_atr,
                take_profit_atr=take_profit_atr,
                risk_per_trade=risk_per_trade
            )

            metrics = calculate_metrics(results)
            trade_log = generate_trade_log(results)

            st.subheader(f"Backtest Results: {ticker}")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Return", f"{metrics['Total Return']:.2%}")
            col2.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
            col3.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")
            col4.metric("Win Rate", f"{metrics['Win Rate']:.2%}")

            st.subheader("Performance Metrics")

            metrics_df = pd.DataFrame([metrics])
            st.dataframe(metrics_df.style.format({
                "Total Return": "{:.2%}",
                "Volatility": "{:.2%}",
                "Sharpe Ratio": "{:.2f}",
                "Max Drawdown": "{:.2%}",
                "Win Rate": "{:.2%}",
                "Average Win": "{:.2%}",
                "Average Loss": "{:.2%}",
                "Profit Factor": "{:.2f}",
                "Expectancy": "{:.4f}"
            }))

            # ✅ CLEAN EQUITY CURVE (NO DESIGN ISSUES)
            st.subheader("Equity Curve")

            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(results["Date"], results["equity_curve"], label="Strategy Equity")
            ax.plot(results["Date"], results["buy_hold_curve"], label="Buy & Hold")

            ax.set_title("Strategy vs Buy & Hold")
            ax.set_xlabel("Date")
            ax.set_ylabel("Equity")

            ax.legend()
            ax.grid(True)

            st.pyplot(fig)

            # ✅ TRADE LOG
            st.subheader("Trade Log")
            st.dataframe(trade_log)

            trade_csv = trade_log.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Trade Log",
                data=trade_csv,
                file_name=f"{ticker}_trade_log.csv",
                mime="text/csv"
            )

            # ✅ REGIME ANALYSIS
            st.subheader("Market Regime Analysis")

            regime_summary = results.groupby("trend_regime")["strategy_return"].agg(
                total_return=lambda x: (1 + x).prod() - 1,
                avg_return="mean",
                volatility="std",
                count="count"
            ).reset_index()

            st.dataframe(regime_summary)

            vol_regime_summary = results.groupby("volatility_regime")["strategy_return"].agg(
                total_return=lambda x: (1 + x).prod() - 1,
                avg_return="mean",
                volatility="std",
                count="count"
            ).reset_index()

            st.subheader("Volatility Regime Analysis")
            st.dataframe(vol_regime_summary)

    except Exception as e:
        st.error("Something went wrong while running the backtest.")
        st.write(e)

st.divider()

st.subheader("Multi-Asset Test")
st.write("Test the same strategy across multiple crypto assets.")

if st.button("Run Multi-Asset Test"):
    try:
        portfolio_results = run_multi_asset(
            ["BTC-USD", "ETH-USD", "SOL-USD"],
            start=str(start_date),
            short_window=short_window,
            long_window=long_window,
            stop_loss_atr=stop_loss_atr,
            take_profit_atr=take_profit_atr,
            risk_per_trade=risk_per_trade
        )

        st.dataframe(portfolio_results.style.format({
            "Total Return": "{:.2%}",
            "Volatility": "{:.2%}",
            "Sharpe Ratio": "{:.2f}",
            "Max Drawdown": "{:.2%}",
            "Win Rate": "{:.2%}",
            "Average Win": "{:.2%}",
            "Average Loss": "{:.2%}",
            "Profit Factor": "{:.2f}",
            "Expectancy": "{:.4f}"
        }))

    except Exception as e:
        st.error("Multi-asset test failed.")
        st.write(e)
st.divider()

st.subheader("Parameter Optimization")

st.write("Find the best MA window combination based on Sharpe Ratio.")

if st.button("Run MA Optimization"):
    try:
        opt_results = optimize_ma(
            ticker=ticker,
            start=str(start_date),
            short_range=[10, 20, 30],
            long_range=[50, 100, 200]
        )

        st.dataframe(opt_results)

    except Exception as e:
        st.error("Optimization failed.")
        st.write(e)


st.markdown("""
---
### Disclaimer
This app is for educational and research purposes only.  
It is not financial advice or a live trading system.
""")