import os
from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit

# Flask Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'geheim')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- HIER IST DEIN HTML CODE DIREKT IN PYTHON ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minecraft Voice Chat Login</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        body { background-color: #121212; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { background-color: #1e1e1e; padding: 40px; border-radius: 15px; text-align: center; width: 90%; max-width: 400px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border-radius: 5px; border: 1px solid #333; background-color: #2c2c2c; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 12px; margin-top: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: bold; }
        button:hover { background-color: #45a049; }
        .log-area { margin-top: 20px; background: #000; padding: 10px; border-radius: 5px; font-family: monospace; font-size: 12px; color: #0f0; text-align: left; height: 100px; overflow-y: auto; }
    </style>
</head>
<body>
<div class="container">
    <h2>🔊 Voice Chat Login</h2>
    <p>Server: MinecraftLospashW.aternos.me</p>
    <input type="text" id="username" placeholder="Dein Minecraft Username">
    <button id="btn-connect" onclick="connect()">Verbinden</button>
    <div id="status-text" style="margin-top:20px;">Bereit...</div>
    <div class="log-area" id="log"></div>
</div>
<script>
    var socket = io();
    function log(msg) { var d = document.getElementById('log'); d.innerHTML += "<div>> " + msg + "</div>"; d.scrollTop = d.scrollHeight; }
    
    socket.on('server_message', function(data) {
        log(data.msg);
        if(data.success) {
            document.getElementById('status-text').innerText = "✅ Eingeloggt!";
            document.getElementById('status-text').style.color = "#4CAF50";
            document.getElementById('btn-connect').disabled = true;
        }
    });

    function connect() {
        var username = document.getElementById('username').value;
        if(!username) { alert("Name fehlt!"); return; }
        document.getElementById('status-text').innerText = "Verbinde...";
        socket.emit('join_request', {username: username});
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    # Wir benutzen render_template_string statt render_template
    return render_template_string(HTML_PAGE)

@socketio.on('join_request')
def handle_join(data):
    username = data.get('username')
    print(f"Login: {username}")
    emit('server_message', {'msg': f'Hallo {username}, Verbindung wird aufgebaut...', 'success': False})
    socketio.sleep(1)
    emit('server_message', {'msg': 'Verbindung zum Voice-Server erfolgreich!', 'success': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
