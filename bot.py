from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
import pandas as pd
import time
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Binance API keys
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Parameters
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1MINUTE
trade_amount = 0.001
rsi_period = 14
rsi_overbought = 70
rsi_oversold = 30
macd_fast = 12
macd_slow = 26
macd_signal = 9
bollinger_window = 20
bollinger_std_dev = 2
supertrend_multiplier = 3
short_window = 5
long_window = 15

# Global variables
bot_running = False
bot_thread = None


def fetch_klines(symbol, interval, limit=500):
    """Fetch historical kline (candlestick) data."""
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    return df[['timestamp', 'open', 'high', 'low', 'close']]


def calculate_rsi(data, period):
    """Calculate the Relative Strength Index (RSI)."""
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_macd(data, fast, slow, signal):
    """Calculate MACD and Signal line."""
    data['ema_fast'] = data['close'].ewm(span=fast, adjust=False).mean()
    data['ema_slow'] = data['close'].ewm(span=slow, adjust=False).mean()
    data['macd'] = data['ema_fast'] - data['ema_slow']
    data['macd_signal'] = data['macd'].ewm(span=signal, adjust=False).mean()
    return data


def calculate_bollinger_bands(data, window, std_dev):
    """Calculate Bollinger Bands."""
    data['bollinger_mid'] = data['close'].rolling(window=window).mean()
    data['bollinger_std'] = data['close'].rolling(window=window).std()
    data['bollinger_upper'] = data['bollinger_mid'] + (std_dev * data['bollinger_std'])
    data['bollinger_lower'] = data['bollinger_mid'] - (std_dev * data['bollinger_std'])
    return data


def calculate_supertrend(data, multiplier):
    """Calculate the SuperTrend indicator."""
    hl2 = (data['high'] + data['low']) / 2
    atr = hl2.rolling(window=14).mean()
    data['supertrend_upper'] = hl2 + (multiplier * atr)
    data['supertrend_lower'] = hl2 - (multiplier * atr)
    data['supertrend'] = np.where(
        data['close'] > data['supertrend_upper'],
        data['supertrend_upper'],
        data['supertrend_lower']
    )
    return data


def calculate_sma(data, window):
    """Calculate the Simple Moving Average (SMA)."""
    return data['close'].rolling(window=window).mean()


def place_order(symbol, side, quantity):
    """Place an order on Binance."""
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(f"Order successful: {order}")
    except Exception as e:
        print(f"An error occurred: {e}")


def trading_bot():
    """Main bot logic."""
    global bot_running
    in_position = False

    while bot_running:
        try:
            # Fetch historical data
            data = fetch_klines(symbol, interval)

            # Calculate indicators
            data['rsi'] = calculate_rsi(data, rsi_period)
            data = calculate_macd(data, macd_fast, macd_slow, macd_signal)
            data = calculate_bollinger_bands(data, bollinger_window, bollinger_std_dev)
            data = calculate_supertrend(data, supertrend_multiplier)
            data['sma_short'] = calculate_sma(data, short_window)
            data['sma_long'] = calculate_sma(data, long_window)

            # Get the latest values
            latest = data.iloc[-1]
            rsi = latest['rsi']
            macd = latest['macd']
            macd_signal = latest['macd_signal']
            bollinger_upper = latest['bollinger_upper']
            bollinger_lower = latest['bollinger_lower']
            supertrend = latest['supertrend']
            sma_short = latest['sma_short']
            sma_long = latest['sma_long']
            close_price = latest['close']

            print(f"RSI: {rsi}, MACD: {macd}, Signal: {macd_signal}")
            print(f"SuperTrend: {supertrend}, SMA Short: {sma_short}, SMA Long: {sma_long}")
            print(f"Bollinger Upper: {bollinger_upper}, Bollinger Lower: {bollinger_lower}")

            # Trading logic
            if rsi < rsi_oversold and close_price < bollinger_lower and not in_position:
                print("Buy Signal: Oversold with RSI and Bollinger Band")
                place_order(symbol, SIDE_BUY, trade_amount)
                in_position = True

            elif rsi > rsi_overbought and close_price > bollinger_upper and in_position:
                print("Sell Signal: Overbought with RSI and Bollinger Band")
                place_order(symbol, SIDE_SELL, trade_amount)
                in_position = False

            elif sma_short > sma_long and not in_position:
                print("Buy Signal: SMA Crossover")
                place_order(symbol, SIDE_BUY, trade_amount)
                in_position = True

            elif sma_short < sma_long and in_position:
                print("Sell Signal: SMA Crossover")
                place_order(symbol, SIDE_SELL, trade_amount)
                in_position = False

            # Wait before the next iteration
            time.sleep(60)

        except Exception as e:
            print(f"Error in the bot: {e}")
            time.sleep(60)
