import pandas as pd

import pandas as pd

def generate_signals(df, strategy_name):
    """
    Generate buy/sell signals based on selected strategy.
    Returns a DataFrame with a new 'Signal' column: 'Buy', 'Sell', or 'Hold'.
    """
    signals = pd.DataFrame(index=df.index)
    signals['Signal'] = 0  # Default to no signal

    # Pairs
    if strategy_name == "EMA + RSI":
        if "EMA" in df.columns and "RSI" in df.columns:
            signals.loc[(df["EMA"] > df["Close"]) & (df["RSI"] < 30), 'Signal'] = 1
            signals.loc[(df["EMA"] < df["Close"]) & (df["RSI"] > 70), 'Signal'] = -1

    elif strategy_name == "MACD + RSI":
        if "MACD" in df.columns and "RSI" in df.columns:
            signals.loc[(df["MACD"] > df['MACD_S']) & (df["RSI"] < 30), 'Signal'] = 1
            signals.loc[(df["MACD"] < df['MACD_S']) & (df["RSI"] > 70), 'Signal'] = -1

    elif strategy_name == "EMA Crossover":
        if "EMA" in df.columns and "EMA_50" in df.columns:
            signals.loc[df["EMA"] > df["EMA_50"], 'Signal'] = 1
            signals.loc[df["EMA"] < df["EMA_50"], 'Signal'] = -1

    elif strategy_name == "MACD + BBands":
        if {"MACD", "BB_upper", "BB_lower"}.issubset(df.columns):
            signals.loc[(df["MACD"] > 0) & (df["Close"] < df["BB_lower"]), 'Signal'] = 1
            signals.loc[(df["MACD"] < 0) & (df["Close"] > df["BB_upper"]), 'Signal'] = -1

    elif strategy_name == "Stoch + ATR":
        if {"Stoch_K", "ATR"}.issubset(df.columns):
            atr_mean = df["ATR"].rolling(5).mean()
            signals.loc[(df["Stoch_K"] < 20) & (df["ATR"] > atr_mean), 'Signal'] = 1
            signals.loc[(df["Stoch_K"] > 80) & (df["ATR"] > atr_mean), 'Signal'] = -1

    elif strategy_name == "OBV + RSI":
        if {"OBV", "RSI"}.issubset(df.columns):
            obv_mean = df["OBV"].rolling(10).mean()
            signals.loc[(df["OBV"] > obv_mean) & (df["RSI"] < 30), 'Signal'] = 1
            signals.loc[(df["OBV"] < obv_mean) & (df["RSI"] > 70), 'Signal'] = -1

    elif strategy_name == "EMA + MACD":
        if {"EMA", "MACD"}.issubset(df.columns):
            signals.loc[(df["EMA"] > df["Close"]) & (df["MACD"] > 0), 'Signal'] = 1
            signals.loc[(df["EMA"] < df["Close"]) & (df["MACD"] < 0), 'Signal'] = -1

    # Individual indicators
    elif strategy_name == "EMA":
        if "EMA" in df.columns:
            signals.loc[df["Close"] > df["EMA"], 'Signal'] = 1
            signals.loc[df["Close"] < df["EMA"], 'Signal'] = -1

    elif strategy_name == "RSI":
        if "RSI" in df.columns:
            signals.loc[df["RSI"] < 30, 'Signal'] = 1
            signals.loc[df["RSI"] > 70, 'Signal'] = -1

    elif strategy_name == "MACD":
        if "MACD" in df.columns and "MACD_S" in df.columns:
            signals.loc[df["MACD"] > df["MACD_S"], 'Signal'] = 1
            signals.loc[df["MACD"] < df["MACD_S"], 'Signal'] = -1

    elif strategy_name == "Stochastic":
        if "Stoch_K" in df.columns:
            signals.loc[df["Stoch_K"] < 20, 'Signal'] = 1
            signals.loc[df["Stoch_K"] > 80, 'Signal'] = -1

    elif strategy_name == "ATR":
        if "ATR" in df.columns:
            atr_mean = df["ATR"].rolling(5).mean()
            signals.loc[df["ATR"] > atr_mean, 'Signal'] = 1
            signals.loc[df["ATR"] < atr_mean, 'Signal'] = -1

    elif strategy_name == "OBV":
        if "OBV" in df.columns:
            obv_mean = df["OBV"].rolling(10).mean()
            signals.loc[df["OBV"] > obv_mean, 'Signal'] = 1
            signals.loc[df["OBV"] < obv_mean, 'Signal'] = -1

    else:
        print(f"⚠️ Warning: Strategy '{strategy_name}' not recognized or missing indicators.")

    signals["Signal"] = signals["Signal"].map({1: "Buy", -1: "Sell"}).fillna("Hold")

    return signals


# was used to generate dummy signals during an earlier bug

# def generate_dummy_signals(df):
#     df['Signal'] = 0
#     df.loc[df.index[::20], 'Signal'] = 1   # Buy every 20th
#     df.loc[df.index[10::20], 'Signal'] = -1  # Sell 10 after each buy

#     signals = {
#         'buy': df.loc[df['Signal'] == 1, 'Close'],
#         'sell': df.loc[df['Signal'] == -1, 'Close']
#     }
#     return df, signals
