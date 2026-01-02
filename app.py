import os
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
from mcstatus import JavaServer

# --- DEINE SERVER DATEN ---
# Prüfe bitte auf Aternos, ob dieser Port noch stimmt!
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lospash_super_secret')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- DAS ULTIMATIVE DESIGN ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lospash Voice</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #00ff9d; --bg: #050505; --glass: rgba(20, 20, 20, 0.85); }
        body { background-color: var(--bg); color: white; font-family: 'Inter', sans-serif; margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
        
        /* Hintergrund & Partikel */
        .background { position: absolute; width: 200%; height: 200%; background: radial-gradient(circle at 50% 50%, rgba(0, 255, 157, 0.08), transparent 40%); animation: moveBg 20s linear infinite; z-index: -2; }
        @keyframes moveBg { 0% { transform: translate(0,0); } 100% { transform: translate(-10%, -10%); } }
        
        /* Karte */
        .card { background: var(--glass); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1); padding: 40px; border-radius: 24px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 30px 80px rgba(0,0,0,0.8); position: relative; }
        
        h1 { font-family: 'Rajdhani', sans-serif; font-size: 36px; margin: 0; text-transform: uppercase; color: #fff; text-shadow: 0 0 20px rgba(0,255,157,0.5); }
        p { color: #888; font-size: 14px; margin-bottom: 30px; }

        /* Status Badge */
        .status-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 50px; font-size: 12px; font-weight: bold; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1); }
        .dot { width: 8px; height: 8px; border-radius: 50%; background: #555; transition: 0.3s; }
        .dot.online { background: var(--primary); box-shadow: 0 0 10px var(--primary); }

        /* Profil Anzeige */
        .profile { background: rgba(0,0,0,0.3); border-radius: 16px; padding: 15px; display: flex; align-items: center; gap: 15px; text-align: left; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px; transition: 0.3s; }
        .avatar { width: 50px; height: 50px; border-radius: 10px; background: #222; object-fit: cover; }
        .user-info h3 { margin: 0; font-size: 16px; color: white; }
        .user-info span { font-size: 12px; color: #666; }
        .verified { color: var(--primary) !important; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }

        /* Button */
        .btn { width: 100%; padding: 18px; border: none; border-radius: 12px; background: #333; color: #888; font-family: 'Rajdhani', sans-serif; font-size: 18px; font-weight: 700; text-transform: uppercase; cursor: not-allowed; transition: 0.3s; margin-top: 10px; }
        .btn.active { background: var(--primary); color: #000; cursor: pointer; box-shadow: 0 0 30px rgba(0, 255, 157, 0.3); }
        .btn.active:hover { transform: scale(1.02); box-shadow: 0 0 50px rgba(0, 255, 157, 0.5); }

        .log { font-size: 11px; color: #555; margin-top: 15px; font-family: monospace; min-height: 15px; }
    </style>
</head>
<body>
    <div class="background"></div>

    <div class="card">
        <div class="status-badge">
            <div class="dot" id="server-dot"></div>
            <span id="server-text">Verbinde zum Server...</span>
        </div>

        <h1>Lospash Voice</h1>
        <p>Premium Audio Experience</p>

        <div class="profile" id="profile-box">
            <img id="head-img" src="" class="avatar" style="display:none;">
            <div class="avatar" id="default-head" style="display:flex; align-items:center; justify-content:center;">?</div>
            <div class="user-info">
                <h3 id="username-display">Gast</h3>
                <span id="user-status">Warte auf Token...</span>
            </div>
        </div>

        <button id="btn" class="btn" onclick="connect()">Bitte warten...</button>
        <div class="log" id="log-msg">Initialisiere System...</div>
    </div>

    <script>
        const socket = io();
        const params = new URLSearchParams(window.location.search);
        const ign = params.get('ign') || params.get('name'); // Name aus der URL
        const btn = document.getElementById('btn');
        const logMsg = document.getElementById('log-msg');

        // 1. Server Status Check
        socket.emit('check_server');

        socket.on('status_update', (data) => {
            const dot = document.getElementById('server-dot');
            const txt = document.getElementById('server-text');
            if(data.online) {
                dot.className = "dot online";
                txt.innerText = "Server Online (" + data.players + " Spieler)";
                if(ign) verifyUser(ign); // Wenn Server an ist, User prüfen
                else logMsg.innerText = "Kein Spielername erkannt.";
            } else {
                dot.className = "dot";
                txt.innerText = "Server Offline";
                logMsg.innerText = "Bitte starte den Server auf Aternos.";
            }
        });

        // 2. User Verifikation
        function verifyUser(username) {
            document.getElementById('username-display').innerText = username;
            document.getElementById('default-head').style.display = 'none';
            document.getElementById('head-img').style.display = 'block';
            document.getElementById('head-img').src = "https://crafatar.com/avatars/" + username + "?overlay";
            
            logMsg.innerText = "Prüfe Anwesenheit...";
            socket.emit('verify_user', {username: username});
        }

        socket.on('login_response', (data) => {
            if(data.success) {
                // Erfolg!
                document.getElementById('user-status').innerText = "Verifiziert ✅";
                document.getElementById('user-status').className = "verified";
                document.getElementById('profile-box').style.borderColor = "var(--primary)";
                logMsg.innerText = "Bereit zum Verbinden.";
                
                btn.className = "btn active";
                btn.innerText = "Jetzt Verbinden";
                btn.onclick = function() {
                    btn.innerText = "Leite weiter...";
                    // Weiterleitung zur echten OpenAudio Engine
                    window.location.href = "https://client.openaudiomc.net/" + window.location.search;
                };
            } else {
                // User nicht gefunden
                logMsg.innerText = data.msg;
                document.getElementById('user-status').innerText = "Nicht Online ❌";
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

# --- BACKEND LOGIK ---
@socketio.on('check_server')
def handle_check():
    try:
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        status = server.status()
        emit('status_update', {'online': True, 'players': status.players.online})
    except:
        emit('status_update', {'online': False, 'players': 0})

@socketio.on('verify_user')
def handle_verification(data):
    target = data.get('username')
    try:
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        query = server.query()
        if target in query.players.names:
            emit('login_response', {'success': True})
        else:
            emit('login_response', {'success': False, 'msg': f'{target} ist nicht online!'})
    except:
        # Falls Query geblockt ist, lassen wir den Spieler trotzdem durch (Fallback)
        emit('login_response', {'success': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
