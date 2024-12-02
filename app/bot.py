from datetime import date
from binance.client import Client
from app.config import Config
from app.enums import CryptoSymbols, KlineIntervals, TradeSide
from typing import Dict, Any, List

client = Client(
    api_key=Config.BINANCE_API_KEY,
    api_secret=Config.BINANCE_API_SECRET,
    testnet=Config.TESTNET
)


def process_klines(klines: List) -> List[Dict[str, Any]]:
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


def fetch_historical_data(
    symbol: CryptoSymbols,
    interval: KlineIntervals,
    start_date: date,
    end_date: date
) -> List[Dict[str, Any]]:
    """
    Fetch historical market data for a given symbol and time range.

    Args:
        symbol (CryptoSymbols): The cryptocurrency symbol (e.g., CryptoSymbols.BTCUSDT).
        interval (KlineIntervals): The interval for Klines (e.g., KlineIntervals.T15MINUTE).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: Historical data as a DataFrame with OHLC and additional information.
    """

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    klines = client.get_historical_klines(
        symbol.value,
        interval.value,
        start_date_str,
        end_date_str
    )

    return process_klines(klines)


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

    return process_klines(klines)


def place_trade(symbol: CryptoSymbols, side: TradeSide, quantity: float) -> Dict:
    """
    Place a trade (buy or sell) on Binance.

    Args:
        symbol (CryptoSymbols): The cryptocurrency symbol to trade (e.g., CryptoSymbols.BTCUSDT).
        side (TradeSide): The trade side, either TradeSide.BUY or TradeSide.SELL.
        quantity (float): The quantity of the asset to trade.

    Returns:
        Dict: The response from the Binance API for the trade.
    """
    # Create the order
    order = client.create_order(
        symbol=symbol.value,
        side=side.value,  # Convert TradeSide enum to string
        type=Client.ORDER_TYPE_MARKET,
        quantity=quantity
    )
    return order
