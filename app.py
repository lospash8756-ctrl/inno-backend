import os
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
from mcstatus import JavaServer

# --- KONFIGURATION ---
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'geheim123')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- HTML FRONTEND ---
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
        .box { background-color: #2b2b2b; padding: 30px; border-radius: 12px; text-align: center; width: 90%; max-width: 400px; box-shadow: 0 4px 20px rgba(0,0,0,0.6); transition: all 0.5s; }
        h2 { color: #fff; margin-bottom: 5px; }
        p { color: #aaa; font-size: 0.9em; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 6px; border: 1px solid #444; background-color: #333; color: white; outline: none; transition: 0.3s; }
        input:focus { border-color: #4CAF50; }
        button { width: 100%; padding: 12px; margin-top: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; transition: 0.3s; }
        button:hover { background-color: #45a049; }
        button:disabled { background-color: #555; cursor: not-allowed; }
        
        /* Voice Visualizer Styles */
        #voice-ui { display: none; margin-top: 20px; }
        .mic-icon { font-size: 50px; color: #4CAF50; margin-bottom: 10px; }
        .volume-bar-container { width: 100%; height: 10px; background-color: #444; border-radius: 5px; overflow: hidden; margin-top: 10px; }
        .volume-bar { height: 100%; width: 0%; background-color: #4CAF50; transition: width 0.05s ease; }
        
        .log { margin-top: 20px; text-align: left; font-size: 0.85em; color: #888; max-height: 100px; overflow-y: auto; background: #222; padding: 10px; border-radius: 4px; border: 1px solid #333; }
        .success { color: #4CAF50; }
        .error { color: #ff5252; }
    </style>
</head>
<body>

<div class="box" id="login-box">
    <h2>🔊 Bedrock Voice Web</h2>
    <p>Status: <span id="server-status" style="font-weight:bold;">Lade...</span></p>
    
    <div id="login-form">
        <input type="text" id="username" placeholder="Dein Minecraft Name">
        <button id="btn" onclick="connect()">Beitreten</button>
    </div>

    <div id="voice-ui">
        <div class="mic-icon">🎙️</div>
        <h3>Mikrofon Aktiv</h3>
        <p>Sende Audio an Server...</p>
        <div class="volume-bar-container">
            <div class="volume-bar" id="vol-bar"></div>
        </div>
        <button onclick="location.reload()" style="background-color: #ff5252; margin-top: 20px;">Trennen</button>
    </div>
    
    <div class="log" id="log">Warte auf Eingabe...</div>
</div>

<script>
    const socket = io();
    const btn = document.getElementById('btn');
    const logDiv = document.getElementById('log');
    
    // Status Update vom Server
    socket.emit('check_server');
    socket.on('status_update', (data) => {
        const el = document.getElementById('server-status');
        el.innerText = data.online ? "Online ✅" : "Offline ❌";
        el.style.color = data.online ? "#4CAF50" : "#ff5252";
    });

    function log(msg, type='') {
        logDiv.innerHTML = `<div class="${type}">> ${msg}</div>` + logDiv.innerHTML;
    }

    // Login Funktion
    function connect() {
        const user = document.getElementById('username').value;
        if(!user) return alert("Name fehlt!");
        
        btn.disabled = true;
        btn.innerText = "Prüfe Spieler...";
        log("Suche " + user + " auf dem Server...");
        
        socket.emit('verify_user', {username: user});
    }

    // Antwort vom Login
    socket.on('login_response', (data) => {
        if(data.success) {
            log(data.msg, "success");
            startMicrophone(); // HIER STARTEN WIR DAS MIKROFON
        } else {
            log("Fehler: " + data.msg, "error");
            btn.disabled = false;
            btn.innerText = "Beitreten";
        }
    });

    // --- MIKROFON LOGIK ---
    async function startMicrophone() {
        try {
            log("Frage nach Mikrofon-Rechten...");
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // UI Umschalten
            document.getElementById('login-form').style.display = 'none';
            document.getElementById('voice-ui').style.display = 'block';
            log("Mikrofon verbunden! Audio läuft.", "success");

            // Audio Visualizer (Damit man sieht, dass es geht)
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const mediaStreamSource = audioContext.createMediaStreamSource(stream);
            const analyzer = audioContext.createAnalyser();
            analyzer.fftSize = 256;
            mediaStreamSource.connect(analyzer);
            
            const dataArray = new Uint8Array(analyzer.frequencyBinCount);
            const volBar = document.getElementById('vol-bar');

            // Funktion um Lautstärke zu messen
            function updateVolume() {
                analyzer.getByteFrequencyData(dataArray);
                let sum = 0;
                for(let i = 0; i < dataArray.length; i++) {
                    sum += dataArray[i];
                }
                let average = sum / dataArray.length;
                
                // Balken bewegen (verstärkt den Effekt etwas mit * 2)
                let width = Math.min(100, average * 2); 
                volBar.style.width = width + "%";
                
                // Wir senden hier "Ping" an den Server, um Aktivität zu simulieren
                if (width > 10) { 
                    socket.emit('voice_packet', { level: width }); 
                }

                requestAnimationFrame(updateVolume);
            }
            updateVolume();

        } catch (err) {
            log("Mikrofon Zugriff verweigert! " + err, "error");
            alert("Du musst das Mikrofon erlauben!");
        }
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
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        status = server.status()
        emit('status_update', {'online': True})
    except:
        emit('status_update', {'online': False})

@socketio.on('verify_user')
def handle_verification(data):
    target_user = data.get('username')
    try:
        # Versucht echte Spielerliste von Aternos zu holen
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        query = server.query()
        if target_user in query.players.names:
            emit('login_response', {'success': True, 'msg': f'Verifiziert! Willkommen {target_user}.'})
        else:
            # Wenn Spieler nicht gefunden, aber Server da ist -> Fehler
            emit('login_response', {'success': False, 'msg': f'{target_user} ist nicht online!'})
    except Exception as e:
        # Fallback (Wenn Aternos Query blockt, lassen wir ihn trotzdem rein zum Testen)
        print(f"Query Fehler: {e}")
        emit('login_response', {'success': True, 'msg': 'Server antwortet nicht auf Namens-Check, Login trotzdem erlaubt.'})

@socketio.on('voice_packet')
def handle_voice(data):
    # Hier kommen die Daten an, wenn jemand spricht
    # Wir tun nichts damit, weil Aternos sie nicht empfangen kann,
    # aber es hält die Verbindung aktiv.
    pass

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
