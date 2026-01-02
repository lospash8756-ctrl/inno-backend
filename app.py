import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# --- DEIN DESIGN (HTML) ---
# Das sieht der Spieler kurz, bevor das Audio startet
HTML_REDIRECT = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lospash Audio</title>
    <style>
        body { 
            background-color: #121212; 
            color: white; 
            font-family: sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            margin: 0; 
        }
        .loader {
            border: 5px solid #333;
            border-top: 5px solid #4CAF50;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin-bottom: 20px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        h1 { color: #4CAF50; margin-bottom: 10px; }
        p { color: #888; }
    </style>
</head>
<body>
    <div class="loader"></div>
    <h1>Lospash Voice Chat</h1>
    <p>Verbinde mit Audio-Server...</p>

    <script>
        // Wir nehmen die Session-Daten aus deiner URL und leiten weiter
        // an den echten OpenAudioMc Server, damit das Mikrofon funktioniert.
        setTimeout(function() {
            // Die Parameter (Token) aus der URL holen
            const params = window.location.search;
            // Weiterleitung zur funktionierenden Audio-Engine
            window.location.href = "https://client.openaudiomc.net/" + params;
        }, 2000); // 2 Sekunden dein Logo zeigen, dann verbinden
    </script>
</body>
</html>
"""

# Die normale Startseite (falls man den Link ohne Token öffnet)
HTML_HOME = """
<!DOCTYPE html>
<html>
<body style="background:#121212; color:white; font-family:sans-serif; text-align:center; padding-top:50px;">
    <h1>Lospash Voice Server</h1>
    <p>Gehe in Minecraft und tippe <b>/audio</b> um dich zu verbinden.</p>
</body>
</html>
"""

@app.route('/')
def index():
    # Prüfen, ob der Link aus Minecraft kommt (hat er Login-Daten?)
    # OpenAudioMc nutzt meistens ?session=... oder ?token=...
    session = request.args.get('session')
    token = request.args.get('token')
    
    if session or token:
        # Ja, es ist ein Spieler aus dem Spiel -> Zeige Redirect Seite
        return render_template_string(HTML_REDIRECT)
    else:
        # Nein, normaler Besucher -> Zeige Info
        return render_template_string(HTML_HOME)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
