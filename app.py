import os
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
from mcstatus import JavaServer

# --- SERVER DATEN ---
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- HTML DESIGN ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lospash Voice</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { background: #050505; color: white; font-family: 'Inter', sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; overflow: hidden; }
        .bg { position: absolute; width: 200%; height: 200%; background: radial-gradient(circle, rgba(0, 255, 157, 0.1), transparent 40%); animation: m 20s linear infinite; z-index: -1; }
        @keyframes m { 0% {transform:translate(0,0)} 100% {transform:translate(-10%,-10%)} }
        .card { background: rgba(20,20,20,0.9); border: 1px solid #333; padding: 40px; border-radius: 20px; text-align: center; width: 90%; max-width: 380px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        h1 { font-family: 'Rajdhani'; font-size: 32px; margin: 0; color: #fff; }
        .badge { background: #111; padding: 5px 10px; border-radius: 20px; font-size: 12px; display: inline-block; margin-bottom: 20px; border: 1px solid #333; }
        .online { color: #00ff9d; } .offline { color: #ff4444; }
        .avatar { width: 60px; height: 60px; border-radius: 12px; margin: 15px auto; display: block; background: #222; }
        .btn { width: 100%; padding: 15px; background: #00ff9d; color: #000; border: none; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; margin-top: 20px; text-transform: uppercase; }
        .btn:disabled { background: #333; color: #666; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="bg"></div>
    <div class="card">
        <div class="badge" id="status">Verbinde...</div>
        <h1>Lospash Voice</h1>
        
        <img id="head" src="" class="avatar" style="display:none">
        <div id="username" style="font-weight:bold; font-size:18px;">Gast</div>
        
        <button id="btn" class="btn" onclick="go()" disabled>Lade...</button>
    </div>

    <script>
        const socket = io();
        // Name kommt aus der URL (/login/Name)
        const ign = "{{ username if username else '' }}"; 

        if(ign) {
            document.getElementById('username').innerText = ign;
            document.getElementById('head').src = "https://crafatar.com/avatars/" + ign + "?overlay";
            document.getElementById('head').style.display = "block";
        }

        socket.emit('check_server');
        socket.on('status_update', (data) => {
            const el = document.getElementById('status');
            if(data.online) {
                el.innerHTML = "● Online (" + data.players + ")";
                el.className = "badge online";
                if(ign) checkUser(ign);
                else {
                    document.getElementById('btn').innerText = "Kein Name erkannt";
                }
            } else {
                el.innerHTML = "● Offline";
                el.className = "badge offline";
                document.getElementById('btn').innerText = "Server Offline";
            }
        });

        function checkUser(name) {
            socket.emit('verify_user', {username: name});
        }

        socket.on('login_response', (data) => {
            const btn = document.getElementById('btn');
            if(data.success) {
                btn.disabled = false;
                btn.innerText = "JETZT VERBINDEN";
            } else {
                btn.innerText = "Nicht auf Server";
            }
        });

        function go() {
            // Weiterleitung
            window.location.href = "https://client.openaudiomc.net/" + window.location.search;
        }
    </script>
</body>
</html>
"""

@app.route('/')
@app.route('/login/<username>')
def index(username=None):
    return render_template_string(HTML_PAGE, username=username)

@socketio.on('check_server')
def handle_check():
    try:
        s = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        st = s.status()
        emit('status_update', {'online': True, 'players': st.players.online})
    except:
        emit('status_update', {'online': False, 'players': 0})

@socketio.on('verify_user')
def handle_verification(data):
    u = data.get('username')
    try:
        s = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        q = s.query()
        if u in q.players.names:
            emit('login_response', {'success': True})
        else:
            emit('login_response', {'success': False})
    except:
        emit('login_response', {'success': True}) # Fallback

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
