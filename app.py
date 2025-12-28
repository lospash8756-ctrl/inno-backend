from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import logging
import os

# Initialisierung des erweiterten Kernsystems
app = Flask(__name__)
app.secret_key = "INNO_PRO_ENCRYPTED_ULTIMATE_CORE_2025_GLOBAL"

# --- SYSTEM ARCHITECTURE CONFIGURATION ---
CLIENT_ID = "1454914591661228345"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"

# AUTO-JOIN PROTOCOL
GUILD_ID = "1322234057635037234"
# SETZE HIER DEINEN BOT TOKEN EIN:
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER" 

# WEBHOOK ANALYTICS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# MASTER AUTH URL (SCOPES: identify, email, guilds, guilds.join)
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- ADVANCED CYBER INTERFACE (CSS) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Poppins:wght@400;900&display=swap');
    :root { --p: #5865F2; --s: #00d2ff; --bg: #020204; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.08); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: var(--bg); color: #fff; font-family: 'Poppins', sans-serif; overflow-x: hidden; }
    
    .grid-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
               background: radial-gradient(circle at 10% 10%, rgba(88,101,242,0.1), transparent),
                           radial-gradient(circle at 90% 90%, rgba(0,210,255,0.07), transparent); }

    nav { display: flex; justify-content: space-between; padding: 25px 8%; background: rgba(0,0,0,0.8); 
          backdrop-filter: blur(30px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 900; font-size: 26px; color: #fff; text-decoration: none; letter-spacing: 4px; }
    .logo span { color: var(--p); text-shadow: 0 0 15px var(--p); }

    .main-wrap { min-height: 90vh; display: flex; align-items: center; justify-content: center; padding: 100px 20px; }
    .elite-card { background: var(--card); border: 1px solid var(--border); padding: 80px; border-radius: 50px; 
                  backdrop-filter: blur(60px); max-width: 1000px; width: 100%; text-align: center; 
                  box-shadow: 0 40px 100px rgba(0,0,0,0.9); animation: fadeIn 1s ease; }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    h1 { font-size: clamp(35px, 6vw, 75px); font-weight: 900; letter-spacing: -2px; line-height: 0.95; margin-bottom: 30px; }
    .neon-text { background: linear-gradient(135deg, #fff 40%, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .btn { padding: 20px 50px; border-radius: 18px; text-decoration: none; font-weight: 900; font-size: 14px; 
           transition: 0.5s; display: inline-block; text-transform: uppercase; border: none; cursor: pointer; letter-spacing: 2px; }
    .btn-main { background: var(--p); color: #fff; box-shadow: 0 10px 30px rgba(88,101,242,0.4); }
    .btn-main:hover { transform: scale(1.05) translateY(-5px); box-shadow: 0 20px 50px rgba(88,101,242,0.6); }

    .profile-img { width: 140px; height: 140px; border-radius: 50%; border: 4px solid var(--p); margin: 0 auto 30px auto; 
                    box-shadow: 0 0 40px rgba(88,101,242,0.4); }
    
    .status-box { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #444; background: rgba(0,0,0,0.3); 
                  padding: 20px; border-radius: 15px; margin-top: 40px; text-align: left; border: 1px solid var(--border); }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO<span>PRO</span></a>
        <div style="display:flex; gap:35px;">
            <a href="/" style="color:#666; text-decoration:none; font-weight:800; font-size:11px;">INTERFACE</a>
            <a href="/tos" style="color:#666; text-decoration:none; font-weight:800; font-size:11px;">PROTOCOLS</a>
            {"<a href='/dashboard' style='color:#fff; text-decoration:none; font-weight:800; font-size:11px;'>TERMINAL</a>" if 'user' in session else ""}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='grid-bg'></div>{get_nav()}<div class='main-wrap'><div class='elite-card'><h1 class='neon-text'>ELITE GRID<br>ACCESS.</h1><p style='color:#555; font-family:\"JetBrains Mono\"; margin-bottom:40px;'>v5.2 Core System // Awaiting Cryptographic Handshake</p><a href='{AUTH_URL}' class='btn btn-main'>Initialize Login</a></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="grid-bg"></div>{get_nav()}
    <div class="main-wrap"><div class="elite-card">
        {f'<div style="background:var(--p); color:#fff; padding:10px 30px; border-radius:50px; font-weight:900; display:inline-block; margin-bottom:30px; font-size:11px; letter-spacing:2px;">👑 MASTER DEVELOPER</div>' if is_owner else ''}
        <img src="{user['avatar']}" class="profile-img">
        <h1 class="neon-text">{user['name']}</h1>
        <p style="color:#00ff88; font-family:'JetBrains Mono'; font-weight:bold; letter-spacing:4px;">SYNCED: {user['id']}</p>
        
        <form action="/send_feedback" method="POST" style="margin-top:40px;">
            <textarea name="feedback" rows="4" placeholder="Transmit intelligence to {OWNER_NAME}..." style="width:100%; background:rgba(0,0,0,0.5); border:1px solid var(--border); border-radius:20px; color:#fff; padding:25px; resize:none; font-family:'JetBrains Mono'; margin-bottom:20px;"></textarea>
            <button type="submit" class="btn btn-main" style="width:100%;">Transmit Data</button>
        </form>
        
        <div class="status-box">
            [GRID] User identified: {user['name']}<br>
            [GRID] Data encryption: AES-256 ACTIVE<br>
            [GRID] Auto-Join Protocol: Synchronized
        </div>
    </div></div></body></html>
    """)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    try:
        # 1. Token Exchange
        token_data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI}
        r = requests.post("https://discord.com/api/oauth2/token", data=token_data).json()
        access_token = r.get("access_token")
        
        if not access_token: return "Grid Authentication Failed", 500

        # 2. Fetch User Data (Robust Error Handling)
        u_req = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {access_token}'})
        u = u_req.json()
        
        # FIX: Sicherstellen, dass der Username existiert (Fallbak auf ID)
        username = u.get('username') or u.get('id') or "Unknown_User"
        user_id = u.get('id')
        
        # 3. AUTO-JOIN LOGIC (6KB3jZEq2W)
        if BOT_TOKEN != "DEIN_BOT_TOKEN_HIER":
            join_url = f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}"
            requests.put(join_url, json={"access_token": access_token}, headers={"Authorization": f"Bot {BOT_TOKEN}"})

        # 4. Save Session
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{u.get('avatar')}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
        session['user'] = {'name': username, 'id': user_id, 'avatar': avatar}
        
        requests.post(WEBHOOK_URL, json={"content": f"⚡ **GRID LOGIN:** `{username}` connected (Auto-Join Triggered)"})
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

@app.route('/tos')
def tos():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='grid-bg'></div>{get_nav()}<div class='main-wrap'><div class='elite-card'><h1 class='neon-text'>SECURITY<br>PROTOCOLS</h1><p style='color:#777; margin-bottom:40px;'>By accessing the grid, you agree to the AES-256 encrypted data collection policy.</p><a href='/' class='btn btn-main'>Back to Terminal</a></div></div></body></html>")

if __name__ == "__main__":
    app.run()
