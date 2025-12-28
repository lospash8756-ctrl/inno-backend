from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

# Gemeinsames Design (CSS)
STYLE = """
<style>
    :root { --primary: #5865F2; --bg: #090a0f; --card: #15171f; }
    body { background: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
    .nav { width: 100%; background: var(--card); padding: 20px; display: flex; justify-content: center; gap: 30px; border-bottom: 2px solid var(--primary); box-sizing: border-box; }
    .nav a { color: #888; text-decoration: none; font-weight: bold; transition: 0.3s; }
    .nav a:hover { color: var(--primary); }
    .content { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px; text-align: center; }
    .card { background: var(--card); padding: 40px; border-radius: 20px; border: 1px solid #333; max-width: 600px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .btn { background: var(--primary); color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold; display: inline-block; margin-top: 20px; transition: 0.3s; }
    .btn:hover { transform: scale(1.05); background: #4752C4; }
    h1 { color: var(--primary); font-family: 'Impact', sans-serif; font-size: 40px; }
    p { color: #ccc; line-height: 1.6; }
</style>
"""

NAV = f"""
<div class="nav">
    <a href="/">HOME</a>
    <a href="/tos">TOS</a>
    <a href="https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email">LOGIN</a>
</div>
"""

@app.route('/')
def home():
    return f"""
    <html><head>{STYLE}</head><body>{NAV}
        <div class="content">
            <div class="card">
                <h1>INNO PRO PORTAL</h1>
                <p>Willkommen beim offiziellen Web-Interface von INNO PRO. Verwalte deine Mods und verifiziere deinen Account für vollen Zugriff.</p>
                <a href="https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email" class="btn">JETZT ANMELDEN</a>
            </div>
        </div>
    </body></html>
    """

@app.route('/tos')
def tos():
    return f"""
    <html><head>{STYLE}</head><body>{NAV}
        <div class="content">
            <div class="card" style="text-align: left;">
                <h1>TERMS OF SERVICE</h1>
                <p>1. <b>Nutzung:</b> Das Tool darf nur für legale Modding-Zwecke verwendet werden.</p>
                <p>2. <b>Daten:</b> Wir speichern keine Passwörter. Nur deine Discord-ID wird zur Verifizierung genutzt.</p>
                <p>3. <b>Haftung:</b> Der Nutzer ist selbst für seine Downloads verantwortlich.</p>
                <a href="/" class="btn">ZURÜCK</a>
            </div>
        </div>
    </body></html>
    """

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Fehler: Kein Code", 400
    try:
        r = requests.post("https://discord.com/api/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        })
        token = r.json().get("access_token")
        user = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
        
        requests.post(WEBHOOK_URL, json={"content": f"✅ Web-Login: **{user.get('username')}**"})
        
        return f"""
        <html><head>{STYLE}</head><body>{NAV}
            <div class="content">
                <div class="card">
                    <h1 style="color: #00ff88;">ERFOLGREICH!</h1>
                    <p>Hallo <b>{user.get('username')}</b>, du bist nun verifiziert.</p>
                    <p>Du kannst dieses Fenster schließen und zur App zurückkehren.</p>
                    <a href="/" class="btn">ZUR STARTSEITE</a>
                </div>
            </div>
        </body></html>
        """
    except Exception as e:
        return f"Fehler: {str(e)}", 500

if __name__ == "__main__":
    app.run()
