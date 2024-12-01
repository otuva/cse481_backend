from binance.client import Client
from app.config import Config
from app.enums import CryptoSymbols
from typing import Dict, Any

client = Client(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET, testnet=Config.TESTNET)

def fetch_market_data(symbol: CryptoSymbols) -> Dict[str, Any]:
    """Fetch real-time market data for a given symbol."""
    klines = client.get_klines(symbol=symbol.value, interval=Client.KLINE_INTERVAL_15MINUTE, limit=50)
    return [{"time": k[0], "open": float(k[1]), "close": float(k[4])} for k in klines]

def execute_trade(symbol: CryptoSymbols, side: str, quantity: float):
    """Place an order on Binance."""
    return client.create_order(symbol=symbol.value, side=side, type=Client.ORDER_TYPE_MARKET, quantity=quantity)
