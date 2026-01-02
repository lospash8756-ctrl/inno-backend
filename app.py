import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- ULTIMATE GAMING DESIGN ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lospash Voice</title>
    <link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #00ff9d;
            --secondary: #00b8ff;
            --bg: #050505;
            --glass: rgba(20, 20, 20, 0.7);
            --border: rgba(255, 255, 255, 0.08);
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
            perspective: 1000px;
        }

        /* Bewegter Hintergrund */
        .background {
            position: absolute;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 50% 50%, rgba(0, 255, 157, 0.05), transparent 40%),
                        radial-gradient(circle at 20% 80%, rgba(0, 184, 255, 0.05), transparent 40%);
            animation: moveBg 20s linear infinite;
            z-index: -2;
        }

        /* Schwebende Partikel (CSS Only) */
        .particles span {
            position: absolute;
            width: 4px; height: 4px;
            background: var(--primary);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--primary);
            animation: floatParticle 10s linear infinite;
            opacity: 0;
            z-index: -1;
        }
        .particles span:nth-child(1) { top: 20%; left: 20%; animation-duration: 8s; }
        .particles span:nth-child(2) { top: 80%; left: 80%; animation-duration: 12s; animation-delay: 1s; }
        .particles span:nth-child(3) { top: 40%; left: 60%; animation-duration: 15s; animation-delay: 2s; }

        /* Die Hauptkarte */
        .card {
            background: var(--glass);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid var(--border);
            padding: 50px 40px;
            border-radius: 30px;
            width: 90%;
            max-width: 420px;
            text-align: center;
            box-shadow: 0 30px 80px rgba(0,0,0,0.8), inset 0 0 0 1px rgba(255,255,255,0.05);
            transform-style: preserve-3d;
            transition: transform 0.1s ease;
            position: relative;
            overflow: hidden;
        }

        /* Neon Linie oben */
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary), transparent);
        }

        h1 {
            font-family: 'Rajdhani', sans-serif;
            font-size: 38px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 0;
            background: linear-gradient(to bottom, #fff, #aaa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        p { color: #888; font-size: 14px; margin-top: 5px; margin-bottom: 35px; }

        /* Avatar Box */
        .avatar-container {
            width: 100px;
            height: 100px;
            margin: 0 auto 20px auto;
            position: relative;
        }
        .avatar {
            width: 100%;
            height: 100%;
            border-radius: 20px;
            border: 2px solid rgba(255,255,255,0.1);
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            transition: transform 0.3s;
        }
        .status-dot {
            position: absolute;
            bottom: -5px; right: -5px;
            width: 20px; height: 20px;
            background: var(--primary);
            border: 4px solid #1a1a1a;
            border-radius: 50%;
            box-shadow: 0 0 15px var(--primary);
        }

        .username {
            font-size: 20px;
            font-weight: 600;
            color: white;
            margin-bottom: 5px;
            display: block;
        }
        .verified {
            color: var(--primary);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
            background: rgba(0, 255, 157, 0.1);
            padding: 4px 10px;
            border-radius: 10px;
        }

        /* Button */
        .btn {
            margin-top: 30px;
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, var(--primary) 0%, #00d482 100%);
            border: none;
            border-radius: 16px;
            color: #000;
            font-family: 'Rajdhani', sans-serif;
            font-size: 18px;
            font-weight: 700;
            text-transform: uppercase;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(0, 255, 157, 0.2);
            transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        .btn:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 20px 50px rgba(0, 255, 157, 0.4);
        }
        .btn:active { transform: scale(0.98); }
        
        .btn::after {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: 0.5s;
        }
        .btn:hover::after { left: 100%; }

        /* Animationen */
        @keyframes moveBg { 0% { transform: translate(0,0); } 100% { transform: translate(-10%, -10%); } }
        @keyframes floatParticle { 
            0% { transform: translateY(100vh) scale(0); opacity: 0; } 
            50% { opacity: 1; }
            100% { transform: translateY(-20vh) scale(1); opacity: 0; } 
        }

    </style>
</head>
<body>

<div class="background"></div>
<div class="particles">
    <span></span><span></span><span></span>
</div>

<div class="card" id="card">
    <h1>Lospash</h1>
    <p>Voice Chat Gateway</p>

    <div id="user-area" style="display:none;">
        <div class="avatar-container">
            <img id="head-img" src="" class="avatar">
            <div class="status-dot"></div>
        </div>
        <span class="username" id="ign-display">Spieler</span>
        <span class="verified">VERIFIZIERT</span>
    </div>

    <div id="guest-area">
        <div class="avatar-container">
            <div class="avatar" style="background:#222; display:flex; align-items:center; justify-content:center; color:#555; font-size:30px;">?</div>
        </div>
        <span class="username">Warte auf Verbindung...</span>
    </div>

    <button class="btn" onclick="connect()" id="btn">
        Verbindung Starten
    </button>
</div>

<script>
    const params = new URLSearchParams(window.location.search);
    const ign = params.get('ign') || params.get('name');
    const card = document.getElementById('card');

    // 3D Tilt Effekt für PC
    document.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth / 2 - e.pageX) / 25;
        const y = (window.innerHeight / 2 - e.pageY) / 25;
        card.style.transform = `rotateY(${x}deg) rotateX(${y}deg)`;
    });

    // User Daten laden
    if (ign) {
        document.getElementById('guest-area').style.display = 'none';
        document.getElementById('user-area').style.display = 'block';
        document.getElementById('ign-display').innerText = ign;
        document.getElementById('head-img').src = "https://crafatar.com/avatars/" + ign + "?overlay";
    }

    function connect() {
        const btn = document.getElementById('btn');
        btn.innerHTML = "LADE AUDIO ENGINE...";
        btn.style.background = "#fff";
        btn.style.color = "#000";
        
        setTimeout(() => {
            // Weiterleitung zur echten Engine
            window.location.href = "https://client.openaudiomc.net/" + window.location.search;
        }, 800);
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
