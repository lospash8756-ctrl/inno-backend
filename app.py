import os
from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')

# WICHTIG: cors_allowed_origins="*" erlaubt deiner React App den Zugriff
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Deine Minecraft Server Daten (Nur zur Info)
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486

@app.route('/')
def index():
    return f"Voice Chat Backend läuft. Verbinde deine React App hierher."

@socketio.on('connect')
def test_connect():
    print('Client verbunden!')
    emit('status', {'msg': 'Verbunden mit Python Backend!'})

@socketio.on('join_request')
def handle_join(data):
    username = data.get('username')
    print(f"Spieler {username} versucht Beitritt...")
    # Hier würde normalerweise die Weiterleitung an Aternos passieren
    # Da Aternos blockt, simulieren wir Erfolg, damit die Website nicht abstürzt
    emit('status', {'msg': f'Hallo {username}, Backend ist bereit.'})

if __name__ == '__main__':
    # WICHTIG: Port muss aus der Umgebungsvariable kommen!
    port = int(os.environ.get("PORT", 5000))
    print(f"Starte Server auf Port {port}")
    socketio.run(app, host='0.0.0.0', port=port)
