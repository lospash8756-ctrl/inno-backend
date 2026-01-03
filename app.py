import os
from flask import Flask, render_template_string, jsonify, request

# --- SERVER KONFIGURATION ---
MC_HOST = "MinecraftLospashW.aternos.me"
MC_PORT = 42486 

app = Flask(__name__)

# --- HTML DESIGN (Modern & GUI Look) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lospash Audio</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body { background: #0a0a0f; color: white; font-family: 'Inter', sans-serif; height: 100vh; display: flex; align-items: center; justify-content: center; margin: 0; overflow: hidden; }
        
        /* Hintergrund Effekt */
        .bg { position: absolute; width: 200%; height: 200%; background: radial-gradient(circle at 50% 50%, rgba(0, 255, 136, 0.05), transparent 50%); animation: pulse 10s infinite; z-index: -1; }
        @keyframes pulse { 0% {opacity:0.5;} 50% {opacity:1;} 100% {opacity:0.5;} }
        
        /* GUI Karte */
        .gui-card { 
            background: rgba(20, 25, 30, 0.95); 
            border: 1px solid rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 16px; 
            width: 90%; 
            max-width: 360px; 
            text-align: center;
            box-shadow: 0 0 40px rgba(0,0,0,0.5);
            position: relative;
        }
        
        /* Dekorations-Linie oben */
        .gui-line { position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, #00ff88, transparent); }

        h1 { font-family: 'Rajdhani'; font-size: 28px; margin: 0 0 5px 0; letter-spacing: 1px; color: #fff; }
        .sub { color: #666; font-size: 13px; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 2px; }

        /* Status Badge */
        .badge { background: #151a20; border: 1px solid #333; padding: 5px 12px; border-radius: 50px; font-size: 11px; display: inline-flex; align-items: center; gap: 6px; margin-bottom: 20px; }
        .dot { width: 6px; height: 6px; border-radius: 50%; background: #444; }
        .online .dot { background: #00ff88; box-shadow: 0 0 8px #00ff88; }
        
        /* Avatar & User */
        .avatar { width: 70px; height: 70px; border-radius: 12px; background: #222; margin: 0 auto 10px auto; border: 2px solid #333; transition: 0.3s; }
        .username { font-size: 18px; font-weight: 700; color: #fff; }
        .status-text { font-size: 12px; color: #555; margin-bottom: 25px; }
        .verified { color: #00ff88; }

        /* Button */
        .btn { width: 100%; padding: 15px; background: #2a3038; color: #777; border: none; border-radius: 8px; font-weight: 700; font-size: 14px; text-transform: uppercase; cursor: not-allowed; transition: 0.3s; letter-spacing: 1px; }
        .btn-active { background: #00ff88; color: #000; cursor: pointer; box-shadow: 0 5px 20px rgba(0, 255, 136, 0.2); }
        .btn-active:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0, 255, 136, 0.3); }

    </style>
</head>
<body>
    <div class="bg"></div>
    <div class="gui-card">
        <div class="gui-line"></div>
        
        <div class="badge" id="server-badge">
            <div class="dot"></div><span id="server-text">System wird geladen...</span>
        </div>

        <h1>LOSPASH</h1>
        <div class="sub">Secure Audio Interface</div>

        <img id="head" src="" class="avatar" style="display:none">
        <div id="username" class="username">Gast</div>
        <div id="user-status" class="status-text">Initialisiere...</div>

        <button id="btn" class="btn" onclick="go()" disabled>Lade...</button>
    </div>

    <script>
        const params = new URLSearchParams(window.location.search);
        // Holt Namen (unterstützt Plugin Parameter UND Pfad)
        let ign = params.get('name') || "{{ username }}"; 

        // Fix für Bedrock Avatare (Punkt entfernen für das Bild)
        let imgName = ign;
        if(ign && ign.startsWith('.') && ign !== "None") {
            imgName = ign.substring(1);
        }

        if(ign && ign !== "None") {
            document.getElementById('username').innerText = ign;
            document.getElementById('head').src = "https://crafatar.com/avatars/" + imgName + "?overlay";
            document.getElementById('head').style.display = "block";
        } else {
             document.getElementById('user-status').innerText = "Warte auf Link...";
        }

        // 1. Server Prüfung
        async function init() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                
                const badge = document.getElementById('server-badge');
                if(data.online) {
                    badge.classList.add('online');
                    document.getElementById('server-text').innerText = "ONLINE (" + data.players + ")";
                    
                    if(ign && ign !== "None") verify(ign);
                    else {
                        document.getElementById('btn').innerText = "Kein Spielername";
                        document.getElementById('user-status').innerText = "Nutze /audio im Spiel";
                    }
                } else {
                    document.getElementById('server-text').innerText = "OFFLINE";
                    document.getElementById('btn').innerText = "Server Offline";
                    document.getElementById('user-status').innerText = "Bitte Server starten";
                }
            } catch(e) { console.log(e); }
        }

        // 2. User Prüfung (Mit Bedrock Support)
        async function verify(name) {
            document.getElementById('user-status').innerText = "Prüfe Berechtigung...";
            try {
                // encodeURIComponent wichtig für Sonderzeichen/Punkte
                const res = await fetch('/api/verify/' + encodeURIComponent(name));
                const data = await res.json();
                
                if(data.verified) {
                    document.getElementById('user-status').innerHTML = "Verifiziert <span class='verified'>✔</span>";
                    enableBtn();
                } else {
                    document.getElementById('user-status').innerText = "Spieler nicht gefunden";
                    document.getElementById('btn').innerText = "Nicht Online";
                }
            } catch(e) {
                // Fallback bei Fehler -> Reinlassen
                enableBtn();
            }
        }

        function enableBtn() {
            const btn = document.getElementById('btn');
            btn.disabled = false;
            btn.classList.add('btn-active');
            btn.innerText = "STARTEN";
        }

        function go() {
            // Weiterleitung zum Audio Client
            window.location.href = "https://client.openaudiomc.net/" + window.location.search;
        }

        init();
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
        # Timeout verhindert langes Laden
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
        p_list = query.players.names
        
        # Bedrock Check Logik
        # 1. Ist "Name" da?
        if username in p_list: return jsonify({'verified': True})
        # 2. Ist ".Name" da? (Wenn Anfrage ohne Punkt kam)
        if ("." + username) in p_list: return jsonify({'verified': True})
        # 3. Ist "Name" da? (Wenn Anfrage mit Punkt kam)
        if username.startswith('.') and username[1:] in p_list: return jsonify({'verified': True})

        return jsonify({'verified': False})
    except:
        # Bei Fehler (Query disabled etc.) -> Immer True
        return jsonify({'verified': True})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
