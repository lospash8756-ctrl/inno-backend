from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import os
import logging

# --- CORE INITIALIZATION ---
app = Flask(__name__)
# Fixes the ENV error by providing a fallback key
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'INNO_PRO_ENCRYPTED_ULTIMATE_CORE_V7_STABLE_9921')

# --- ELITE SYSTEM CONFIGURATION ---
CLIENT_ID = "1454914591661228345"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"

# AUTO-JOIN PROTOCOL
GUILD_ID = "1322234057635037234"
# MANDATORY: Insert your Bot Token here to enable guilds.join
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER" 

# ANALYTICS & FEEDBACK WEBHOOKS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# FULL SCOPE AUTH URL
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- NEXT-GEN CYBER INTERFACE (V7 EXTENDED) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');
    :root { --p: #5865F2; --s: #00d2ff; --bg: #010103; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.08); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
    
    .glow-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
                  background: radial-gradient(circle at 10% 15%, rgba(88,101,242,0.12), transparent),
                              radial-gradient(circle at 85% 85%, rgba(0,210,255,0.08), transparent); }

    nav { display: flex; justify-content: space-between; padding: 25px 8%; background: rgba(0,0,0,0.85); 
          backdrop-filter: blur(40px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 900; font-size: 26px; color: #fff; text-decoration: none; letter-spacing: 5px; }
    .logo span { color: var(--p); text-shadow: 0 0 15px var(--p); }
    .nav-links a { color: #666; text-decoration: none; margin-left: 35px; font-size: 11px; font-weight: 800; text-transform: uppercase; transition: 0.4s; }
    .nav-links a:hover { color: #fff; text-shadow: 0 0 10px #fff; }

    .view-container { min-height: 90vh; display: flex; align-items: center; justify-content: center; padding: 80px 20px; flex-direction: column; }
    .elite-card { background: var(--card); border: 1px solid var(--border); padding: 70px; border-radius: 50px; 
                  backdrop-filter: blur(80px); max-width: 1050px; width: 100%; text-align: center; 
                  box-shadow: 0 40px 100px rgba(0,0,0,0.9); transition: 0.5s; }
    
    h1 { font-size: clamp(35px, 6vw, 75px); font-weight: 900; letter-spacing: -3px; line-height: 0.95; margin-bottom: 25px; }
    .neon-text { background: linear-gradient(135deg, #fff 40%, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .btn { padding: 20px 45px; border-radius: 18px; text-decoration: none; font-weight: 900; font-size: 14px; 
           transition: 0.5s; display: inline-block; text-transform: uppercase; border: none; cursor: pointer; letter-spacing: 2px; }
    .btn-p { background: var(--p); color: #fff; box-shadow: 0 15px 40px rgba(88,101,242,0.4); }
    .btn-p:hover { transform: scale(1.05) translateY(-5px); box-shadow: 0 20px 50px rgba(88,101,242,0.6); }

    .tos-grid { text-align: left; background: rgba(0,0,0,0.3); padding: 40px; border-radius: 30px; height: 550px; 
                overflow-y: auto; border: 1px solid var(--border); margin-bottom: 30px; font-size: 13px; line-height: 2.2; color: #888; }
    .tos-grid b { color: var(--s); display: block; margin-top: 25px; text-transform: uppercase; font-size: 11px; }

    .terminal-output { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #444; text-align: left; 
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
    return render_template_string(f"<html><head><title>INNO PRO | Portal</title>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>INNO PRO<br>SYSTEM CORE</h1><p style='color:#444; font-family:\"JetBrains Mono\"; margin-bottom:40px;'>Centralized Security Interface v7.0 // Stable Build</p><a href='{AUTH_URL}' class='btn btn-p'>Authorize Profile</a></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    
    return render_template_string(f"""
    <html><head><title>Terminal | {user['name']}</title>{CSS}</head><body><div class="glow-layer"></div>{get_nav()}
    <div class="view-container"><div class="elite-card">
        {f'<div style="background:var(--p); color:#fff; padding:10px 30px; border-radius:50px; font-weight:900; display:inline-block; margin-bottom:25px; font-size:11px; letter-spacing:2px;">MASTER DEVELOPER ACCESS</div>' if is_owner else ''}
        <img src="{user['avatar']}" style="width:130px; height:130px; border-radius:50%; border:4px solid var(--p); margin-bottom:25px; box-shadow:0 0 40px rgba(88,101,242,0.4);">
        <h1 class="neon-text">{user['name']}</h1>
        <p style="color:#00ff88; font-family:'JetBrains Mono'; font-weight:bold; letter-spacing:4px;">ACCESS_TOKEN: {user['id']}</p>
        
        <form action="/send_feedback" method="POST" style="margin-top:40px;">
            <textarea name="feedback" rows="4" placeholder="Transmit intel to {OWNER_NAME}..." style="width:100%; background:rgba(0,0,0,0.5); border:1px solid var(--border); border-radius:20px; color:#fff; padding:25px; resize:none; font-family:'JetBrains Mono'; margin-bottom:15px;"></textarea>
            <button type="submit" class="btn btn-p" style="width:100%;">Transmit Intel</button>
        </form>
    </div></div></body></html>
    """)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    try:
        # Token Handshake
        r = requests.post("https://discord.gg/api/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        })
        
        token_data = r.json()
        access_token = token_data.get("access_token")
        if not access_token: return "Grid Handshake Failure: Access Token Missing", 500

        # Identity Extraction with Multi-Level Fallback
        u_req = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {access_token}'})
        u = u_req.json()
        
        # FIXED: Robust User Identity Resolution (Fixes 'username' error)
        username = u.get('username') or u.get('global_name') or u.get('id') or "Unknown_User"
        user_id = u.get('id')

        # Auto-Join Protocol
        if BOT_TOKEN != "DEIN_BOT_TOKEN_HIER":
            requests.put(f"https://discord.com/api/guilds/{GUILD_ID}/members/{user_id}", 
                         json={"access_token": access_token}, 
                         headers={"Authorization": f"Bot {BOT_TOKEN}"})

        # Save Final Session Data
        avatar_hash = u.get('avatar')
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png" if avatar_hash else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
        
        session['user'] = {'name': username, 'id': user_id, 'avatar': avatar}
        
        requests.post(WEBHOOK_URL, json={"content": f"⚡ **CORE SYNC:** `{username}` (UID: {user_id}) authorized."})
        return redirect(url_for('dashboard'))

    except Exception as e:
        return f"Grid Core Failure: {str(e)}", 500

@app.route('/tos')
def tos():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}<div class='view-container'><div class='elite-card'>
        <h1 class='neon-text'>SECURITY<br>PROTOCOLS</h1>
        <div class='tos-grid'>
            <b>01. GRID USAGE AGREEMENT</b><p>By connecting to INNO PRO, you authorize the temporary storage of your Discord Snowflake ID for verification. Packets are encrypted via AES-256 standards.</p>
            <b>02. ACCOUNT INTEGRITY</b><p>Licenses are bound to a unique HWID fingerprint. Attempting to spoof, share, or bypass hardware locks results in a permanent blacklist.</p>
            <b>03. ANTI-ANALYSIS MEASURES</b><p>Usage of debuggers, packet sniffers (Wireshark), or virtual machine environments is strictly prohibited. Detection leads to immediate node disconnection.</p>
            <b>04. NO REFUND POLICY</b><p>Grid access is a digital service. Once authorized, all access rights are final. Chargebacks result in a global ban and legal report.</p>
            <b>05. OWNER AUTHORITY</b><p>{OWNER_NAME} reserves the right to terminate any active session for security or maintenance reasons without prior notice.</p>
            <b>06. SYSTEM STABILITY</b><p>We do not guarantee 100% grid uptime. Maintenance windows are announced in the official community server.</p>
            <b>07. PROHIBITED CODE</b><p>The redistribution or modification of grid resources is a violation of copyright protocols.</p>
        </div>
        <a href='/' class='btn btn-p'>I Accept All Protocols</a>
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
