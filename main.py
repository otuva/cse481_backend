from flask import Flask
from app.routes import routes
from app.socketio import socketio, start_stream
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(routes)

socketio.init_app(app)

if __name__ == "__main__":
    start_stream()
    socketio.run(app, debug=True)
