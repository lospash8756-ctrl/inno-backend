import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- DEIN GENAUES DESIGN (Bild 1 Nachbau) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bedrock Voice Web</title>
    <style>
        body { 
            background-color: #121212; 
            color: #ffffff; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            margin: 0; 
        }

        .card {
            background-color: #1f1f1f;
            padding: 30px;
            border-radius: 8px;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        h1 { 
            text-align: center; 
            font-size: 22px; 
            margin-bottom: 10px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            gap: 10px;
        }

        .status-line {
            text-align: center;
            color: #888;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .status-green { color: #4CAF50; font-weight: bold; }

        input {
            width: 100%;
            padding: 12px;
            background-color: #ebf5ff; /* Helles Blau wie im Bild */
            border: none;
            border-radius: 4px;
            font-size: 16px;
            color: #000;
            margin-bottom: 20px;
            box-sizing: border-box;
            outline: none;
        }

        .btn {
            width: 100%;
            padding: 15px;
            background-color: #555; /* Grau wie im Bild */
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
        }
        .btn:hover { background-color: #666; }
        .btn-green { background-color: #4CAF50; }
        .btn-green:hover { background-color: #45a049; }

        .console {
            margin-top: 20px;
            background-color: #161616;
            padding: 15px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 13px;
            color: #888;
            min-height: 50px;
        }
        .log-entry { margin-bottom: 5px; }
    </style>
</head>
<body>

<div class="card">
    <h1>🔊 Bedrock Voice Web</h1>
    <div class="status-line">Status: <span class="status-green">Online ✅</span></div>

    <div id="login-ui">
        <input type="text" id="username" placeholder="Dein Name" value="" readonly>
        <button class="btn" id="main-btn" onclick="startProcess()">Prüfe Server...</button>
    </div>

    <div class="console" id="console">
        <div class="log-entry">> Warte auf Eingabe...</div>
    </div>
</div>

<script>
    // Holt den Token und Namen aus der URL (die vom Plugin kommt)
    const params = new URLSearchParams(window.location.search);
    const userParam = params.get('user') || "Spieler"; 
    
    // Setzt den Namen ins Feld (falls vorhanden)
    document.getElementById('username').value = userParam;

    function log(text) {
        const consoleDiv = document.getElementById('console');
        consoleDiv.innerHTML += `<div class="log-entry">> ${text}</div>`;
    }

    function startProcess() {
        const btn = document.getElementById('main-btn');
        btn.disabled = true;
        btn.style.backgroundColor = "#333";
        
        log("Prüfe, ob " + document.getElementById('username').value + " online ist...");
        
        // Fake-Ladezeit für den Effekt
        setTimeout(() => {
            log("Verbindung hergestellt!");
            log("Authentifizierung erfolgreich.");
            
            // Jetzt ändern wir den Button zum "Start" Button
            btn.innerText = "🔊 Voice Chat Beitreten";
            btn.classList.add('btn-green');
            btn.disabled = false;
            
            // Wenn man JETZT klickt, geht es zum echten Audio
            btn.onclick = function() {
                log("Leite weiter zur Audio-Engine...");
                const currentParams = window.location.search;
                // Hier ist der Trick: Wir leiten erst jetzt weiter
                window.location.href = "https://client.openaudiomc.net/" + currentParams;
            };
        }, 1500);
    }

    // Automatischer Start wenn Parameter da sind (optional, wirkt flüssiger)
    if(params.has('token')) {
        document.getElementById('username').value = "Lospash User"; // Oder Name aus Token parsen wenn möglich
        // Wir warten kurz, damit der User deine Seite sieht
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
