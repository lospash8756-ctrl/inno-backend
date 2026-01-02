import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- GEMEINSAMES DESIGN (CSS & BACKGROUND) ---
# Das nutzen wir für alle Seiten, damit es einheitlich aussieht.
SHARED_STYLE = """
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lospash Voice</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #00ff9d; --bg: #050505; --glass: rgba(20, 20, 20, 0.8); --text: #eee; }
        body {
            background-color: var(--bg); color: var(--text); font-family: 'Inter', sans-serif;
            margin: 0; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center;
            overflow-x: hidden;
        }
        /* Hintergrund Animation */
        .background {
            position: fixed; top: 0; left: 0; width: 200%; height: 200%; z-index: -2;
            background: radial-gradient(circle at 50% 50%, rgba(0, 255, 157, 0.05), transparent 40%);
            animation: moveBg 20s linear infinite;
        }
        @keyframes moveBg { 0% { transform: translate(0,0); } 100% { transform: translate(-10%, -10%); } }
        
        /* Die Karte */
        .card {
            background: var(--glass); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.08); padding: 40px; border-radius: 24px;
            width: 90%; max-width: 500px; text-align: center;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6); margin: 20px;
        }
        
        h1 { font-family: 'Rajdhani', sans-serif; font-size: 32px; margin: 0 0 10px 0; color: #fff; text-transform: uppercase; }
        h2 { color: var(--primary); font-size: 20px; margin-bottom: 20px; }
        p, li { color: #aaa; font-size: 14px; line-height: 1.6; text-align: left; }
        
        /* Footer Links */
        .footer { margin-top: 30px; font-size: 12px; color: #666; display: flex; gap: 15px; justify-content: center; }
        .footer a { color: #888; text-decoration: none; transition: 0.3s; }
        .footer a:hover { color: var(--primary); }

        /* Button & Avatar Styles aus vorherigem Design */
        .btn {
            width: 100%; padding: 18px; background: var(--primary); border: none; border-radius: 12px;
            color: #000; font-family: 'Rajdhani', sans-serif; font-size: 18px; font-weight: 700;
            text-transform: uppercase; cursor: pointer; margin-top: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.3); transition: 0.3s;
        }
        .btn:hover { transform: scale(1.02); box-shadow: 0 0 40px rgba(0, 255, 157, 0.5); }
        
        .avatar { width: 80px; height: 80px; border-radius: 15px; border: 2px solid rgba(255,255,255,0.1); margin-bottom: 10px; }
        .badge { background: rgba(0,255,157,0.1); color: var(--primary); padding: 4px 10px; border-radius: 5px; font-size: 11px; font-weight: bold; letter-spacing: 1px; }
    </style>
</head>
"""

# --- SEITE 1: HOME (LOGIN) ---
HTML_HOME = SHARED_STYLE + """
<body>
    <div class="background"></div>
    <div class="card">
        <h1>Lospash Voice</h1>
        <div style="margin-bottom:20px;">Secure Audio Gateway</div>

        <div id="user-area" style="display:none;">
            <img id="head-img" src="" class="avatar"><br>
            <div class="badge">VERIFIZIERT</div>
            <h3 id="ign-display" style="margin: 10px 0 0 0; color:white;">Spieler</h3>
        </div>

        <div id="guest-area">
            <div class="avatar" style="background:#222; display:flex; align-items:center; justify-content:center; margin:0 auto 10px auto;">?</div>
            <p style="text-align:center;">Warte auf Token...</p>
        </div>

        <button class="btn" onclick="connect()" id="btn">Verbindung Herstellen</button>
        
        <div style="margin-top: 20px; font-size: 12px; color: #555;">
            Durch Klicken akzeptierst du unsere <a href="/tos" style="color:#777;">Nutzungsbedingungen</a>.
        </div>
    </div>

    <div class="footer">
        <a href="/">Home</a>
        <a href="/tos">Nutzungsbedingungen (TOS)</a>
        <a href="/privacy">Datenschutz</a>
    </div>

    <script>
        const params = new URLSearchParams(window.location.search);
        const ign = params.get('ign') || params.get('name');

        if (ign) {
            document.getElementById('guest-area').style.display = 'none';
            document.getElementById('user-area').style.display = 'block';
            document.getElementById('ign-display').innerText = ign;
            document.getElementById('head-img').src = "https://crafatar.com/avatars/" + ign + "?overlay";
        }

        function connect() {
            const btn = document.getElementById('btn');
            btn.innerText = "LADE...";
            // Weiterleitung zur echten Engine mit allen Parametern
            setTimeout(() => {
                window.location.href = "https://client.openaudiomc.net/" + window.location.search;
            }, 500);
        }
    </script>
</body>
</html>
"""

# --- SEITE 2: TOS (NUTZUNGSBEDINGUNGEN) ---
HTML_TOS = SHARED_STYLE + """
<body>
    <div class="background"></div>
    <div class="card" style="text-align:left;">
        <h1>Rechtliches</h1>
        <h2>Nutzungsbedingungen (TOS)</h2>
        <div style="max-height: 300px; overflow-y: auto; padding-right: 10px;">
            <p><strong>1. Akzeptanz</strong><br>Durch die Nutzung von Lospash Voice stimmst du zu, dich respektvoll zu verhalten. Beleidigungen oder Missbrauch des Voice Chats führen zum Bann.</p>
            <p><strong>2. Nutzung</strong><br>Der Service wird "wie besehen" bereitgestellt. Wir garantieren keine 100%ige Verfügbarkeit.</p>
            <p><strong>3. Verhalten</strong><br>Kein Spam, keine Werbung, keine Belästigung anderer Spieler über Audio.</p>
            <p><strong>4. Aufnahmen</strong><br>Das Aufnehmen von Gesprächen ohne Einwilligung der Beteiligten ist untersagt.</p>
        </div>
        <a href="/" class="btn" style="display:block; text-align:center; text-decoration:none; margin-top:20px;">Zurück</a>
    </div>
    <div class="footer">
        <a href="/">Home</a>
        <a href="/tos" style="color:var(--primary);">TOS</a>
        <a href="/privacy">Datenschutz</a>
    </div>
</body>
</html>
"""

# --- SEITE 3: DATENSCHUTZ ---
HTML_PRIVACY = SHARED_STYLE + """
<body>
    <div class="background"></div>
    <div class="card" style="text-align:left;">
        <h1>Datenschutz</h1>
        <h2>Privacy Policy</h2>
        <div style="max-height: 300px; overflow-y: auto; padding-right: 10px;">
            <p><strong>1. Welche Daten?</strong><br>Wir verarbeiten deinen Minecraft-Namen und deine IP-Adresse temporär, um die Audio-Verbindung herzustellen.</p>
            <p><strong>2. Audio-Daten</strong><br>Der Voice-Chat läuft über Peer-to-Peer oder Relay-Server. Wir speichern KEINE Audio-Gespräche.</p>
            <p><strong>3. Cookies</strong><br>Diese Seite verwendet technische Cookies, um deine Sitzung aktiv zu halten.</p>
            <p><strong>4. Drittanbieter</strong><br>Die Audio-Technologie wird von OpenAudioMc bereitgestellt.</p>
        </div>
        <a href="/" class="btn" style="display:block; text-align:center; text-decoration:none; margin-top:20px;">Zurück</a>
    </div>
    <div class="footer">
        <a href="/">Home</a>
        <a href="/tos">TOS</a>
        <a href="/privacy" style="color:var(--primary);">Datenschutz</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_HOME)

@app.route('/tos')
def tos():
    return render_template_string(HTML_TOS)

@app.route('/privacy')
def privacy():
    return render_template_string(HTML_PRIVACY)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
