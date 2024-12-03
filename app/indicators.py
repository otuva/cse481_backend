import pandas as pd
import pandas_ta as ta


def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Apply technical indicators to the market data."""
    data["SMA"] = ta.sma(data["close"], length=20)
    data["EMA"] = ta.ema(data["close"], length=20)
    data["RSI"] = ta.rsi(data["close"], length=14)

    bbands = ta.bbands(data["close"], length=20)
    data["BB_upper"], data["BB_middle"], data["BB_lower"] = bbands["BBU_20_2.0"], bbands["BBM_20_2.0"], bbands["BBL_20_2.0"]

    macd = ta.macd(data["close"], fast=12, slow=26, signal=9)
    data['MACD'], data['MACD_Signal'], data['MACD_Hist'] = macd

    supertrend = ta.supertrend(data["high"], data["low"], data["close"])
    data["SuperTrend"] = supertrend["SUPERT_7_3.0"]

    return data

def generate_signals(data: pd.DataFrame) -> pd.DataFrame:
    """
    Generate buy/sell signals based on calculated indicators.

    Args:
        data (pd.DataFrame): Market data with indicators.

    Returns:
        pd.DataFrame: DataFrame with a new column 'Signal' (1 = Buy, -1 = Sell, 0 = Hold).
    """
    data["Signal"] = 0  # Default to Hold

    # Buy signal:
    # - When RSI is below 30 (oversold)
    # - AND price crosses above the lower Bollinger Band
    buy_condition = (data["RSI"] < 30) & (data["close"] > data["BB_lower"])
    data.loc[buy_condition, "Signal"] = 1

    # Sell signal:
    # - When RSI is above 70 (overbought)
    # - OR price crosses below the upper Bollinger Band
    sell_condition = (data["RSI"] > 70) | (data["close"] < data["BB_upper"])
    data.loc[sell_condition, "Signal"] = -1

    return data