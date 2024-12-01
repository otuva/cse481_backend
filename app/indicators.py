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
