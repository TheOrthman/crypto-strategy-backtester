# ₿ Crypto Strategy Backtester

A professional crypto trading strategy backtesting platform built with Python and Streamlit.

This app allows users to test rule-based trading strategies on historical crypto data under realistic market conditions, including transaction costs, slippage, and risk management.

---

## 🚀 Live Demo
(Coming soon — deployed on Streamlit Cloud)

---

## 🎯 Features

- Backtesting on real crypto data (BTC, ETH, SOL, etc.)
- Moving Average Crossover strategy
- ATR-based Stop Loss & Take Profit
- Risk-based Position Sizing
- Transaction Costs & Slippage modeling
- Trade Log with detailed entries/exits
- Performance Metrics:
  - Total Return
  - Sharpe Ratio
  - Max Drawdown
  - Win Rate
  - Profit Factor
  - Expectancy
- Market Regime Detection:
  - Bullish / Bearish / Sideways
  - High vs Low Volatility
- Multi-Asset Strategy Testing
- Parameter Optimization (MA tuning)
- Interactive Streamlit Dashboard

---

## 🧠 Problem It Solves

Most trading strategies appear profitable but fail in real markets due to:
- lack of proper backtesting
- ignoring costs (fees, slippage)
- overfitting
- poor risk management

This system solves that by providing a realistic simulation environment where strategies are evaluated based on **risk-adjusted performance**, not just returns.

---

## ⚙️ Tech Stack

- Python
- pandas, numpy
- scikit-learn
- matplotlib
- yfinance
- Streamlit

---

## 📂 Project Structure
crypto-strategy-backtester/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│ ├── init.py
│ ├── data.py
│ ├── indicators.py
│ ├── regime.py
│ ├── strategies.py
│ ├── backtest.py
│ ├── metrics.py
│ ├── portfolio.py
│ └── optimizer.py
│
└── images/


---

## ▶️ How to Run Locally

```bash
git clone https://github.com/TheOrthman/crypto-strategy-backtester
cd crypto-strategy-backtester

pip install -r requirements.txt

streamlit run app.py
📊 How It Works
Load historical crypto data
Generate indicators (MA, ATR, returns)
Apply strategy rules
Simulate trades with:
costs
slippage
risk sizing
Evaluate performance using professional metrics
Analyze results across different market regimes
💡 Key Insight

The system focuses on risk-adjusted performance, meaning:

A strategy is only considered good if it delivers consistent returns with controlled risk.

📌 Example Use Cases
Testing new trading strategies before live deployment
Evaluating performance across different crypto assets
Optimizing trading parameters
Understanding how strategies behave in different market conditions
⚠️ Disclaimer

This project is for educational and research purposes only.
It does not constitute financial advice.

👤 Author

Built as part of a data science and financial analytics portfolio.


---



```text
THEORTHMAN