from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import time

app = Flask(__name__)
app.secret_key = "INNO_PRO_ULTIMATE_CORE_SYSTEM_2025"

# --- SYSTEM CONFIGURATION ---
CLIENT_ID = "1454914591661228345"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
GUILD_ID = "1322234057635037234" # Die ID deines Servers (6KB3jZEq2W)
BOT_TOKEN = "MTE3NzMzNzA1OTI0MjY4ODY3Mg.GjXmC7.xxxxxxxxxxxxxxxxxxxx" # HINWEIS: Du musst deinen Bot-Token hier einfügen, damit der Auto-Join funktioniert!

# WEBHOOKS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# Neuer Auth-Link mit allen erforderlichen Scopes (identify, email, guilds, guilds.join)
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- UI & UX ARCHITECTURE (EXTENDED) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');
    :root { --p: #5865F2; --s: #00d2ff; --bg: #010102; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.07); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }

    /* Matrix-like Background Glow */
    .glow-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
                  background: radial-gradient(circle at 15% 15%, rgba(88,101,242,0.12), transparent 40%),
                              radial-gradient(circle at 85% 85%, rgba(0,210,255,0.08), transparent 40%); }

    nav { display: flex; justify-content: space-between; align-items: center; padding: 25px 8%; 
          background: rgba(0,0,0,0.8); backdrop-filter: blur(25px); border-bottom: 1px solid var(--border); 
          position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 900; font-size: 26px; color: #fff; text-decoration: none; letter-spacing: 5px; font-family: 'Inter'; }
    .logo span { color: var(--p); text-shadow: 0 0 15px var(--p); }
    .nav-links a { color: #888; text-decoration: none; margin-left: 35px; font-size: 11px; font-weight: 800; 
                   text-transform: uppercase; transition: all 0.4s ease; letter-spacing: 1px; }
    .nav-links a:hover { color: #fff; transform: translateY(-2px); }

    .main-container { min-height: 90vh; display: flex; align-items: center; justify-content: center; padding: 60px 20px; }
    .elite-card { background: var(--card); border: 1px solid var(--border); padding: 70px; border-radius: 50px; 
                  backdrop-filter: blur(50px); max-width: 1100px; width: 100%; text-align: center; 
                  box-shadow: 0 40px 100px rgba(0,0,0,0.9); position: relative; overflow: hidden; }
    
    .elite-card::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 3px; 
                          background: linear-gradient(90deg, transparent, var(--p), transparent); animation: scan 4s linear infinite; }
    @keyframes scan { 0% { left: -100%; } 100% { left: 100%; } }

    h1 { font-size: clamp(40px, 7vw, 75px); font-weight: 900; letter-spacing: -3px; line-height: 0.95; margin-bottom: 25px; }
    .gradient-text { background: linear-gradient(135deg, #fff 30%, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .btn { padding: 20px 45px; border-radius: 18px; text-decoration: none; font-weight: 900; font-size: 14px; 
           transition: 0.5s; display: inline-block; text-transform: uppercase; border: none; cursor: pointer; letter-spacing: 2px; }
    .btn-p { background: var(--p); color: #fff; box-shadow: 0 15px 40px rgba(88,101,242,0.4); }
    .btn-p:hover { transform: scale(1.05) translateY(-5px); box-shadow: 0 20px 50px rgba(88,101,242,0.6); }

    .loading-text { font-family: 'JetBrains Mono', monospace; color: var(--s); font-size: 12px; margin-top: 20px; text-transform: uppercase; }
    .profile-img { width: 140px; height: 140px; border-radius: 50%; border: 4px solid var(--p); margin-bottom: 30px; 
                    box-shadow: 0 0 40px rgba(88,101,242,0.5); animation: pulse 2s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 20px rgba(88,101,242,0.3); } 50% { box-shadow: 0 0 50px rgba(88,101,242,0.6); } 100% { box-shadow: 0 0 20px rgba(88,101,242,0.3); } }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO<span>PRO</span></a>
        <div class="nav-links">
            <a href="/">Interface</a>
            <a href="/features">Database</a>
            <a href="/tos">Protocols</a>
            {"<a href='/dashboard'>Terminal</a><a href='/logout' style='color:#ff3333;'>Disconnect</a>" if 'user' in session else f"<a href='{AUTH_URL}'>Initialize</a>"}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"""
    <html><head><title>INNO PRO | Central Hub</title>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}
    <div class='main-container'><div class='elite-card'>
        <h1 class='gradient-text'>SYSTEMS<br>ONLINE.</h1>
        <p style='color:#555; font-size:18px; max-width:600px; margin:0 auto 40px auto; font-family:"JetBrains Mono";'>Secure connection established. Awaiting user authorization to access the global grid.</p>
        <a href='{AUTH_URL}' class='btn btn-p'>Authorize Access</a>
    </div></div></body></html>
    """)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    
    return render_template_string(f"""
    <html><head><title>Terminal | {user['name']}</title>{CSS}</head><body><div class="glow-layer"></div>{get_nav()}
    <div class="main-container"><div class="elite-card">
        {f'<div style="background:var(--p); color:#fff; padding:10px 30px; border-radius:50px; font-weight:900; display:inline-block; margin-bottom:25px; font-size:12px; letter-spacing:2px;">MASTER DEVELOPER ACCESS</div>' if is_owner else ''}
        <img src="{user['avatar']}" class="profile-img">
        <h1 class="gradient-text">{user['name']}</h1>
        <p class="loading-text">Status: Decrypting User Profile...</p>
        <p style="color:#00ff88; font-family:'JetBrains Mono'; font-weight:bold; letter-spacing:3px; margin-top:10px;">AUTHORIZED: {user['id']}</p>
        
        <div style="margin-top:40px; padding:30px; background:rgba(255,255,255,0.01); border-radius:20px; border:1px solid var(--border);">
            <h3 style="margin-bottom:20px; text-transform:uppercase; font-size:14px; color:var(--s);">Submit Intelligence Report</h3>
            <form action="/send_feedback" method="POST">
                <textarea name="feedback" rows="4" placeholder="Transmit data to {OWNER_NAME}..." style="width:100%; background:rgba(0,0,0,0.5); border:1px solid var(--border); border-radius:15px; color:#fff; padding:20px; resize:none; font-family:'JetBrains Mono';"></textarea>
                <button type="submit" class="btn btn-p" style="width:100%; margin-top:15px;">Transmit Data</button>
            </form>
        </div>
        <br>
        <a href="{DISCORD_INVITE}" class="btn" style="background:rgba(255,255,255,0.05); color:#fff; width:100%;">Access Mainframe (Discord)</a>
    </div></div></body></html>
    """)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    # Token Austausch
    token_data = {
        'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
    }
    r = requests.post("https://discord.com/api/oauth2/token", data=token_data).json()
    access_token = r.get("access_token")
    
    if not access_token: return "Auth Error", 500
    
    # User Daten holen
    u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {access_token}'}).json()
    
    # AUTO-JOIN LOGIC
    # HINWEIS: Dies erfordert einen Bot-Token in der GUILD_ID.
    join_url = f"https://discord.com/api/guilds/{GUILD_ID}/members/{u['id']}"
    headers = {"Authorization": f"Bot {BOT_TOKEN}"}
    payload = {"access_token": access_token}
    requests.put(join_url, json=payload, headers=headers)
    
    # Session speichern
    avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
    session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
    
    # Webhook
    requests.post(WEBHOOK_URL, json={"content": f"📡 **GRID CONNECTED:** `{u['username']}` (Auto-Join triggered)"})
    
    return redirect(url_for('dashboard'))

# ... (Restliche Routen wie /features, /tos, /logout, /send_feedback identisch zum letzten Elite-Patch)

if __name__ == "__main__":
    app.run()
