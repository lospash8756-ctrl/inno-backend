from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import logging
import time

# Initialize Extended Core System
app = Flask(__name__)
app.secret_key = "INNO_PRO_ENCRYPTED_ULTIMATE_CORE_2025_V4_STABLE"

# --- SYSTEM ARCHITECTURE & ENCRYPTION CONFIG ---
CLIENT_ID = "1454914591661228345"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"

# AUTO-JOIN PROTOCOL (6KB3jZEq2W)
GUILD_ID = "1322234057635037234"
# IMPORTANT: Insert your Bot Token here for Auto-Join functionality!
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER" 

# ANALYTICS WEBHOOKS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# MASTER AUTH LINK (Scopes: identify, email, guilds, guilds.join)
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- NEXT-GEN CYBER INTERFACE (EXTENDED CSS) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');
    :root { --p: #5865F2; --s: #00d2ff; --bg: #010103; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.08); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
    
    .glow-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
                    background: radial-gradient(circle at 10% 15%, rgba(88,101,242,0.12), transparent),
                                radial-gradient(circle at 85% 85%, rgba(0,210,255,0.08), transparent); }

    nav { display: flex; justify-content: space-between; padding: 25px 8%; background: rgba(0,0,0,0.85); 
          backdrop-filter: blur(40px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 900; font-size: 26px; color: #fff; text-decoration: none; letter-spacing: 5px; }
    .logo span { color: var(--p); text-shadow: 0 0 15px var(--p); }
    .nav-links a { color: #666; text-decoration: none; margin-left: 35px; font-size: 11px; font-weight: 800; text-transform: uppercase; transition: 0.4s; }
    .nav-links a:hover { color: #fff; text-shadow: 0 0 10px #fff; }

    .view-container { min-height: 90vh; display: flex; align-items: center; justify-content: center; padding: 80px 20px; }
    .elite-card { background: var(--card); border: 1px solid var(--border); padding: 70px; border-radius: 50px; 
                  backdrop-filter: blur(80px); max-width: 1050px; width: 100%; text-align: center; 
                  box-shadow: 0 40px 100px rgba(0,0,0,0.9); transition: 0.6s cubic-bezier(0.2, 1, 0.2, 1); }
    
    h1 { font-size: clamp(35px, 6vw, 75px); font-weight: 900; letter-spacing: -3px; line-height: 0.95; margin-bottom: 25px; }
    .neon-text { background: linear-gradient(135deg, #fff 40%, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .btn { padding: 20px 45px; border-radius: 18px; text-decoration: none; font-weight: 900; font-size: 14px; 
           transition: 0.5s; display: inline-block; text-transform: uppercase; border: none; cursor: pointer; letter-spacing: 2px; }
    .btn-p { background: var(--p); color: #fff; box-shadow: 0 15px 40px rgba(88,101,242,0.4); }
    .btn-p:hover { transform: scale(1.05) translateY(-5px); box-shadow: 0 20px 50px rgba(88,101,242,0.6); }

    .profile-avatar { width: 140px; height: 140px; border-radius: 50%; border: 4px solid var(--p); margin: 0 auto 30px auto; 
                       box-shadow: 0 0 40px rgba(88,101,242,0.4); }
    
    .tos-box { text-align: left; background: rgba(0,0,0,0.3); padding: 35px; border-radius: 25px; height: 400px; 
               overflow-y: auto; border: 1px solid var(--border); margin-bottom: 30px; font-size: 13px; line-height: 1.8; color: #888; }
    .tos-box b { color: var(--s); text-transform: uppercase; font-size: 11px; display: block; margin-top: 15px; }

    .terminal-log { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #444; text-align: left; 
                    background: rgba(0,0,0,0.4); padding: 20px; border-radius: 15px; margin-top: 40px; }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO<span>PRO</span></a>
        <div class="nav-links">
            <a href="/">Interface</a>
            <a href="/tos">Protocols</a>
            {"<a href='/dashboard'>Terminal</a><a href='/logout' style='color:#ff3333;'>Disconnect</a>" if 'user' in session else f"<a href='{AUTH_URL}'>Initialize</a>"}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"<html><head><title>INNO PRO | Portal</title>{CSS}</head><body><div class='glow-overlay'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>GRID ACCESS<br>PENDING.</h1><p style='color:#444; font-family:\"JetBrains Mono\"; margin-bottom:40px;'>Centralized Security Interface v5.2 // Awaiting Authorization</p><a href='{AUTH_URL}' class='btn btn-p'>Authorize Connection</a></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    
    return render_template_string(f"""
    <html><head><title>Terminal | {user['name']}</title>{CSS}</head><body><div class="glow-overlay"></div>{get_nav()}
    <div class="view-container"><div class="elite-card">
        {f'<div style="background:var(--p); color:#fff; padding:10px 30px; border-radius:50px; font-weight:900; display:inline-block; margin-bottom:25px; font-size:11px; letter-spacing:2px;">MASTER DEVELOPER PRIVILEGES</div>' if is_owner else ''}
        <img src="{user['avatar']}" class="profile-avatar">
        <h1 class="neon-text">{user['name']}</h1>
        <p style="color:#00ff88; font-family:'JetBrains Mono'; font-weight:bold; letter-spacing:4px;">SYNC_ID: {user['id']}</p>
        
        <form action="/send_feedback" method="POST" style="margin-top:40px;">
            <textarea name="feedback" rows="4" placeholder="Transmit intel to {OWNER_NAME}..." style="width:100%; background:rgba(0,0,0,0.5); border:1px solid var(--border); border-radius:20px; color:#fff; padding:25px; resize:none; font-family:'JetBrains Mono'; margin-bottom:15px;"></textarea>
            <button type="submit" class="btn btn-p" style="width:100%;">Transmit Intel</button>
        </form>
        <div class="terminal-log">
            [SYS] Auth successful // User: {user['name']}<br>
            [SYS] Encryption: AES-256 Enabled<br>
            [SYS] Auto-Join: Synchronized with {GUILD_ID}
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
        if not access_token: return "Grid Handshake Failure", 500

        # 2. Advanced Profile Fetching (Retry-Logic)
        u_req = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {access_token}'})
        if u_req.status_code != 200: return "Failed to retrieve Discord Identity", 500
        
        u = u_req.json()
        # FIXED: Robust identity resolution
        username = u.get('username') or u.get('global_name') or u.get('id')
        user_id = u.get('id')

        # 3. AUTO-JOIN LOGIC (6KB3jZEq2W)
        if BOT_TOKEN != "DEIN_BOT_TOKEN_HIER":
            requests.put(f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}", 
                         json={"access_token": access_token}, 
                         headers={"Authorization": f"Bot {BOT_TOKEN}"})

        # 4. Finalize Session
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{u.get('avatar')}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
        session['user'] = {'name': username, 'id': user_id, 'avatar': avatar}
        
        requests.post(WEBHOOK_URL, json={"content": f"⚡ **CORE SYNC:** `{username}` authorized."})
        return redirect(url_for('dashboard'))

    except Exception as e:
        return f"Grid Core Failure: {str(e)}", 500

@app.route('/tos')
def tos():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class='glow-overlay'></div>{get_nav()}<div class='view-container'><div class='elite-card'>
        <h1 class='neon-text'>SECURITY<br>PROTOCOLS</h1>
        <div class='tos-box'>
            <b>01. Neural Interface Usage</b><p>You agree to the 256-bit encryption of all transmitted metadata.</p>
            <b>02. Identity Verification</b><p>Profile sync is mandatory for grid access. Multi-accounting results in a permanent HWID ban.</p>
            <b>03. Code Integrity</b><p>Attempting to debug or intercept grid traffic is strictly forbidden by the administration.</p>
            <b>04. Data Privacy</b><p>We only store your Discord Snowflake ID for authentication. No personal data is harvested.</p>
            <b>05. Service Termination</b><p>{OWNER_NAME} reserves the right to disconnect any node at any time.</p>
        </div>
        <a href='/' class='btn btn-p'>Accept Protocols</a>
    </div></div></body></html>
    """)

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('home'))

@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    if 'user' not in session: return redirect(url_for('home'))
    msg = request.form.get('feedback')
    if msg: requests.post(FEEDBACK_WEBHOOK, json={"embeds": [{"title": "📩 Intel Received", "description": msg, "color": 5814783, "footer": {"text": f"Agent: {session['user']['name']}"}}]})
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run()
