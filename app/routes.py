from flask import Blueprint, Response, jsonify, request
from app.bot import fetch_market_data
from app.indicators import calculate_indicators
from app.enums import CryptoSymbols, KlineIntervals
import pandas as pd

routes = Blueprint("routes", __name__)


@routes.route("/api/market-data/symbols", methods=["GET"])
def get_valid_symbols():
    """Return a list of valid cryptocurrency symbols."""
    valid_symbols = [symbol.name for symbol in CryptoSymbols]
    return jsonify({"symbols": valid_symbols})


@routes.route("/api/market-data/symbols/intervals", methods=["GET"])
def get_valid_intervals():
    """Return a list of valid intervals for Klines."""
    valid_intervals = [interval.name for interval in KlineIntervals]
    return jsonify({"intervals": valid_intervals})


@routes.route("/api/market-data/<symbol>/<interval>", methods=["GET"])
def get_market_data(symbol, interval):
    try:
        crypto_symbol = CryptoSymbols[symbol]
        kline_interval = KlineIntervals[interval]
    except KeyError:
        return jsonify({"error": "Invalid"}), 400

    data = fetch_market_data(crypto_symbol, kline_interval, 50)
    df = pd.DataFrame(data)
    indicators = calculate_indicators(df)
    return Response(indicators.to_json(orient="records"), mimetype='application/json')
