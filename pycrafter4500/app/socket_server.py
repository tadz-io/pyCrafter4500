from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    return "Socket server is running"


# Receive data from Streamlit and forward to the client
@socketio.on("send_command")
def handle_send_command(data):
    emit("relay_to_client", data, broadcast=True)  # Broadcast to all connected clients


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8765)
