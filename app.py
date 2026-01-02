import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- DAS ULTIMATIVE DESIGN ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lospash Voice</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --accent: #00ffa3;
            --bg: #0b0e14;
            --card: rgba(23, 27, 34, 0.7);
            --border: rgba(255, 255, 255, 0.1);
        }

        body {
            background-color: var(--bg);
            /* Cooler animierter Hintergrund */
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(0, 255, 163, 0.08), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(118, 75, 255, 0.08), transparent 25%);
            color: white;
            font-family: 'Outfit', sans-serif;
            margin: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        /* Die Karte mit Glas-Effekt */
        .card {
            background: var(--card);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            padding: 40px;
            border-radius: 24px;
            width: 90%;
            max-width: 400px;
            text-align: center;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            animation: floatUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
        }

        /* Server Badge */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 255, 163, 0.1);
            color: var(--accent);
            padding: 6px 16px;
            border-radius: 100px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 25px;
            border: 1px solid rgba(0, 255, 163, 0.2);
        }
        .dot { width: 8px; height: 8px; background: var(--accent); border-radius: 50%; box-shadow: 0 0 10px var(--accent); animation: pulse 2s infinite;}

        h1 { margin: 0 0 5px 0; font-size: 28px; background: linear-gradient(to right, #fff, #bbb); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
        p { color: #8892b0; font-size: 14px; margin-bottom: 30px; }

        /* Profil Bereich */
        .profile {
            display: flex;
            align-items: center;
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 16px;
            border: 1px solid var(--border);
            margin-bottom: 25px;
            text-align: left;
            gap: 15px;
        }
        .avatar {
            width: 48px;
            height: 48px;
            border-radius: 10px;
            background: #222;
        }
        .user-info h3 { margin: 0; font-size: 16px; color: #fff; }
        .user-info span { font-size: 12px; color: var(--accent); }

        /* Button */
        .btn {
            width: 100%;
            padding: 18px;
            border: none;
            border-radius: 14px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            background: linear-gradient(135deg, #00ffa3 0%, #00d186 100%);
            color: #003320;
            box-shadow: 0 10px 30px rgba(0, 255, 163, 0.2);
            position: relative;
            overflow: hidden;
        }
        .btn:hover { transform: translateY(-3px); box-shadow: 0 15px 40px rgba(0, 255, 163, 0.3); }
        .btn:active { transform: scale(0.98); }

        /* Animationen */
        @keyframes floatUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }

    </style>
</head>
<body>

<div class="card">
    <div class="badge"><div class="dot"></div>Lospash Voice</div>
    
    <h1>Willkommen</h1>
    <p>Verbinde dein Audio für das beste Erlebnis.</p>

    <div class="profile" id="profile-box" style="display:none;">
        <img id="head-img" src="" class="avatar">
        <div class="user-info">
            <h3 id="username-display">Lade...</h3>
            <span>Verifiziert ✅</span>
        </div>
    </div>

    <div class="profile" id="guest-box">
        <div class="avatar" style="background: #333; display:flex; align-items:center; justify-content:center;">?</div>
        <div class="user-info">
            <h3>Gast Spieler</h3>
            <span style="color:#888;">Name nicht erkannt</span>
        </div>
    </div>

    <button class="btn" onclick="connect()" id="btn">
        🔊 Jetzt Beitreten
    </button>
</div>

<script>
    // URL Parameter holen
    const params = new URLSearchParams(window.location.search);
    
    // Wir suchen nach dem Parameter 'ign' (In-Game Name), den wir gleich im Plugin einstellen
    const ign = params.get('ign') || params.get('name'); 

    if (ign) {
        // Name gefunden -> UI Update
        document.getElementById('guest-box').style.display = 'none';
        document.getElementById('profile-box').style.display = 'flex';
        
        // Name setzen
        document.getElementById('username-display').innerText = ign;
        
        // Kopf von Crafatar laden
        document.getElementById('head-img').src = "https://crafatar.com/avatars/" + ign + "?overlay";
    }

    function connect() {
        const btn = document.getElementById('btn');
        btn.innerHTML = "Verbinde...";
        btn.style.opacity = "0.7";
        
        // Weiterleitung zur echten Engine
        // Wir nehmen alle Parameter mit, damit der Token erhalten bleibt
        setTimeout(() => {
            window.location.href = "https://client.openaudiomc.net/" + window.location.search;
        }, 500);
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
