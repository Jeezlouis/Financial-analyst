import streamlit as st
import pandas as pd
from strategies import apply_selected_indicators
from utils import load_stock_data  # assume you have a function to load data
from visualizer import plot_price_with_indicators, plot_volume, plot_rsi, plot_macd, plot_atr, plot_bbands, plot_ema, plot_obv, plot_stoch, plot_cumulative_return, plot_drawdown
from signals import generate_signals
from performance import calculate_performance, plot_win_rate, calculate_pnl
import io

st.title("📈 Hybrid Financial Analyst")

# Load user CSV or example
uploaded = st.file_uploader("Upload OHLCV CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = load_stock_data("BTC-USD")  # fallback or sample

if "df_with_indicators" not in st.session_state:
    st.session_state.df_with_indicators = df.copy()


st.subheader("Choose Indicators")
available_indicators = ["EMA", "MACD", "RSI", "Stochastic", "Bollinger Bands", "ATR", "OBV"]
selected_indicators = st.multiselect("Select indicators to apply", available_indicators)

# Parameter controls
params = {}
if "EMA" in selected_indicators:
    length = st.slider("EMA Length", 5, 50, 14)
    params["EMA"] = {"length": length}
if "MACD" in selected_indicators:
    fast = st.slider("MACD Fast", 5, 20, 12)
    slow = st.slider("MACD Slow", 20, 40, 26)
    signal = st.slider("MACD Signal", 5, 15, 9)
    params["MACD"] = {"fast": fast, "slow": slow, "signal": signal}
if "RSI" in selected_indicators:
    length = st.slider("RSI Length", 5, 30, 14)
    params["RSI"] = {"length": length}
if "Stochastic" in selected_indicators:
    k = st.slider("Stochastic %K", 5, 21, 14)
    d = st.slider("Stochastic %D", 3, 10, 3)
    smooth_k = st.slider("Stochastic smooth K", 1, 5, 3)
    params["Stochastic"] = {"k": k, "d": d, "smooth_k": smooth_k}
if "Bollinger Bands" in selected_indicators:
    length = st.slider("BB Length", 10, 30, 20)
    std = st.slider("BB Std Dev", 1, 3, 2)
    params["Bollinger Bands"] = {"length": length, "std": std}
if "ATR" in selected_indicators:
    length = st.slider("ATR Length", 5, 30, 14)
    params["ATR"] = {"length": length}
if "OBV" in selected_indicators:
    params["OBV"] = {}  # No params for OBV

if st.button("Apply Indicators"):
    df_with_indicators = apply_selected_indicators(df.copy(), selected_indicators, params)
    st.session_state.df_with_indicators = df_with_indicators
    st.success("Indicators applied successfully!")
    st.dataframe(df_with_indicators)


    # numeric_cols = df.select_dtypes(include=['number']).columns
    # plot_cols = ['Close'] + [col for col in numeric_cols if col not in ['Open', 'High', 'Low', 'Close', 'Volume']]
    # if plot_cols:
    #     st.line_chart(df[plot_cols])
    # else:
    #     st.warning("No valid numeric columns to plot.")



st.subheader("📊 Visualizations")

df = st.session_state.get("df_with_indicators", None)

if df is not None and not df.empty:
    strategy_for_signals = st.selectbox("Select Strategy for Signal Generation", [
        "None", "EMA + RSI", "MACD + RSI", "EMA Crossover", "MACD + BBands",
        "Stoch + ATR", "OBV + RSI", "EMA + MACD", "EMA", "RSI", "Stoch",
        "BBands", "ATR", "MACD", "OBV"
    ])

    signals = None
    signals_dict = {'buy': pd.Series(dtype=float), 'sell': pd.Series(dtype=float)}  # empty default
    

    if strategy_for_signals != "None":
        signals = generate_signals(df, strategy_name=strategy_for_signals)
        # df, signals = generate_dummy_signals(df)
        # st.write("Generated signals:", signals)

        # # Extract buy and sell signals indices
        # buy_indices = signals.index[signals['Signal'] == 1]
        # sell_indices = signals.index[signals['Signal'] == -1]

        # buy_signals = df.loc[buy_indices, 'Close'] if not buy_indices.empty else pd.Series(dtype=float)
        # sell_signals = df.loc[sell_indices, 'Close'] if not sell_indices.empty else pd.Series(dtype=float)

        buy_signals = signals[signals['Signal'] == 'Buy']
        sell_signals = signals[signals['Signal'] == 'Sell']


        signals_dict = {'Buy': buy_signals, 'Sell': sell_signals}
        # st.write("signals_dict:", signals_dict)
        

        # Calculate PnL only if both buy and sell signals exist
        if not buy_signals.empty and not sell_signals.empty:
            trades_df = calculate_pnl(df, signals_dict)
            # st.write(trades_df.tail(10))
        else:
            st.info("No buy/sell signals generated with the selected strategy.")

    # Plot chart — check signals DataFrame safely before passing
    if signals is not None and not signals.empty:
        fig = plot_price_with_indicators(df, indicators=selected_indicators, signals=signals)
    else:
        fig = plot_price_with_indicators(df, indicators=selected_indicators, signals=None)

    st.plotly_chart(fig, use_container_width=True)

    # Other charts (Volume, RSI, MACD, etc.) — check if each returns a figure before plotting
    with st.expander("📈 Volume"):
        st.plotly_chart(plot_volume(df), use_container_width=True)

    with st.expander("📉 RSI"):
        rsi_chart = plot_rsi(df)
        if rsi_chart is not None:
            st.plotly_chart(rsi_chart, use_container_width=True)

    with st.expander("📉 MACD"):
        macd_chart = plot_macd(df)
        if macd_chart is not None:
            st.plotly_chart(macd_chart, use_container_width=True)

    with st.expander("📉 EMA"):
        ema_chart = plot_ema(df)
        if ema_chart is not None:
            st.plotly_chart(ema_chart, use_container_width=True)

    with st.expander("📉 BBANDS"):
        bbands_chart = plot_bbands(df)
        if bbands_chart is not None:
            st.plotly_chart(bbands_chart, use_container_width=True)

    with st.expander("📉 STOCH"):
        stoch_chart = plot_stoch(df)
        if stoch_chart is not None:
            st.plotly_chart(stoch_chart, use_container_width=True)

    with st.expander("📉 ATR"):
        atr_chart = plot_atr(df)
        if atr_chart is not None:
            st.plotly_chart(atr_chart, use_container_width=True)

    with st.expander("📉 OBV"):
        obv_chart = plot_obv(df)
        if obv_chart is not None:
            st.plotly_chart(obv_chart, use_container_width=True)

    # Performance metrics & charts
    if signals is not None and strategy_for_signals != "None":
        metrics = calculate_performance(df, signals)

        if metrics:
            st.subheader("📊 Strategy Performance Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Return", metrics["Total Return"])
            col2.metric("Sharpe Ratio", metrics["Sharpe Ratio"])
            col3.metric("Max Drawdown", metrics["Max Drawdown"])

            col4, col5 = st.columns(2)
            col4.metric("# of Trades", metrics["# of Trades"])
            col5.metric("% Profitable", metrics["% Profitable"])

            st.markdown(f"**🏅 Badges:** {metrics['Badges']}")
        else:
            st.info("⚠️ Not enough signals to calculate performance.")

        st.subheader("📊 Strategy Charts")
        # trades_df = pd.DataFrame(signals["trade_log"]) if signals is not None and "trade_log" in signals else pd.DataFrame()

        col1, col2 = st.columns(2)

        if trades_df.empty:
            st.warning("⚠️ trades_df is empty! No trades executed.")
        elif "pnl" not in trades_df.columns:
            st.error("❌ 'pnl' column still missing before plotting!")

        with col1:
            st.plotly_chart(plot_cumulative_return(trades_df), use_container_width=True)
        with col2:
            st.plotly_chart(plot_drawdown(trades_df), use_container_width=True)

        st.plotly_chart(plot_win_rate(trades_df), use_container_width=True)

        st.subheader("📥 Export Results")

        # Trade Logs CSV
        csv = trades_df.to_csv(index=False)
        st.download_button(
            label="Download Trade Log CSV",
            data=csv,
            file_name="trade_log.csv",
            mime="text/csv"
        )

        # Result PNG: save plot to image
        import io
        img_buffer = io.BytesIO()
        plot_cumulative_return(trades_df).write_image(img_buffer, format='png')
        st.download_button("Download Equity Chart (PNG)", data=img_buffer, file_name="equity_chart.png", mime="image/png")

else:
    st.warning("No indicators have been applied yet. Please apply indicators before generating visualizations.")

st.markdown("---")
st.markdown("""
**📌 Disclaimer:** This is a demo financial analysis tool. The data and strategies used are for educational purposes only and do not constitute financial advice.

🔗 Created by Jeezlouis(https://github.com/Jeezlouis)  
🧠 Powered by `pandas_ta`, `plotly`, and `Streamlit`
""")


