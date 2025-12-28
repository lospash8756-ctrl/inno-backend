from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import json
import logging

# Initialisierung des Flask-Kernsystems
app = Flask(__name__)
app.secret_key = "INNO_PRO_ENCRYPTED_SYSTEM_CORE_2025_ULTIMATE"

# --- SYSTEM-KONFIGURATION ---
# Die neue Client-ID von deinem Screenshot
CLIENT_ID = "1454914591661228345" 
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"

# AUTO-JOIN CONFIGURATION
GUILD_ID = "1322234057635037234" # Deine Server-ID
# HINWEIS: Du MUSST einen Bot-Token hier eintragen, damit Auto-Join klappt!
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER_EINSETZEN" 

# WEBHOOK-ENDPUNKTE
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# VOLLSTÄNDIGER OAUTH2 LINK MIT AUTO-JOIN PERMISSION
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- ADVANCED UI ENGINE (CYBER-GRID DESIGN) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');
    :root { --p: #5865F2; --s: #00d2ff; --bg: #010103; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.06); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }

    .glow-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
               background: radial-gradient(circle at 10% 10%, rgba(88,101,242,0.1), transparent),
                           radial-gradient(circle at 90% 90%, rgba(0,210,255,0.07), transparent); }

    nav { display: flex; justify-content: space-between; padding: 25px 8%; background: rgba(0,0,0,0.85); 
          backdrop-filter: blur(40px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 900; font-size: 26px; color: #fff; text-decoration: none; letter-spacing: 5px; }
    .logo span { color: var(--p); text-shadow: 0 0 15px var(--p); }

    .container { min-height: 90vh; display: flex; align-items: center; justify-content: center; padding: 100px 20px; }
    .terminal-card { background: var(--card); border: 1px solid var(--border); padding: 80px; border-radius: 60px; 
                     backdrop-filter: blur(80px); max-width: 1100px; width: 100%; text-align: center; 
                     box-shadow: 0 50px 120px rgba(0,0,0,0.95); transition: 0.5s ease; }
    
    h1 { font-size: clamp(40px, 7vw, 75px); font-weight: 900; letter-spacing: -3px; line-height: 0.95; margin-bottom: 30px; }
    .grad-text { background: linear-gradient(135deg, #fff 40%, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .btn { padding: 20px 50px; border-radius: 20px; text-decoration: none; font-weight: 900; font-size: 15px; 
           transition: 0.5s; display: inline-block; text-transform: uppercase; border: none; cursor: pointer; letter-spacing: 2px; }
    .btn-main { background: var(--p); color: #fff; box-shadow: 0 15px 40px rgba(88,101,242,0.4); }
    .btn-main:hover { transform: scale(1.05) translateY(-5px); box-shadow: 0 20px 50px rgba(88,101,242,0.6); }

    .avatar-frame { width: 140px; height: 140px; border-radius: 50%; border: 4px solid var(--p); margin: 0 auto 30px auto; 
                    box-shadow: 0 0 40px rgba(88,101,242,0.4); overflow: hidden; position: relative; }
    .avatar-frame img { width: 100%; height: 100%; object-fit: cover; }
    
    .loading-bar { width: 100%; height: 2px; background: rgba(255,255,255,0.05); margin: 20px 0; position: relative; }
    .loading-bar::after { content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 40%; background: var(--p); animation: load 2s infinite ease-in-out; }
    @keyframes load { 0% { left: 0; width: 0%; } 50% { left: 0; width: 100%; } 100% { left: 100%; width: 0%; } }

    .terminal-log { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #444; text-align: left; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin-top: 30px; line-height: 1.8; }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO<span>PRO</span></a>
        <div style="display:flex; gap:40px;">
            <a href="/" style="color:#666; text-decoration:none; font-weight:800; font-size:11px; letter-spacing:1px;">GRID_HOME</a>
            <a href="/tos" style="color:#666; text-decoration:none; font-weight:800; font-size:11px; letter-spacing:1px;">SECURITY_PROT</a>
            {"<a href='/dashboard' style='color:#fff; text-decoration:none; font-weight:800; font-size:11px; letter-spacing:1px;'>USER_TERMINAL</a>" if 'user' in session else ""}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"""
    <html><head><title>INNO PRO | Central Hub</title>{CSS}</head><body><div class='glow-bg'></div>{get_nav()}
    <div class='container'><div class='terminal-card'>
        <h1 class='grad-text'>CONNECTION<br>PENDING...</h1>
        <p style='color:#555; font-family:"JetBrains Mono"; font-size:14px; margin-bottom:40px;'>Inno.Download Mainframe v5.2 // Awaiting Secure Auth Sequence</p>
        <a href='{AUTH_URL}' class='btn btn-main'>Initialize Login</a>
    </div></div></body></html>
    """)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    
    return render_template_string(f"""
    <html><head><title>Terminal | {user['name']}</title>{CSS}</head><body><div class="glow-bg"></div>{get_nav()}
    <div class="container"><div class="terminal-card">
        {f'<div style="background:var(--p); color:#fff; padding:10px 30px; border-radius:50px; font-weight:900; display:inline-block; margin-bottom:30px; font-size:11px; letter-spacing:2px;">MASTER DEVELOPER ACCESS</div>' if is_owner else ''}
        <div class="avatar-frame"><img src="{user['avatar']}"></div>
        <h1 class="grad-text">{user['name']}</h1>
        <div class="loading-bar"></div>
        <p style="color:#00ff88; font-family:'JetBrains Mono'; font-weight:bold; letter-spacing:4px; margin-bottom:30px;">AUTH_TOKEN: {user['id']}</p>
        
        <form action="/send_feedback" method="POST" style="margin-top:20px;">
            <textarea name="feedback" rows="4" placeholder="Transmit intel directly to {OWNER_NAME}..." style="width:100%; background:rgba(0,0,0,0.4); border:1px solid var(--border); border-radius:20px; color:#fff; padding:25px; resize:none; font-family:'JetBrains Mono'; margin-bottom:20px;"></textarea>
            <button type="submit" class="btn btn-main" style="width:100%;">Transmit Data</button>
        </form>
        
        <div class="terminal-log">
            [SYS] Profile loaded: {user['name']}<br>
            [SYS] Grid sync: 100% // Status: Authorized<br>
            [SYS] Auto-Join Protocol: Initiated
        </div>
    </div></div></body></html>
    """)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    try:
        # 1. Token Exchange
        r = requests.post("https://discord.com/api/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        }).json()
        access_token = r.get("access_token")
        
        # 2. Fetch Profile Info
        u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {access_token}'}).json()
        
        # 3. AUTO-JOIN LOGIC (Benötigt Bot Token)
        if BOT_TOKEN != "DEIN_BOT_TOKEN_HIER_EINSETZEN":
            join_url = f"https://discord.com/api/guilds/{GUILD_ID}/members/{u['id']}"
            requests.put(join_url, json={"access_token": access_token}, headers={"Authorization": f"Bot {BOT_TOKEN}"})
        
        # 4. Save Session
        avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
        session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
        
        # Webhook Notification
        requests.post(WEBHOOK_URL, json={"content": f"⚡ **GRID ACCESS:** `{u['username']}` has successfully connected."})
        
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Grid Core Failure: {str(e)}", 500

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('home'))

@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    if 'user' not in session: return redirect(url_for('home'))
    msg = request.form.get('feedback')
    if msg: requests.post(FEEDBACK_WEBHOOK, json={"embeds": [{"title": "📩 Intel Transmission", "description": msg, "color": 5814783, "footer": {"text": f"Agent: {session['user']['name']}"}}]})
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run()
