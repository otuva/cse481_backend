from flask import Flask, jsonify, request
import threading
import bot  # Import the bot module

app = Flask(__name__)

@app.route("/start_bot", methods=["POST"])
def start_bot():
    """Start the trading bot."""
    if bot.bot_running:
        return jsonify({"message": "Bot is already running."}), 400

    bot.bot_running = True
    bot.bot_thread = threading.Thread(target=bot.trading_bot)
    bot.bot_thread.start()

    return jsonify({"message": "Bot started successfully."})


@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    """Stop the trading bot."""
    if not bot.bot_running:
        return jsonify({"message": "Bot is not running."}), 400

    bot.bot_running = False
    if bot.bot_thread:
        bot.bot_thread.join()

    return jsonify({"message": "Bot stopped successfully."})


@app.route("/status", methods=["GET"])
def status():
    """Get the bot status."""
    return jsonify({"bot_running": bot.bot_running})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
