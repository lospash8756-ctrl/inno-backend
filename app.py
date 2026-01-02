import os
from flask import Flask, render_template_string, jsonify

# --- DEINE SERVER DATEN ---
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486 

app = Flask(__name__)

# --- HTML DESIGN ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lospash Voice</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { background: #050505; color: white; font-family: 'Inter', sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; overflow: hidden; }
        .bg { position: absolute; width: 200%; height: 200%; background: radial-gradient(circle, rgba(0, 255, 157, 0.1), transparent 40%); animation: m 20s linear infinite; z-index: -1; }
        @keyframes m { 0% {transform:translate(0,0)} 100% {transform:translate(-10%,-10%)} }
        
        .card { background: rgba(20,20,20,0.9); border: 1px solid #333; padding: 40px; border-radius: 20px; text-align: center; width: 90%; max-width: 380px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); }
        h1 { font-family: 'Rajdhani'; font-size: 32px; margin: 0; color: #fff; text-shadow: 0 0 20px rgba(0,255,157,0.3); }
        p { color: #888; font-size: 14px; margin-bottom: 25px; }
        
        .badge { background: #111; padding: 6px 12px; border-radius: 20px; font-size: 12px; display: inline-block; margin-bottom: 20px; border: 1px solid #333; transition: 0.3s; }
        .online { color: #00ff9d; border-color: #00ff9d; } 
        .offline { color: #ff4444; border-color: #ff4444; }
        
        .avatar { width: 64px; height: 64px; border-radius: 12px; margin: 0 auto 15px auto; display: block; background: #222; border: 2px solid #333; }
        
        .btn { width: 100%; padding: 16px; background: #333; color: #666; border: none; border-radius: 12px; font-weight: bold; font-size: 16px; cursor: not-allowed; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; }
        .btn-active { background: #00ff9d; color: #000; cursor: pointer; box-shadow: 0 0 25px rgba(0, 255, 157, 0.4); }
        .btn-active:hover { transform: scale(1.02); }

        .log { font-size: 11px; color: #555; margin-top: 15px; font-family: monospace; }
        .verified { color: #00ff9d; font-weight: bold; }
    </style>
</head>
<body>
    <div class="bg"></div>
    <div class="card">
        <div class="badge" id="status">Lade Status...</div>
        <h1>Lospash Voice</h1>
        <p>Premium Audio Gateway</p>
        
        <img id="head" src="" class="avatar" style="display:none">
        <div id="username" style="font-weight:bold; font-size:18px; margin-bottom:5px;">Gast</div>
        <div id="user-check" style="font-size:12px; color:#666; margin-bottom:20px;">Warte auf Server...</div>
        
        <button id="btn" class="btn" onclick="go()" disabled>Lade...</button>
        <div class="log" id="log-msg">Initialisiere System...</div>
    </div>

    <script>
        const params = new URLSearchParams(window.location.search);
        const ign = params.get('name') || "{{ username }}"; 

        if(ign && ign !== "None") {
            document.getElementById('username').innerText = ign;
            document.getElementById('head').src = "https://crafatar.com/avatars/" + ign + "?overlay";
            document.getElementById('head').style.display = "block";
        }

        async function checkServer() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                const badge = document.getElementById('status');
                if(data.online) {
                    badge.innerText = "● Online (" + data.players + ")";
                    badge.classList.add('online');
                    document.getElementById('log-msg').innerText = "Server verbunden.";
                    
                    if(ign && ign !== "None") checkUser(ign);
                    else {
                        document.getElementById('btn').innerText = "Kein Name";
                        document.getElementById('user-check').innerText = "Bitte Link im Spiel nutzen";
                    }
                } else {
                    badge.innerText = "● Offline";
                    badge.classList.add('offline');
                    document.getElementById('btn').innerText = "Server Offline";
                    document.getElementById('log-msg').innerText = "Aternos Server starten!";
                }
            } catch (e) {
                console.error(e);
            }
        }

        async function checkUser(name) {
            document.getElementById('user-check').innerText = "Prüfe Spieler...";
            try {
                const response = await fetch('/api/verify/' + name);
                const data = await response.json();
                
                const btn = document.getElementById('btn');
                if(data.verified) {
                    document.getElementById('user-check').innerText = "Verifiziert ✓";
                    document.getElementById('user-check').classList.add('verified');
                    btn.disabled = false;
                    btn.classList.add('btn-active');
                    btn.innerText = "JETZT VERBINDEN";
                } else {
                    document.getElementById('user-check').innerText = "Nicht gefunden ❌";
                    btn.innerText = "Nicht Online";
                    document.getElementById('log-msg').innerText = "Du musst auf dem Server sein.";
                }
            } catch (e) {
                // Fallback bei Fehler: Reinlassen
                enableButton();
            }
        }

        function enableButton() {
            const btn = document.getElementById('btn');
            btn.disabled = false;
            btn.classList.add('btn-active');
            btn.innerText = "JETZT VERBINDEN";
        }

        function go() {
            window.location.href = "https://client.openaudiomc.net/" + window.location.search;
        }

        checkServer();
    </script>
</body>
</html>
"""

# --- ROUTEN ---
@app.route('/')
@app.route('/login/<username>')
def index(username=None):
    return render_template_string(HTML_PAGE, username=username)

@app.route('/api/status')
def api_status():
    from mcstatus import JavaServer
    try:
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        status = server.status()
        return jsonify({'online': True, 'players': status.players.online})
    except:
        return jsonify({'online': False})

@app.route('/api/verify/<username>')
def api_verify(username):
    from mcstatus import JavaServer
    try:
        server = JavaServer.lookup(f"{MC_HOST}:{MC_PORT}")
        query = server.query()
        if username in query.players.names:
            return jsonify({'verified': True})
        else:
            return jsonify({'verified': False})
    except:
        return jsonify({'verified': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
