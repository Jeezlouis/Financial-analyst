import plotly.express as px
import pandas as pd
import numpy as np

def calculate_pnl(df, signals, trade_size_pct=0.10, initial_balance=10000):
    if isinstance(signals, dict):
        buy_signals = signals.get('Buy', pd.DataFrame()).copy()
        sell_signals = signals.get('Sell', pd.DataFrame()).copy()

        buy_signals["Signal"] = "Buy"
        sell_signals["Signal"] = "Sell"

        signals = pd.concat([buy_signals, sell_signals]).sort_index()

    if "Signal" not in signals.columns:
        raise ValueError("❌ 'Signal' column is missing from the signals DataFrame.")

    buys = signals[signals["Signal"] == "Buy"]
    sells = signals[signals["Signal"] == "Sell"]

    trades = []

    buy_times = buys.index.tolist()
    sell_times = sells.index.tolist()

    i = j = 0
    while i < len(buy_times) and j < len(sell_times):
        buy_time = buy_times[i]
        sell_time = sell_times[j]

        if sell_time > buy_time and buy_time in df.index and sell_time in df.index:
            entry_price = df.loc[buy_time, 'Close']
            exit_price = df.loc[sell_time, 'Close']
            entry_date = df.loc[buy_time, 'Date']
            exit_date = df.loc[sell_time, 'Date']

            trade_size = trade_size_pct * initial_balance
            qty = trade_size / entry_price
            pnl = (exit_price - entry_price) * qty

            trades.append({
                'entry_time': entry_date,
                'exit_time': exit_date,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'qty': qty,
                'pnl': pnl
            })
            i += 1
            j += 1
        else:
            j += 1  # Skip unmatched sell

    trades_df = pd.DataFrame(trades)

    return trades_df



def calculate_performance(df, signals, initial_balance=10000, trade_size_pct=0.10, risk_free_rate=0.0):

    buy_signals = signals[signals["Signal"] == "Buy"]
    sell_signals = signals[signals["Signal"] == "Sell"]


    if buy_signals.empty or sell_signals.empty:
        return None


    # Prepare signals dict expected by calculate_pnl (if it expects dict)
    signals_dict = {"Buy": buy_signals, "Sell": sell_signals}

    trades_df = calculate_pnl(df, signals_dict)
    if trades_df.empty:
        return None

    balance = initial_balance
    trade_size = trade_size_pct * initial_balance

    for idx, row in trades_df.iterrows():
        qty = trade_size / row["entry_price"]
        pnl = (row["exit_price"] - row["entry_price"]) * qty
        trades_df.at[idx, "pnl"] = pnl

    total_pnl = trades_df["pnl"].sum()
    total_return = total_pnl / initial_balance

    daily_returns = trades_df["pnl"] / initial_balance

    if daily_returns.std() == 0 or len(daily_returns) < 2:
        sharpe_ratio = 0.0
    else:
        sharpe_ratio = ((daily_returns.mean() - risk_free_rate / 252) / daily_returns.std()) * (252**0.5)

    equity_curve = trades_df["pnl"].cumsum() + initial_balance
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    max_drawdown = drawdown.min() if not drawdown.empty else 0.0

    num_trades = len(trades_df)
    win_rate = (trades_df["pnl"] > 0).mean() * 100 if num_trades > 0 else 0.0

    emojis = []
    if total_return > 0.2:
        emojis.append("📈")
    if sharpe_ratio > 1.5:
        emojis.append("🏆")
    if win_rate > 60:
        emojis.append("🔥")

    return {
        "Total Return": f"{total_return * 100:.2f}%",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Max Drawdown": f"{max_drawdown * 100:.2f}%",
        "# of Trades": num_trades,
        "% Profitable": f"{win_rate:.1f}%",
        "Badges": " ".join(emojis),
        "Trades": trades_df
    }



def plot_win_rate(trades_df):
    if trades_df.empty or "pnl" not in trades_df.columns:
        return None
    wins = trades_df[trades_df["pnl"] > 0].shape[0]
    losses = trades_df[trades_df["pnl"] <= 0].shape[0]

    # Avoid plot with no data
    if wins + losses == 0:
        return None

    fig = px.pie(
        values=[wins, losses],
        names=["Wins", "Losses"],
        title="🏆 Win vs Loss Distribution"
    )
    return fig
