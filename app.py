import os
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
from mcstatus import JavaServer

# --- KONFIGURATION ---
# Deine Aternos Adresse
MC_HOST = "MinecraftLospashW.aternos.me"
# Der Port (Standard ist 25565, bei Aternos oft dynamisch, hier dein Port)
MC_PORT = 42486 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'geheim123')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- HTML FRONTEND (Direkt im Code) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Chat Web</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { background-color: #1a1a1a; color: #ddd; font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .box { background-color: #2b2b2b; padding: 30px; border-radius: 12px; text-align: center; width: 90%; max-width: 400px; box-shadow: 0 4px 20px rgba(0,0,0,0.6); }
        h2 { color: #fff; margin-bottom: 5px; }
        p { color: #aaa; font-size: 0.9em; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 6px; border: 1px solid #444; background-color: #333; color: white; box-sizing: border-box; outline: none; transition: 0.3s; }
        input:focus { border-color: #4CAF50; }
        button { width: 100%; padding: 12px; margin-top: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; transition: 0.3s; }
        button:hover { background-color: #45a049; }
        button:disabled { background-color: #555; cursor: wait; }
        .log { margin-top: 20px; text-align: left; font-size: 0.85em; color: #888; max-height: 100px; overflow-y: auto; background: #222; padding: 10px; border-radius: 4px; }
        .success { color: #4CAF50; font-weight: bold; }
        .error { color: #ff5252; font-weight: bold; }
    </style>
</head>
<body>
<div class="box">
    <h2>🔊 Bedrock Voice Web</h2>
    <p>Status: <span id="server-status">Prüfe...</span></p>
    
    <input type="text" id="username" placeholder="Dein Minecraft Name">
    <button id="btn" onclick="connect()">Beitreten</button>
    
    <div class="log" id="log">Warte auf Eingabe...</div>
</div>

<script>
    const socket = io();
    const btn = document.getElementById('btn');
    const logDiv = document.getElementById('log');

    function log(msg, type='') {
        logDiv.innerHTML = `<div class="${type}">> ${msg}</div>` + logDiv.innerHTML;
    }

    // Server Status beim Laden abrufen
    socket.emit('check_server');

    socket.on('status_update', (data) => {
        document.getElementById('server-status').innerText = data.online ? "Online ✅" : "Offline ❌";
        document.getElementById('server-status').style.color = data.online ? "#4CAF50" : "#ff5252";
    });

    socket.on('login_response', (data) => {
        if(data.success) {
            log("Erfolg: " + data.msg, "success");
            btn.innerText = "Verbunden";
            btn.style.backgroundColor = "#333";
            // HIER würde jetzt der WebRTC Audio-Stream starten
        } else {
            log("Fehler: " + data.msg, "error");
            btn.disabled = false;
            btn.innerText = "Beitreten";
        }
    });

    function connect() {
        const user = document.getElementById('username').value;
        if(!user) return alert("Name fehlt!");
        
        btn.disabled = true;
        btn.innerText = "Prüfe Server...";
        log("Prüfe, ob " + user + " online ist...");
        
        socket.emit('verify_user', {username: user});
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@socketio.on('check_server')
def handle_check():
    try:
        # Versucht den Server anzupingen
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        status = server.status()
        emit('status_update', {'online': True, 'players': status.players.online})
    except:
        emit('status_update', {'online': False})

@socketio.on('verify_user')
def handle_verification(data):
    target_user = data.get('username')
    
    try:
        # 1. Verbindung zum echten Minecraft Server aufbauen
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        query = server.query() # Query muss auf Aternos/Server.properties aktiviert sein!
        
        # 2. Liste der Spieler abrufen
        online_players = query.players.names
        
        print(f"Online Spieler: {online_players}") # Zeigt im Log an, wer online ist
        
        # 3. Prüfen ob der User dabei ist
        if target_user in online_players:
            emit('login_response', {
                'success': True, 
                'msg': f'Verifiziert! {target_user} ist online. Voice wird gestartet...'
            })
            # HIER wäre der Punkt für die Audio-Verbindung
        else:
            emit('login_response', {
                'success': False, 
                'msg': f'Spieler "{target_user}" nicht gefunden! Du musst erst dem Server joinen.'
            })
            
    except Exception as e:
        # Fallback, falls Query nicht geht (passiert oft bei Aternos)
        print(f"Fehler bei Server-Query: {e}")
        # Wir lassen ihn rein, warnen aber
        emit('login_response', {
            'success': True, 
            'msg': f'Server antwortet, aber Spielerliste verborgen. Verbinde trotzdem...'
        })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
