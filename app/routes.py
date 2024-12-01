from flask import Blueprint, jsonify, request
from app.bot import fetch_market_data, execute_trade
from app.indicators import calculate_indicators
from app.enums import CryptoSymbols
import pandas as pd

routes = Blueprint("routes", __name__)

@routes.route("/api/market-data/<symbol>", methods=["GET"])
def get_market_data(symbol):
    try:
        crypto_symbol = CryptoSymbols[symbol]  # Validate and get CryptoSymbols enum
    except KeyError:
        return jsonify({"error": "Invalid symbol"}), 400

    data = fetch_market_data(crypto_symbol)
    df = pd.DataFrame(data)
    indicators = calculate_indicators(df)
    return jsonify(indicators.tail(5).to_dict(orient="records"))

@routes.route("/api/trade", methods=["POST"])
def place_trade():
    request_data = request.get_json()
    try:
        symbol = CryptoSymbols[request_data.get("symbol")]  # Validate and get CryptoSymbols enum
    except KeyError:
        return jsonify({"error": "Invalid symbol"}), 400

    side = request_data.get("side")
    quantity = request_data.get("quantity")
    result = execute_trade(symbol, side, quantity)
    return jsonify(result)
