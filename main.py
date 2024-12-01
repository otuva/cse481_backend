from flask import Flask, jsonify
import bot  # Import the bot module

app = Flask(__name__)

@app.route("/start_bot", methods=["POST"])
def start_bot():
    """Start the trading bot."""
    response, status = bot.start_bot()
    return jsonify(response), status


@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    """Stop the trading bot."""
    response, status = bot.stop_bot()
    return jsonify(response), status


@app.route("/status", methods=["GET"])
def status():
    """Get the bot status."""
    return jsonify({"bot_running": bot.bot_running})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
