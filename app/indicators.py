import pandas as pd
import pandas_ta as ta

def calculate_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """Apply technical indicators to the market data."""
    data["SMA"] = ta.sma(data["close"], length=20)
    data["EMA"] = ta.ema(data["close"], length=20)
    data["RSI"] = ta.rsi(data["close"], length=14)
    data["BB_upper"], data["BB_middle"], data["BB_lower"] = ta.bbands(data["close"], length=20)
    data["MACD"], data["MACD_signal"], _ = ta.macd(data["close"], fast=12, slow=26, signal=9)
    data["SuperTrend"] = ta.supertrend(data["high"], data["low"], data["close"])["SUPERT_7_3.0"]
    return data
