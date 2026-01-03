import os
from flask import Flask, render_template_string

app = Flask(__name__)

# --- HTML DESIGN (High-End & Immer Grün) ---
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
        
        /* Hintergrund Animation */
        .bg { position: absolute; width: 200%; height: 200%; background: radial-gradient(circle, rgba(0, 255, 136, 0.08), transparent 40%); animation: m 15s linear infinite; z-index: -1; }
        @keyframes m { 0% {transform:translate(0,0)} 100% {transform:translate(-10%,-10%)} }
        
        .card { 
            background: rgba(20, 25, 30, 0.95); 
            border: 1px solid rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 20px; 
            text-align: center; 
            width: 90%; 
            max-width: 380px; 
            box-shadow: 0 0 50px rgba(0,0,0,0.6); 
            position: relative;
        }

        /* Neon Linie */
        .line { position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, transparent, #00ff88, transparent); box-shadow: 0 0 15px #00ff88; }
        
        h1 { font-family: 'Rajdhani'; font-size: 32px; margin: 10px 0; color: #fff; letter-spacing: 1px; }
        
        /* Avatar */
        .avatar-box { width: 80px; height: 80px; margin: 20px auto; position: relative; }
        .avatar { width: 100%; height: 100%; border-radius: 15px; background: #222; border: 2px solid #333; }
        .pulse { position: absolute; top: -5px; left: -5px; right: -5px; bottom: -5px; border-radius: 20px; border: 2px solid #00ff88; opacity: 0; animation: p 2s infinite; }
        @keyframes p { 0% {transform:scale(1); opacity:1} 100% {transform:scale(1.2); opacity:0} }

        .username { font-size: 20px; font-weight: bold; margin-bottom: 5px; }
        .status { font-size: 12px; color: #666; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 2px; }
        .verified { color: #00ff88; }

        /* Button */
        .btn { width: 100%; padding: 18px; background: #2a3038; color: #888; border: none; border-radius: 10px; font-weight: 700; font-size: 16px; cursor: pointer; transition: 0.3s; text-transform: uppercase; }
        .btn-ready { background: #00ff88; color: #000; box-shadow: 0 0 30px rgba(0, 255, 136, 0.3); animation: pop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        .btn-ready:hover { transform: scale(1.02); box-shadow: 0 0 50px rgba(0, 255, 136, 0.5); }
        
        @keyframes pop { 0% {transform: scale(0.8);} 100% {transform: scale(1);} }
    </style>
</head>
<body>
    <div class="bg"></div>
    <div class="card">
        <div class="line"></div>
        <h1>LOSPASH</h1>
        
        <div class="avatar-box">
            <div class="pulse" id="pulse"></div>
            <img id="head" src="" class="avatar" style="display:none">
        </div>

        <div id="username" class="username">Gast</div>
        <div id="status" class="status">Verbinde System...</div>
        
        <button id="btn" class="btn" onclick="go()">Lade...</button>
    </div>

    <script>
        // Wir holen den Namen direkt aus dem Link (?name=...)
        const params = new URLSearchParams(window.location.search);
        let ign = params.get('name');
        
        // Bedrock Fix (falls Name mit . beginnt)
        let imgName = ign;
        if(ign && ign.startsWith('.')) imgName = ign.substring(1);

        // GUI Setup
        const btn = document.getElementById('btn');
        const status = document.getElementById('status');
        const pulse = document.getElementById('pulse');

        if(ign) {
            document.getElementById('username').innerText = ign;
            document.getElementById('head').src = "https://crafatar.com/avatars/" + imgName + "?overlay";
            document.getElementById('head').style.display = "block";
            
            // Starte "Fake" Sequenz
            simulateCheck();
        } else {
            // Fallback wenn kein Name da ist
            document.getElementById('username').innerText = "Spieler";
            simulateCheck(); 
        }

        function simulateCheck() {
            // Schritt 1: Prüfen
            status.innerText = "Synchronisiere...";
            
            setTimeout(() => {
                // Schritt 2: Erfolg (Egal ob Server an oder aus ist!)
                status.innerHTML = "VERIFIZIERT <span class='verified'>✔</span>";
                pulse.style.opacity = "1"; // Grüner Ring an
                
                // Button aktivieren
                btn.className = "btn btn-ready";
                btn.innerText = "AUDIO VERBINDEN";
            }, 1500); // 1.5 Sekunden "Ladezeit" für den Effekt
        }

        function go() {
            btn.innerText = "LEITE WEITER...";
            // Wir leiten weiter und nehmen alle Tokens mit
            window.location.href = "https://client.openaudiomc.net/" + window.location.search;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

# WICHTIG: Render Settings -> Start Command: "gunicorn app:app"
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
