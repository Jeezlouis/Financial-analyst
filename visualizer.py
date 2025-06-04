import plotly.graph_objs as go
import pandas as pd

def plot_price_with_indicators(df, indicators=[], title="Price Chart with Indicators", signals=None):
    fig = go.Figure()

    # Price line
    fig.add_trace(go.Candlestick(
        x=df['Date'],
        open=df['Open'], high=df['High'], 
        low=df['Low'], close=df['Close'], 
        name='Candle stick'
        
    ))

    # Indicators (EMA, RSI, BBANDS etc.)
    # for ind in indicators:
    #     if ind in df.columns:
    #         fig.add_trace(go.Scatter(
    #             x=df.index,
    #             y=df[ind],
    #             name=ind
    #         ))

    # Optional buy/sell signals as markers
    if signals is not None:
        if 'buy' in signals and not signals['buy'].empty:
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=signals['Buy'],
                mode='markers',
                name='Buy Signal',
                marker=dict(symbol='triangle-up', size=10, color='green')
            ))
        if 'sell' in signals and not signals['sell'].empty:
            fig.add_trace(go.Scatter(
                x=df['Date'],
                y=signals['Sell'],
                mode='markers',
                name='Sell Signal',
                marker=dict(symbol='triangle-down', size=10, color='red')
            ))

    fig.update_layout(title=title, xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=False)
    return fig



def plot_volume(df):
    return go.Figure(data=[
        go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='blue')
    ]).update_layout(title='Volume', xaxis_title='Date', yaxis_title='Volume')


def plot_rsi(df):
    if 'RSI' in df.columns or 'RSI' in df.columns:
        fig = go.Figure()
        if 'RSI' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'))
        if 'RSI' in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'))
        fig.add_shape(type='line', x0=df.index[0], x1=df.index[-1], y0=70, y1=70, line=dict(dash='dash', color='red'))
        fig.add_shape(type='line', x0=df.index[0], x1=df.index[-1], y0=30, y1=30, line=dict(dash='dash', color='green'))
        fig.update_layout(title='RSI', yaxis_title='Value')
        return fig
    return None


def plot_macd(df):
    if 'MACD' in df.columns and 'MACD_S' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD'))
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_S'], name='Signal'))
        if 'MACD_H' in df.columns:
            fig.add_trace(go.Bar(x=df.index, y=df['MACD_H'], name='Histogram'))
        fig.update_layout(title='MACD', yaxis_title='MACD Value')
        return fig
    return None

def plot_ema(df):
    if 'EMA' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], name='EMA'))
        return fig
    return None
def plot_stoch(df):
    if 'Stoch_K' in df.columns and 'Stoch_D' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Stoch_K'], name='Stoch_K'))  # fixed key
        fig.add_trace(go.Scatter(x=df.index, y=df['Stoch_D'], name='Stoch_D'))
        return fig
    return None

def plot_bbands(df):
    if 'BBL' in df.columns and 'BBM' in df.columns and 'BBU' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['BBU'], name='Upper', line=dict(color='teal')))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['BBM'], name='Middle', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['BBL'], name='Lower', line=dict(color='pink')))
        return fig
    return None

def plot_atr(df):
    if 'ATRr_14' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['ATRr_14'], name='ATR'))
        return fig
    return None

def plot_obv(df):
    if 'OBV' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['OBV'], name='OBV'))
        return fig
    return None



def plot_cumulative_return(trades_df, initial_balance=10000):
    trades_df["cumulative_pnl"] = trades_df["pnl"].cumsum() + initial_balance
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trades_df["exit_time"],
        y=trades_df["cumulative_pnl"],
        mode='lines+markers',
        name="Cumulative Return",
        line=dict(color='green')
    ))
    fig.update_layout(title="📈 Cumulative Return Over Time", xaxis_title="Date", yaxis_title="Equity")
    return fig


def plot_drawdown(trades_df, initial_balance=10000):
    equity_curve = trades_df["pnl"].cumsum() + initial_balance
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trades_df["exit_time"],
        y=drawdown,
        mode='lines',
        name="Drawdown",
        line=dict(color='red')
    ))
    fig.update_layout(title="📉 Drawdown Chart", xaxis_title="Date", yaxis_title="Drawdown (%)")
    return fig

