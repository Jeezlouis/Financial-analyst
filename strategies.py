from indicators import (
    compute_ema, compute_macd, compute_rsi,
    compute_stoch, compute_bbands, compute_atr, compute_obv
)
import pandas as pd

INDICATOR_FUNCTIONS = {
    "EMA": compute_ema,
    "MACD": compute_macd,
    "RSI": compute_rsi,
    "Stochastic": compute_stoch,
    "Bollinger Bands": compute_bbands,
    "ATR": compute_atr,
    "OBV": compute_obv,
    "EMA + RSI": ("ema", "rsi"),
    "MACD + BBands": ("macd", "bbands"),
    "Stoch + ATR": ("stoch", "atr"),
    "OBV + RSI": ("obv", "rsi"),
    "EMA + MACD": ("ema", "macd")
}

def apply_selected_indicators(df, selected_indicators, params):
    for indicator in selected_indicators:
        func = INDICATOR_FUNCTIONS[indicator]
        args = params.get(indicator, {})
        result = func(df, **args)

        if isinstance(result, pd.Series):
            df[indicator] = result
        elif isinstance(result, pd.DataFrame):
            for col in result.columns:
                df[col] = result[col]
    return df
