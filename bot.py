from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
import pandas as pd
import time

# Load environment variables from .env file
load_dotenv()

# Binance API keys
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Parameters for the bot
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1MINUTE
short_window = 5
long_window = 15
trade_amount = 0.001

# Global variables for bot status
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
    return df[['timestamp', 'close']]

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
    in_position = False  # Track if we hold the asset

    while bot_running:
        try:
            # Fetch historical data
            data = fetch_klines(symbol, interval)

            # Calculate SMAs
            data['sma_short'] = calculate_sma(data, short_window)
            data['sma_long'] = calculate_sma(data, long_window)

            # Get the latest SMA values
            sma_short = data['sma_short'].iloc[-1]
            sma_long = data['sma_long'].iloc[-1]
            print(f"SMA Short: {sma_short}, SMA Long: {sma_long}")

            # Trading logic
            if sma_short > sma_long and not in_position:
                print("Bullish crossover detected! Placing a BUY order...")
                place_order(symbol, SIDE_BUY, trade_amount)
                in_position = True

            elif sma_short < sma_long and in_position:
                print("Bearish crossover detected! Placing a SELL order...")
                place_order(symbol, SIDE_SELL, trade_amount)
                in_position = False

            # Wait before the next iteration
            time.sleep(60)

        except Exception as e:
            print(f"Error in the bot: {e}")
            time.sleep(60)
