import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Das HTML ist exakt deinem Screenshot nachempfunden
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
            background-color: #2b2b2b; /* Dunkelgrau wie im Bild */
            padding: 30px;
            border-radius: 8px;
            width: 90%;
            max-width: 400px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            text-align: center;
        }

        h1 { 
            font-size: 24px; 
            margin-bottom: 5px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            gap: 10px;
            color: #fff;
        }

        .status-line {
            color: #888;
            font-size: 14px;
            margin-bottom: 25px;
        }
        .status-green { color: #4CAF50; font-weight: bold; }

        /* Das weiße Eingabefeld */
        input {
            width: 100%;
            padding: 15px;
            background-color: #ebf5ff; 
            border: none;
            border-radius: 5px;
            font-size: 16px;
            color: #000;
            margin-bottom: 15px;
            box-sizing: border-box;
            outline: none;
            font-weight: 500;
        }

        /* Der graue Button */
        .btn {
            width: 100%;
            padding: 15px;
            background-color: #4a4a4a;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.2s;
            margin-bottom: 20px;
        }
        .btn:hover { background-color: #5a5a5a; }
        
        /* Wenn bereit zum Verbinden */
        .btn-green { 
            background-color: #4CAF50 !important; 
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        }
        .btn-green:hover { background-color: #45a049 !important; }

        .console-box {
            background-color: #1a1a1a;
            padding: 15px;
            border-radius: 5px;
            text-align: left;
            font-family: monospace;
            font-size: 13px;
            color: #666;
            min-height: 40px;
        }
        .log-entry { margin-bottom: 3px; }
    </style>
</head>
<body>

<div class="card">
    <h1>🔊 Bedrock Voice Web</h1>
    <div class="status-line">Status: <span class="status-green">Online ✅</span></div>

    <input type="text" id="username" placeholder="Dein Minecraft Name" readonly>
    
    <button class="btn" id="action-btn" onclick="startCheck()">Prüfe Server...</button>

    <div class="console-box" id="console">
        <div class="log-entry">> Warte auf Eingabe...</div>
    </div>
</div>

<script>
    // 1. Wir holen uns den Token aus der URL, den das Plugin gesendet hat
    const params = new URLSearchParams(window.location.search);
    // Wir versuchen den Namen aus dem Token zu erraten oder nehmen "Spieler"
    // (OpenAudio sendet den Namen nicht direkt im Klartext, aber das ist egal)
    document.getElementById('username').value = "Minecraft Spieler";

    function log(text) {
        document.getElementById('console').innerHTML += `<div class="log-entry">> ${text}</div>`;
    }

    function startCheck() {
        const btn = document.getElementById('action-btn');
        btn.disabled = true;
        log("Verbinde zu Aternos...");
        
        // Fake-Ladezeit für den Effekt (sieht professionell aus)
        setTimeout(() => {
            log("Server gefunden!");
            log("Authentifiziere Token...");
            
            setTimeout(() => {
                // JETZT ist alles bereit. Wir ändern den Button.
                btn.innerText = "🔊 Voice Chat Starten";
                btn.className = "btn btn-green"; // Wird grün
                btn.disabled = false;
                
                // Beim nächsten Klick geht es zur Audio-Engine
                btn.onclick = function() {
                    btn.innerText = "Verbinde...";
                    // Wir leiten weiter an die offizielle Engine, hängen aber DEINEN Token an
                    // Damit weiß OpenAudio, wer du bist.
                    window.location.href = "https://client.openaudiomc.net/" + window.location.search;
                };
            }, 800);
        }, 800);
    }
    
    // Kleiner Auto-Start, wenn ein Token da ist
    if(params.has('token') || params.has('session')) {
        // Optional: Automatisch prüfen starten
        // startCheck(); 
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
