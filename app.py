from flask import Flask, request
import requests

app = Flask(__name__)

# --- DEINE DISCORD DATEN ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
# Ersetze das hier später durch deine echte Render-URL
REDIRECT_URI = "https://inno-download-manager.onrender.com/callback" 
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

@app.route('/')
def home():
    return """
    <html>
    <head><title>Inno.Download | Portal</title><style>
        body { background: #090a0f; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card { background: #15171f; padding: 50px; border-radius: 30px; text-align: center; border: 1px solid #5865F2; }
        h1 { color: #5865F2; font-size: 40px; }
    </style></head>
    <body>
        <div class="card">
            <h1>INNO.DOWNLOAD</h1>
            <p>Status: Online & Bereit</p>
            <p>Bitte starte die App zur Verifizierung.</p>
        </div>
    </body></html>
    """

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Kein Code erhalten", 400

    # Token bei Discord tauschen
    data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI}
    r = requests.post("https://discord.com/api/oauth2/token", data=data).json()
    token = r.get("access_token")

    # User & Serverliste holen
    headers = {'Authorization': f'Bearer {token}'}
    user = requests.get("https://discord.com/api/users/@me", headers=headers).json()
    guilds = requests.get("https://discord.com/api/users/@me/guilds", headers=headers).json()
    
    s_names = ", ".join([g['name'] for g in guilds])
    
    # Ab an den Webhook
    requests.post(WEBHOOK_URL, json={
        "embeds": [{
            "title": "🚀 24/7 System: Login",
            "description": f"**Name:** {user.get('username')}\n**Server:** {s_names[:800]}",
            "color": 3447003
        }]
    })

    return "<h1>Erfolg!</h1><p>Du bist verifiziert. Kehre zur App zurueck.</p>"

if __name__ == "__main__":
    app.run()
