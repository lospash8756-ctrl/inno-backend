from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Deine Server-Daten
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486

@app.route('/')
def index():
    # Wir übergeben die IP und den Port an die Website
    return render_template('index.html', host=MC_HOST, port=MC_PORT)

if __name__ == '__main__':
    print(f"Starte Website für Voice Chat auf http://localhost:5000")
    print(f"Ziel-Server: {MC_HOST}:{MC_PORT}")
    socketio.run(app, host='0.0.0.0', port=5000)
