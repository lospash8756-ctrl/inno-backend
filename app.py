from flask import Flask, request
import requests
import sys

app = Flask(__name__)

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

@app.route('/')
def home():
    return "<h1>Inno.Download Backend ist LIVE</h1>"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Kein Code von Discord erhalten.", 400

    try:
        # 1. Token bei Discord abfragen
        token_data = {
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        }
        r = requests.post("https://discord.com/api/oauth2/token", data=token_data)
        r.raise_for_status()
        token = r.json().get("access_token")

        # 2. Nutzerdaten abrufen
        headers = {'Authorization': f'Bearer {token}'}
        user = requests.get("https://discord.com/api/users/@me", headers=headers).json()
        
        # 3. Webhook senden (Sicher verpackt)
        webhook_payload = {
            "content": f"✅ **Login erfolgreich!**\n**User:** {user.get('username')} (ID: {user.get('id')})"
        }
        requests.post(WEBHOOK_URL, json=webhook_payload)

        return "<h1>Verifizierung erfolgreich!</h1><p>Du kannst die App jetzt nutzen.</p>"

    except Exception as e:
        # Zeigt den Fehler direkt im Browser an, falls es kracht
        return f"Fehler im Callback: {str(e)}", 500

if __name__ == "__main__":
    app.run()
