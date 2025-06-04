import yfinance as yf
import pandas as pd

def load_stock_data(ticker="AAPL", start="2022-01-01", end=None):
    """
    Load OHLCV data from Yahoo Finance.
    
    Parameters:
    - ticker (str): Stock or crypto ticker symbol (e.g., "AAPL", "BTC-USD")
    - start (str): Start date in "YYYY-MM-DD" format
    - end (str): End date in "YYYY-MM-DD" format (defaults to today)
    
    Returns:
    - DataFrame with columns: ['Open', 'High', 'Low', 'Close', 'Volume']
    """
    try:
        df = yf.download(ticker, start=start, end=end, progress=False)
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.dropna(inplace=True)
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        print(f"Error loading data for {ticker}: {e}")
        return pd.DataFrame()
