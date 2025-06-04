import pandas as pd
import pandas_ta as ta

# Trend
def compute_ema(df, length=14):
    ema_df = ta.ema(df['Close'], length=length)
    ema_df.columns = ['EMA_14']
    return ema_df
# Momentum
def compute_macd(df, fast=12, slow=26, signal=9):
    macd_df = ta.macd(df['Close'], fast=fast, slow=slow, signal=signal)
    macd_df.columns = ['MACD', 'MACD_S', 'MACD_H']
    return macd_df

def compute_rsi(df, length=9):
    return ta.rsi(df['Close'], length=length)

def compute_stoch(df, k=14, d=3, smooth_k=3):
    stoch_df = ta.stoch(df['High'], df['Low'], df['Close'], k=k, d=d, smooth_k=smooth_k)
    stoch_df.columns = ['Stoch_K', 'Stoch_D']  # fixed names to match plot
    return stoch_df

# Volatility
def compute_bbands(df, length=20, std=2):
    bbands_df = ta.bbands(df['Close'], length=length, std=std)
    bbands_df.columns = ["BBL", "BBM", "BBU", "BBB", "BBP"]
    return bbands_df

def compute_atr(df, length=14):
    return ta.atr(df['High'], df['Low'], df['Close'], length=length)

# Volume
def compute_obv(df):
    return ta.obv(df['Close'], df['Volume'])

# quantitative


