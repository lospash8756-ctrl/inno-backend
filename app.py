from flask import Flask, request, render_template_string, session
import requests

app = Flask(__name__)
app.secret_key = "INNO_SECRET_KEY_99" # Erforderlich für das Dashboard-System

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

# --- DESIGN & LAYOUT ---
STYLE = """
<style>
    :root { --primary: #5865F2; --accent: #00d2ff; --bg: #050608; --card: rgba(255,255,255,0.05); }
    body { background: var(--bg); color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; }
    nav { background: rgba(0,0,0,0.8); padding: 15px 5%; display: flex; justify-content: space-between; border-bottom: 2px solid var(--primary); backdrop-filter: blur(10px); sticky: top; }
    nav a { color: #fff; text-decoration: none; margin-left: 20px; font-weight: 600; font-size: 14px; transition: 0.3s; }
    nav a:hover { color: var(--accent); }
    .container { padding: 60px 10%; display: flex; flex-direction: column; align-items: center; }
    .glass-card { background: var(--card); border: 1px solid rgba(255,255,255,0.1); padding: 40px; border-radius: 20px; backdrop-filter: blur(15px); width: 100%; max-width: 900px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
    h1 { font-size: 40px; color: #fff; margin-bottom: 20px; letter-spacing: 2px; }
    .btn { background: var(--primary); color: #fff; padding: 12px 30px; border-radius: 8px; text-decoration: none; font-weight: bold; display: inline-block; transition: 0.3s; border: none; cursor: pointer; }
    .btn:hover { transform: scale(1.05); box-shadow: 0 0 20px var(--primary); }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; width: 100%; margin-top: 30px; }
    .feature-item { background: rgba(255,255,255,0.02); padding: 20px; border-radius: 10px; border-left: 4px solid var(--primary); }
    .avatar { width: 80px; height: 80px; border-radius: 50%; border: 2px solid var(--primary); margin-bottom: 15px; }
</style>
"""

NAV = f"""
<nav>
    <div style="font-weight: 900; color: var(--primary);">INNO PRO</div>
    <div>
        <a href="/">HOME</a>
        <a href="/tos">TOS</a>
        <a href="https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email">LOGIN</a>
    </div>
</nav>
"""

@app.route('/')
def home():
    content = """
    <div class="glass-card">
        <h1>POWERED BY INNO</h1>
        <p>Dein zentraler Hub für Next-Gen Modding Tools. Melde dich an, um dein persönliches Dashboard freizuschalten.</p>
        <div class="grid">
            <div class="feature-item"><h3>Cloud Mods</h3><p>Verwalte deine Downloads online.</p></div>
            <div class="feature-item"><h3>Auto-Inject</h3><p>Mods direkt ins Spiel laden.</p></div>
            <div class="feature-item"><h3>High Speed</h3><p>Keine Limits beim Download.</p></div>
        </div>
        <br><br>
        <a href="https://discord.com/api/oauth2/authorize?client_id=1454916135790186537&redirect_uri=https://inno-backend-1.onrender.com/callback&response_type=code&scope=identify+guilds+email" class="btn">DISCORD LOGIN</a>
    </div>
    """
    return f"<html><head>{STYLE}</head><body>{NAV}<div class='container'>{content}</div></body></html>"

@app.route('/tos')
def tos():
    content = """
    <div class="glass-card">
        <h1>Terms of Service</h1>
        <p>1. Keine missbräuchliche Nutzung der Server-API.</p>
        <p>2. Automatisierte Scraper sind verboten.</p>
        <p>3. Nur ein Account pro Nutzer.</p>
        <a href="/" class="btn">ZURÜCK</a>
    </div>
    """
    return f"<html><head>{STYLE}</head><body>{NAV}<div class='container'>{content}</div></body></html>"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Auth Error", 400
    try:
        r = requests.post("https://discord.com/api/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        }).json()
        token = r.get("access_token")
        u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
        
        # Webhook Alert
        requests.post(WEBHOOK_URL, json={"content": f"🚀 **Dashboard Login:** {u.get('username')}"})

        avatar_url = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"

        content = f"""
        <div class="glass-card">
            <img src="{avatar_url}" class="avatar">
            <h1>Willkommen, {u.get('username')}!</h1>
            <p>Dein Account ist verifiziert. Hier sind deine Optionen:</p>
            <div class="grid">
                <div class="feature-item" style="border-color: #00ff88;">
                    <h3>Software Key</h3>
                    <p>Status: <span style="color: #00ff88;">AKTIV</span></p>
                    <code>INNO-PRO-8822-X</code>
                </div>
                <div class="feature-item">
                    <h3>Downloads</h3>
                    <p>PC-Tool Version 5.1 verfügbar.</p>
                    <a href="#" style="color: var(--accent);">JETZT LADEN</a>
                </div>
                <div class="feature-item">
                    <h3>User ID</h3>
                    <p>{u.get('id')}</p>
                </div>
            </div>
            <br>
            <a href="/" class="btn">LOGOUT</a>
        </div>
        """
        return f"<html><head>{STYLE}</head><body>{NAV}<div class='container'>{content}</div></body></html>"
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
