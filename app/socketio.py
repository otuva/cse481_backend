from flask_socketio import SocketIO
import time
from threading import Thread
from app.bot import fetch_market_data
from app.enums import CryptoSymbols

socketio = SocketIO()

def stream_data():
    """Continuously emit market data for all symbols to the frontend."""
    while True:
        updates = {}
        for symbol in CryptoSymbols:
            updates[symbol.name] = fetch_market_data(symbol)
        socketio.emit("market_update", updates)
        time.sleep(10)

def start_stream():
    """Start the background thread for streaming."""
    Thread(target=stream_data).start()
