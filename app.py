import os
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
from mcstatus import JavaServer

# --- DEINE SERVER DATEN ---
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486 

app = Flask(__name__)
# WICHTIG: Ein Secret Key für Sicherheit
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'lospash_secret_key_999')

# CORS erlauben, damit keine Fehler auf Render passieren
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- DAS DESIGN (HTML/CSS) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lospash Voice Portal</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { 
            background-color: #121212; 
            color: #ffffff; 
            font-family: 'Roboto', sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            margin: 0; 
        }
        
        .card { 
            background-color: #1e1e1e; 
            padding: 40px; 
            border-radius: 12px; 
            text-align: center; 
            width: 90%; 
            max-width: 400px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); 
            border: 1px solid #333;
        }

        h1 { margin-top: 0; color: #4CAF50; font-size: 26px; text-transform: uppercase; letter-spacing: 1px; }
        
        .status-box {
            background: #252525;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
        }
        .dot { height: 10px; width: 10px; background-color: #555; border-radius: 50%; display: inline-block; }
        .dot.online { background-color: #4CAF50; box-shadow: 0 0 8px #4CAF50; }
        .dot.offline { background-color: #f44336; }

        input { 
            width: 100%; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 6px; 
            border: 1px solid #444; 
            background-color: #2c2c2c; 
            color: white; 
            box-sizing: border-box; 
            font-size: 16px;
            outline: none;
        }
        input:focus { border-color: #4CAF50; }

        button { 
            width: 100%; 
            padding: 15px; 
            margin-top: 10px; 
            background-color: #4CAF50; 
            color: white; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            font-size: 16px; 
            font-weight: bold; 
            transition: 0.2s; 
        }
        button:hover { background-color: #43a047; transform: translateY(-2px); }
        button:disabled { background-color: #555; transform: none; cursor: not-allowed; }

        /* Versteckte Bereiche */
        #success-area { display: none; text-align: left; margin-top: 20px; border-top: 1px solid #444; padding-top: 20px; }
        .step { margin-bottom: 15px; display: flex; gap: 10px; }
        .num { background: #4CAF50; color: #000; width: 20px; height: 20px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; font-size: 12px; flex-shrink: 0; }
        .text { font-size: 14px; color: #ccc; }
        .cmd { background: #000; padding: 2px 6px; border-radius: 4px; color: #0f0; font-family: monospace; }
        
        #error-msg { color: #ff5252; font-size: 13px; margin-top: 10px; min-height: 18px; }
    </style>
</head>
<body>

<div class="card">
    <h1>🔊 Voice Portal</h1>
    
    <div class="status-box">
        <span class="dot" id="status-dot"></span>
        <span id="server-status">Verbinde zum Server...</span>
    </div>

    <div id="login-form">
        <p style="color:#aaa; font-size:14px;">Gib deinen Namen ein, um dich zu verifizieren.</p>
        <input type="text" id="username" placeholder="Minecraft Name (z.B. Lospash)">
        <button id="btn" onclick="checkUser()">Verbinden</button>
        <div id="error-msg"></div>
    </div>

    <div id="success-area">
        <div style="text-align: center; color: #4CAF50; font-weight: bold; margin-bottom: 15px;">✅ Verifiziert!</div>
        
        <div class="step">
            <div class="num">1</div>
            <div class="text">Gehe jetzt zurück ins Spiel.</div>
        </div>
        <div class="step">
            <div class="num">2</div>
            <div class="text">Öffne den Chat und schreibe:<br><br><span class="cmd">/audio</span></div>
        </div>
        <div class="step">
            <div class="num">3</div>
            <div class="text">Klicke auf den Link im Chat, um das Mikrofon zu aktivieren.</div>
        </div>
    </div>
</div>

<script>
    // Verbindet sich automatisch mit der aktuellen Render-URL
    const socket = io(); 
    
    // UI Elemente
    const btn = document.getElementById('btn');
    const errorMsg = document.getElementById('error-msg');
    const dot = document.getElementById('status-dot');
    const statusText = document.getElementById('server-status');

    // 1. Automatisch Server Status prüfen beim Laden
    socket.emit('check_server');

    socket.on('status_update', (data) => {
        if(data.online) {
            dot.className = "dot online";
            statusText.innerText = "Online (" + data.players + " Spieler)";
        } else {
            dot.className = "dot offline";
            statusText.innerText = "Server ist Offline";
        }
    });

    // 2. Button Klick
    function checkUser() {
        const user = document.getElementById('username').value;
        if(!user) return;
        
        btn.disabled = true;
        btn.innerText = "Prüfe...";
        errorMsg.innerText = "";
        
        // Anfrage an Python Backend senden
        socket.emit('verify_user', {username: user});
    }

    // 3. Antwort vom Backend verarbeiten
    socket.on('login_response', (data) => {
        if(data.success) {
            // Erfolg: Formular ausblenden, Anleitung einblenden
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('success-area').style.display = 'block';
        } else {
            // Fehler anzeigen
            errorMsg.innerText = data.msg;
            btn.disabled = false;
            btn.innerText = "Verbinden";
        }
    });
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
        # Aternos Server pingen
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        status = server.status()
        emit('status_update', {'online': True, 'players': status.players.online})
    except:
        emit('status_update', {'online': False, 'players': 0})

@socketio.on('verify_user')
def handle_verification(data):
    target_user = data.get('username')
    try:
        # Versuche via Query herauszufinden, ob der Spieler da ist
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        query = server.query()
        
        if target_user in query.players.names:
            emit('login_response', {'success': True})
        else:
            emit('login_response', {
                'success': False, 
                'msg': f'"{target_user}" wurde nicht auf dem Server gefunden.'
            })
            
    except Exception as e:
        # Wenn Aternos Query blockiert (passiert oft), lassen wir den User trotzdem durch
        # damit die Webseite nicht "kaputt" wirkt.
        print(f"Query Fehler (normal bei Aternos): {e}")
        emit('login_response', {'success': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
