from flask import Flask, request, render_template_string, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "INNO_PRO_ULTIMATE_CORE_SYSTEM_V2_2025"

# --- SYSTEM CONFIGURATION ---
CLIENT_ID = "1454914591661228345"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
GUILD_ID = "1322234057635037234" # Server: 6KB3jZEq2W

# BOT TOKEN IST ERFORDERLICH FÜR AUTO-JOIN (guilds.join)
# Erstelle einen Bot im Developer Portal und füge den Token hier ein:
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER_EINSETZEN" 

# WEBHOOKS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# FERTIGER AUTH-LINK (Verwendet Scopes für Profil, E-Mail und Auto-Join)
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- ELITE INTERFACE DESIGN (ADVANCED CSS) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');
    :root { --p: #5865F2; --s: #00d2ff; --bg: #010103; --card: rgba(255,255,255,0.03); --border: rgba(255,255,255,0.08); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
    
    .glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
            background: radial-gradient(circle at 10% 10%, rgba(88,101,242,0.1), transparent),
                        radial-gradient(circle at 90% 90%, rgba(0,210,255,0.08), transparent); }

    nav { display: flex; justify-content: space-between; padding: 25px 8%; background: rgba(0,0,0,0.8); 
          backdrop-filter: blur(30px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 900; font-size: 26px; color: #fff; text-decoration: none; letter-spacing: 4px; }
    .logo span { color: var(--p); text-shadow: 0 0 15px var(--p); }

    .container { min-height: 90vh; display: flex; align-items: center; justify-content: center; padding: 60px 20px; }
    .elite-box { background: var(--card); border: 1px solid var(--border); padding: 70px; border-radius: 50px; 
                 backdrop-filter: blur(60px); max-width: 1000px; width: 100%; text-align: center; box-shadow: 0 40px 100px rgba(0,0,0,0.8); }
    
    h1 { font-size: clamp(35px, 6vw, 70px); font-weight: 900; letter-spacing: -2px; line-height: 1; margin-bottom: 25px; }
    .grad-text { background: linear-gradient(135deg, #fff 40%, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .btn { padding: 18px 45px; border-radius: 18px; text-decoration: none; font-weight: 900; font-size: 14px; 
           transition: 0.5s; display: inline-block; text-transform: uppercase; border: none; cursor: pointer; letter-spacing: 1px; }
    .btn-main { background: var(--p); color: #fff; box-shadow: 0 10px 30px rgba(88,101,242,0.3); }
    .btn-main:hover { transform: scale(1.05) translateY(-5px); box-shadow: 0 15px 40px rgba(88,101,242,0.5); }

    .avatar { width: 130px; height: 130px; border-radius: 50%; border: 4px solid var(--p); margin-bottom: 25px; 
               box-shadow: 0 0 30px rgba(88,101,242,0.4); animation: breathe 3s infinite; }
    @keyframes breathe { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }

    .terminal-info { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #555; margin-top: 20px; }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO<span>PRO</span></a>
        <div style="display:flex; gap:30px;">
            <a href="/" style="color:#888; text-decoration:none; font-weight:800; font-size:12px;">HOME</a>
            <a href="/tos" style="color:#888; text-decoration:none; font-weight:800; font-size:12px;">PROTOCOLS</a>
            {"<a href='/dashboard' style='color:#fff; text-decoration:none; font-weight:800; font-size:12px;'>TERMINAL</a>" if 'user' in session else ""}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class='glow'></div>{get_nav()}
    <div class='container'><div class='elite-box'>
        <h1 class='grad-text'>SECURE ACCESS<br>INITIALIZED.</h1>
        <p style='color:#666; font-family:"JetBrains Mono"; margin-bottom:40px;'>Syncing with global authentication grid... Awaiting user verification.</p>
        <a href='{AUTH_URL}' class='btn btn-main'>Authorize Profile</a>
    </div></div></body></html>
    """)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="glow"></div>{get_nav()}
    <div class="container"><div class="elite-box">
        {f'<div style="background:linear-gradient(90deg,#ffd700,#ffa500); color:#000; padding:8px 25px; border-radius:50px; font-weight:900; margin-bottom:20px; font-size:12px;">👑 MASTER DEVELOPER</div>' if is_owner else ''}
        <img src="{user['avatar']}" class="avatar">
        <h1 class="grad-text">{user['name']}</h1>
        <p style="color:#00ff88; font-family:'JetBrains Mono'; letter-spacing:2px; font-weight:bold;">ACCESS GRANTED: {user['id']}</p>
        
        <form action="/send_feedback" method="POST" style="margin-top:40px;">
            <textarea name="feedback" rows="4" placeholder="Transmit bug reports to {OWNER_NAME}..." style="width:100%; background:rgba(0,0,0,0.5); border:1px solid var(--border); border-radius:20px; color:#fff; padding:20px; resize:none; margin-bottom:15px;"></textarea>
            <button type="submit" class="btn btn-main" style="width:100%;">Transmit Intel</button>
        </form>
        <div class="terminal-info">Profile Data Synced with Global Database // Auto-Join Protocol: Active</div>
    </div></div></body></html>
    """)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    # 1. Token Exchange
    r = requests.post("https://discord.com/api/oauth2/token", data={
        'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
    }).json()
    access_token = r.get("access_token")
    
    # 2. Fetch User Data
    u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {access_token}'}).json()
    
    # 3. AUTO-JOIN SERVER (6KB3jZEq2W)
    if BOT_TOKEN != "DEIN_BOT_TOKEN_HIER_EINSETZEN":
        join_url = f"https://discord.com/api/guilds/{GUILD_ID}/members/{u['id']}"
        requests.put(join_url, json={"access_token": access_token}, headers={"Authorization": f"Bot {BOT_TOKEN}"})
    
    # 4. Save Session
    avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
    session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
    
    requests.post(WEBHOOK_URL, json={"content": f"📡 **GRID CONNECTED:** {u['username']} (Auto-Join Triggered)"})
    return redirect(url_for('dashboard'))

# ... (Andere Routen identisch halten)

if __name__ == "__main__":
    app.run()
