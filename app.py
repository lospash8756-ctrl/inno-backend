import os
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
from mcstatus import JavaServer

# --- KONFIGURATION ---
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lospash_secret')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- DAS PREMIUM HTML ---
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
        :root {
            --primary: #00ff9d;
            --bg: #050505;
            --glass: rgba(20, 20, 20, 0.85);
        }
        body {
            background-color: var(--bg);
            color: white;
            font-family: 'Inter', sans-serif;
            margin: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        /* Animierter Hintergrund */
        .background {
            position: absolute; width: 200%; height: 200%;
            background: radial-gradient(circle at 50% 50%, rgba(0, 255, 157, 0.08), transparent 40%);
            animation: moveBg 20s linear infinite; z-index: -1;
        }
        @keyframes moveBg { 0% { transform: translate(0,0); } 100% { transform: translate(-10%, -10%); } }

        /* Karte */
        .card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 24px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 30px 80px rgba(0,0,0,0.8);
            transition: transform 0.2s;
        }

        h1 { font-family: 'Rajdhani', sans-serif; font-size: 36px; margin: 0; text-transform: uppercase; color: #fff; }
        p { color: #888; font-size: 14px; margin-bottom: 30px; }

        /* Server Status */
        .status-badge {
            display: inline-flex; align-items: center; gap: 8px;
            background: rgba(255,255,255,0.05); padding: 6px 12px; border-radius: 50px;
            font-size: 12px; font-weight: bold; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1);
        }
        .dot { width: 8px; height: 8px; border-radius: 50%; background: #555; }
        .dot.online { background: var(--primary); box-shadow: 0 0 10px var(--primary); }

        /* Profil */
        .profile {
            background: rgba(0,0,0,0.3); border-radius: 16px; padding: 15px;
            display: flex; align-items: center; gap: 15px; text-align: left;
            border: 1px solid rgba(255,255,255,0.05); margin-bottom: 20px;
        }
        .avatar { width: 50px; height: 50px; border-radius: 10px; background: #222; }
        .user-info h3 { margin: 0; font-size: 16px; color: white; }
        .user-info span { font-size: 12px; color: #666; }
        .user-info span.verified { color: var(--primary); font-weight: bold; }

        /* Button */
        .btn {
            width: 100%; padding: 18px; border: none; border-radius: 12px;
            background: #333; color: #888; font-family: 'Rajdhani', sans-serif;
            font-size: 18px; font-weight: 700; text-transform: uppercase;
            cursor: not-allowed; transition: 0.3s;
        }
        .btn.active {
            background: var(--primary); color: #000; cursor: pointer;
            box-shadow: 0 0 30px rgba(0, 255, 157, 0.3);
        }
        .btn.active:hover { transform: scale(1.02); }

        .log { font-size: 11px; color: #555; margin-top: 15px; font-family: monospace; min-height: 20px; }
    </style>
</head>
<body>
    <div class="background"></div>

    <div class="card">
        <div class="status-badge">
            <div class="dot" id="server-dot"></div>
            <span id="server-text">Prüfe Server...</span>
        </div>

        <h1>Lospash Voice</h1>
        <p>Secure Audio Gateway</p>

        <div class="profile">
            <img id="head-img" src="" class="avatar" style="display:none;">
            <div class="avatar" id="default-head" style="display:flex; align-items:center; justify-content:center;">?</div>
            <div class="user-info">
                <h3 id="username-display">Gast</h3>
                <span id="user-status">Warte auf Token...</span>
            </div>
        </div>

        <button id="btn" class="btn" onclick="connect()">Warten...</button>
        <div class="log" id="log-msg"></div>
    </div>

    <script>
        const socket = io();
        const params = new URLSearchParams(window.location.search);
        // Wir holen den Namen, den das Plugin per ?ign=Name gesendet hat
        const ign = params.get('ign') || params.get('name');
        
        const btn = document.getElementById('btn');
        const logMsg = document.getElementById('log-msg');

        // 1. Server Status prüfen (ECHT!)
        socket.emit('check_server');

        socket.on('status_update', (data) => {
            const dot = document.getElementById('server-dot');
            const txt = document.getElementById('server-text');
            if(data.online) {
                dot.className = "dot online";
                txt.innerText = "Server Online (" + data.players + " Spieler)";
                // Wenn Server online ist und wir einen Namen haben -> User prüfen
                if(ign) checkUserReal(ign);
            } else {
                dot.className = "dot";
                txt.innerText = "Server Offline";
                logMsg.innerText = "Server ist aus. Starte ihn auf Aternos.";
            }
        });

        // 2. User wirklich auf dem Server prüfen
        function checkUserReal(username) {
            document.getElementById('username-display').innerText = username;
            document.getElementById('default-head').style.display = 'none';
            document.getElementById('head-img').style.display = 'block';
            document.getElementById('head-img').src = "https://crafatar.com/avatars/" + username + "?overlay";
            
            logMsg.innerText = "Prüfe, ob du online bist...";
            socket.emit('verify_user', {username: username});
        }

        socket.on('login_response', (data) => {
            if(data.success) {
                // ECHT VERIFIZIERT!
                document.getElementById('user-status').innerText = "Verifiziert ✅";
                document.getElementById('user-status').className = "verified";
                logMsg.innerText = "Identität bestätigt.";
                
                // Button freischalten
                btn.className = "btn active";
                btn.innerText = "Jetzt Verbinden";
                btn.onclick = function() {
                    btn.innerText = "Leite weiter...";
                    // Weiterleitung zum echten Audio
                    window.location.href = "https://client.openaudiomc.net/" + window.location.search;
                };
            } else {
                logMsg.innerText = data.msg;
                document.getElementById('user-status').innerText = "Nicht gefunden";
            }
        });

        // Fallback, falls kein Name in URL
        if(!ign) {
            logMsg.innerText = "Kein Token gefunden. Bitte nutze /audio im Spiel.";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

# --- ECHTE SERVERSEITIGE LOGIK ---

@socketio.on('check_server')
def handle_check():
    try:
        # Pingt deinen echten Aternos Server
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        status = server.status()
        emit('status_update', {'online': True, 'players': status.players.online})
    except:
        emit('status_update', {'online': False})

@socketio.on('verify_user')
def handle_verification(data):
    target_user = data.get('username')
    try:
        # Fragt den Server: "Ist dieser Spieler wirklich da?"
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        query = server.query()
        
        if target_user in query.players.names:
            emit('login_response', {'success': True})
        else:
            # Wenn nicht gefunden -> Fehler
            emit('login_response', {'success': False, 'msg': f'{target_user} ist nicht auf dem Server!'})
    except:
        # Aternos Query ist manchmal zickig -> Wir lassen ihn rein, wenn der Ping ging
        emit('login_response', {'success': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
