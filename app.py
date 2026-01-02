import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- DAS NEUE, PROFESSIONELLE DESIGN ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lospash Voice</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #00ff88;
            --bg-dark: #0a0a0f;
            --card-bg: rgba(20, 20, 25, 0.95);
            --text-main: #ffffff;
            --text-muted: #8888aa;
        }

        * { box-sizing: border-box; }

        body { 
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 255, 136, 0.05) 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, rgba(0, 255, 136, 0.05) 0%, transparent 20%);
            color: var(--text-main); 
            font-family: 'Inter', sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh; 
            margin: 0; 
            overflow: hidden;
        }

        /* Schicker Container mit Glas-Effekt */
        .card {
            background: var(--card-bg);
            padding: 40px;
            border-radius: 24px;
            width: 85%;
            max-width: 380px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6);
            border: 1px solid rgba(255,255,255,0.08);
            text-align: center;
            backdrop-filter: blur(10px);
            transform: translateY(0);
            transition: transform 0.3s ease;
        }

        /* Logo / Titel */
        h1 { 
            font-size: 24px; 
            font-weight: 800; 
            margin: 0 0 5px 0; 
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #fff 0%, #aaa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            font-size: 13px;
            color: var(--text-muted);
            margin-bottom: 30px;
            font-weight: 500;
        }

        /* Status Badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 255, 136, 0.1);
            color: var(--primary);
            padding: 6px 14px;
            border-radius: 50px;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 25px;
            border: 1px solid rgba(0, 255, 136, 0.2);
        }
        .dot {
            width: 8px; 
            height: 8px; 
            background: var(--primary); 
            border-radius: 50%;
            box-shadow: 0 0 10px var(--primary);
            animation: pulse 2s infinite;
        }

        /* Eingabefeld */
        .input-group {
            position: relative;
            margin-bottom: 15px;
            text-align: left;
        }
        label {
            display: block;
            font-size: 11px;
            color: var(--text-muted);
            margin-bottom: 6px;
            margin-left: 4px;
            font-weight: 600;
            text-transform: uppercase;
        }
        input {
            width: 100%;
            padding: 16px;
            background-color: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            font-size: 15px;
            color: #fff;
            outline: none;
            transition: 0.3s;
            font-family: monospace;
        }
        input:focus {
            border-color: var(--primary);
            background-color: rgba(0, 255, 136, 0.05);
        }

        /* Der Haupt-Button */
        .btn {
            width: 100%;
            padding: 18px;
            background: #2a2a30;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-top: 10px;
            position: relative;
            overflow: hidden;
        }
        .btn:hover { background: #3a3a40; transform: translateY(-2px); }
        .btn:active { transform: scale(0.98); }

        /* Grüner Status für Button */
        .btn-success {
            background: var(--primary) !important;
            color: #000 !important;
            box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
        }
        .btn-success:hover {
            box-shadow: 0 15px 40px rgba(0, 255, 136, 0.4);
        }

        /* Konsole */
        .console {
            margin-top: 25px;
            padding: 15px;
            background: #000;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #666;
            text-align: left;
            min-height: 40px;
            border: 1px solid #222;
        }
        .log-line { margin-bottom: 4px; opacity: 0; animation: fadeIn 0.3s forwards; }
        .log-success { color: var(--primary); }

        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        @keyframes fadeIn { to { opacity: 1; } }

        /* Lade-Spinner im Button */
        .loader {
            display: none;
            width: 18px; height: 18px;
            border: 2px solid #fff;
            border-bottom-color: transparent;
            border-radius: 50%;
            display: inline-block;
            box-sizing: border-box;
            animation: rotation 1s linear infinite;
            vertical-align: middle;
            margin-right: 8px;
        }
        @keyframes rotation { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    </style>
</head>
<body>

<div class="card">
    <div class="status-badge">
        <div class="dot"></div>
        <span>System Online</span>
    </div>

    <h1>Lospash Voice</h1>
    <div class="subtitle">Secure Audio Gateway</div>

    <div class="input-group">
        <label>Spieler Name</label>
        <input type="text" id="username" value="Lade..." readonly>
    </div>

    <button class="btn" id="action-btn" onclick="startProcess()">
        <span id="btn-text">Verbindung prüfen</span>
    </button>

    <div class="console" id="console">
        <div class="log-line">> Bereit zur Authentifizierung...</div>
    </div>
</div>

<script>
    // URL Parameter auslesen
    const params = new URLSearchParams(window.location.search);
    const hasToken = params.has('token') || params.has('session');

    // Name "faken" für coolen Effekt (OpenAudio sendet den Namen nicht im Klartext)
    const fakeNames = ["Lospash User", "Bedrock Player", "Minecraft Gast"];
    document.getElementById('username').value = "Authentifiziere...";

    // Konsole Log Funktion
    function log(msg, type="") {
        const line = document.createElement('div');
        line.className = 'log-line ' + (type === 'success' ? 'log-success' : '');
        line.innerText = "> " + msg;
        document.getElementById('console').appendChild(line);
        document.getElementById('console').scrollTop = 999;
    }

    // Hauptfunktion
    function startProcess() {
        const btn = document.getElementById('action-btn');
        const btnText = document.getElementById('btn-text');
        
        // UI Sperren
        btn.disabled = true;
        btn.style.cursor = "wait";
        btnText.innerHTML = '<span class="loader"></span> Prüfe...';
        
        log("Starte Handshake mit Server...");

        // Fake Delay für "Hacker"-Feeling
        setTimeout(() => {
            document.getElementById('username').value = "Verifiziert ✅";
            log("Token akzeptiert.");
            log("Audio-Stream gefunden.");
            
            setTimeout(() => {
                log("Bereit zum Verbinden!", "success");
                
                // Button auf GRÜN schalten
                btn.className = "btn btn-success";
                btn.disabled = false;
                btn.style.cursor = "pointer";
                btnText.innerHTML = "🔊 Voice Chat Beitreten";
                
                // Click Event ändern
                btn.onclick = function() {
                    btnText.innerText = "Leite weiter...";
                    // Weiterleitung zur echten Audio-Engine
                    window.location.href = "https://client.openaudiomc.net/" + window.location.search;
                };
            }, 800);
        }, 1200);
    }

    // Auto-Start (optional, wirkt flüssiger)
    if(hasToken) {
        setTimeout(startProcess, 500);
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
