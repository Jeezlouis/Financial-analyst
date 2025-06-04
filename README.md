# 📈 Crypto Trading Strategy Simulator

This project is a Python-based **backtesting simulator** that evaluates different trading strategies on historical cryptocurrency data using technical indicators such as **EMA**, **RSI**, and **MACD**.

---

## 🚀 Features

- ✅ Strategy-based signal generation (Buy, Sell, Hold)
- ✅ Supports combination and individual indicators:
  - EMA + RSI
  - MACD + RSI
  - EMA crossover
  - RSI-only
  - MACD-only
  - EMA-only
- ✅ Trade simulation:
  - Entry/exit timing and price tracking
  - Trade size based on percentage of account balance
  - Realistic PnL (Profit and Loss) calculation
- ✅ Organized trade logs
- ✅ Performance metrics generation
- ✅ Optional Plotly visualization support

---

## 📂 Project Structure

├── data/ # Folder for input CSV data (OHLCV format)
├── indicators.py # Functions to compute EMA, RSI, MACD
├── strategy.py # Strategy-based signal generator
├── main.py # Entry script to run a simulation
├── utils/ # (Optional) utility scripts: formatting, plotting
├── README.md # Project documentation


---

## 🧠 Strategies Implemented

| Strategy         | Buy Signal Conditions                              | Sell Signal Conditions                              |
|------------------|----------------------------------------------------|-----------------------------------------------------|
| EMA + RSI        | EMA > Close and RSI < 30                           | EMA < Close and RSI > 70                            |
| MACD + RSI       | MACD > MACD Signal and RSI < 30                    | MACD < MACD Signal and RSI > 70                     |
| EMA Crossover    | EMA > EMA_50                                       | EMA < EMA_50                                        |
| RSI Only         | RSI < 30                                           | RSI > 70                                            |
| MACD Only        | MACD > MACD Signal                                 | MACD < MACD Signal                                  |
| EMA Only         | EMA > Close                                        | EMA < Close                                         |

---

## 📊 Input Format

The project expects a CSV file with the following columns:

Date, Open, High, Low, Close, Volume



The `Date` column should be in datetime format. The CSV should be placed in the `data/` directory or loaded via pandas.

---

## ⚙️ How It Works

1. **Load Data**: Historical crypto price data is loaded using pandas.
2. **Calculate Indicators**: Indicators such as EMA, RSI, and MACD are computed and added to the DataFrame.
3. **Generate Signals**: Based on the chosen strategy, buy/sell signals are generated.
4. **Simulate Trades**: Each buy is matched to the next valid sell; PnL is calculated.
5. **Evaluate Performance**: Trade stats, final balance, and win/loss ratio are shown.

---

## 🛠️ Requirements

Install the required packages using uv:

```bash
uv add .
▶️ Usage
Run the simulator via the main.py script:


python main.py
Inside main.py, you can select which strategy to test:

strategy_name = "EMA + RSI"  # or any other strategy listed above
Make sure your dataset is properly loaded and cleaned in main.py.

📈 Example Output

Total Trades: 10
Winning Trades: 6
Losing Trades: 4
Final Balance: $10,825.43
Win Rate: 60%
Total PnL: +$825.43
A DataFrame of trades and optionally a plot of entries/exits can also be displayed using Plotly.

📌 TODO (optional ideas)
Add stop-loss and take-profit simulation

Add multiple asset support

Integrate live trading via Binance API

Export trade logs to CSV

Add Sharpe ratio, max drawdown calculations

📬 Contact
For suggestions, improvements, or questions, feel free to open an issue or fork the project. Happy backtesting! 🚀



---

Let me know if you want a version with example screenshots or code snippets included as well!
