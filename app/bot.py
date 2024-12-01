from binance.client import Client
from app.config import Config
from app.enums import CryptoSymbols, KlineIntervals
from typing import Dict, Any, List

client = Client(
    api_key=Config.BINANCE_API_KEY,
    api_secret=Config.BINANCE_API_SECRET,
    testnet=Config.TESTNET
)


def fetch_market_data(symbol: CryptoSymbols, interval: KlineIntervals, limit: int) -> List[Dict[str, Any]]:
    """
    Fetch real-time market data for a given symbol.

    Args:
        symbol (CryptoSymbols): The cryptocurrency symbol (e.g., CryptoSymbols.BTCUSDT).
        interval (KlineIntervals): The interval for Klines (e.g., KlineIntervals.T15MINUTE).
        limit (int): Number of Klines to retrieve.

    Returns:
        List[Dict[str, Any]]: Processed market data with key indicators for each Kline.
    """
    klines = client.get_klines(
        symbol=symbol.value,
        interval=interval.value,
        limit=limit
    )

    processed_klines = []
    for kline in klines:
        processed_klines.append({
            'open_time': kline[0],
            'open': float(kline[1]),
            'high': float(kline[2]),
            'low': float(kline[3]),
            'close': float(kline[4]),
            'volume': float(kline[5]),
            'close_time': kline[6],
            'quote_asset_volume': float(kline[7]),
            'number_of_trades': kline[8],
            'taker_buy_base_asset_volume': float(kline[9]),
            'taker_buy_quote_asset_volume': float(kline[10])
        })

    return processed_klines
