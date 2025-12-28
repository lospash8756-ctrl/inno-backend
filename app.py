from flask import Flask, request
import requests

app = Flask(__name__)

CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

@app.route('/')
def home():
    return "<h1>INNO PRO 24/7</h1><p>Status: Aktiv</p>"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Fehler: Kein Code", 400
    
    try:
        # Token abrufen
        r = requests.post("https://discord.com/api/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        })
        token = r.json().get("access_token")
        
        # User Infos holen
        u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
        username = u.get('username', 'Unbekannt')
        
        # Webhook senden
        requests.post(WEBHOOK_URL, json={"content": f"✅ Login: **{username}**"})
        
        return "<h1>Erfolg!</h1><p>Du kannst die App jetzt nutzen.</p>"
    except Exception as e:
        return f"Fehler: {str(e)}", 500
