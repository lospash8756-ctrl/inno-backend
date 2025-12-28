from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import os
import json
import time

# --- CORE SYSTEM INITIALIZATION ---
app = Flask(__name__)
# Global Security Layer: Fixes ENV missing variable errors
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'INNO_PRO_ULTIMATE_V9_CORE_ENCRYPTED_2025')

# --- ELITE CONFIGURATION GRID ---
CLIENT_ID = "1454914591661228345"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"

# AUTO-JOIN SERVER PROTOCOL (Server: 6KB3jZEq2W)
GUILD_ID = "1322234057635037234"
# MANDATORY: Insert your Bot Token here to enable auto-server entry
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" 

# ANALYTICS & MONITORING WEBHOOKS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# SECURE AUTH LINK (Scopes: identify, guilds, email, guilds.join)
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- NEXT-GEN CYBER INTERFACE (V9 ULTRA-EXTENDED) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');
    :root { --p: #5865F2; --s: #00d2ff; --bg: #010103; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.08); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
    
    .glow-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
                  background: radial-gradient(circle at 10% 15%, rgba(88,101,242,0.15), transparent),
                              radial-gradient(circle at 85% 85%, rgba(0,210,255,0.1), transparent); }

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

    .tos-grid { text-align: left; background: rgba(0,0,0,0.3); padding: 45px; border-radius: 35px; height: 550px; 
                overflow-y: auto; border: 1px solid var(--border); margin-bottom: 30px; font-size: 14px; line-height: 2.5; color: #999; }
    .tos-grid b { color: var(--s); display: block; margin-top: 30px; text-transform: uppercase; font-size: 12px; }
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
    return render_template_string(f"<html><head><title>INNO PRO | Portal</title>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>ELITE GRID<br>SYNCHRONIZED</h1><p style='color:#444; font-family:\"JetBrains Mono\"; margin-bottom:40px;'>Centralized Security Interface v9.0 // AES-256 Active</p><a href='{AUTH_URL}' class='btn btn-p'>Authorize Profile</a></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    return render_template_string(f"<html><head><title>Terminal | {user['name']}</title>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}<div class='view-container'><div class='elite-card'>{f'<div style=\"background:var(--p); color:white; padding:5px 25px; border-radius:50px; font-weight:900; margin-bottom:20px;\">MASTER DEVELOPER</div>' if is_owner else ''}<img src='{user['avatar']}' style='width:130px; border-radius:50%; border:3px solid var(--p); margin-bottom:25px;'><h1 class='neon-text'>{user['name']}</h1><p style='color:lime; font-family:\"JetBrains Mono\";'>AUTHORIZED AGENT</p><br><a href='{DISCORD_INVITE}' class='btn btn-p'>Official Discord</a></div></div></body></html>")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    try:
        # STEP 1: TOKEN HANDSHAKE V9
        token_url = "https://discord.com/api/v10/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        }
        
        r = requests.post(token_url, data=data, headers=headers)
        
        # DEBUG: Catching handshake failure immediately
        if r.status_code != 200:
            return f"Grid Handshake Failure: Server returned {r.status_code}. Response: {r.text}", 500
            
        token_data = r.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            return "Grid Handshake Failure: Access Token missing from Discord response.", 500

        # STEP 2: IDENTITY EXTRACTION
        u = requests.get("https://discord.com/api/v10/users/@me", headers={'Authorization': f'Bearer {access_token}'}).json()
        username = u.get('username') or u.get('global_name') or u.get('id') or "Unknown_Agent"
        user_id = u.get('id')

        # STEP 3: AUTO-JOIN PROTOCOL
        if BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
            join_url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}"
            requests.put(join_url, json={"access_token": access_token}, headers={"Authorization": f"Bot {BOT_TOKEN}"})

        # STEP 4: SESSION FINALIZATION
        avatar_hash = u.get('avatar')
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png" if avatar_hash else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
        session['user'] = {'name': username, 'id': user_id, 'avatar': avatar}
        
        requests.post(WEBHOOK_URL, json={"content": f"⚡ **CORE SYNC:** `{username}` authorized into the grid."})
        return redirect(url_for('dashboard'))

    except Exception as e:
        return f"Grid Handshake Failure: {str(e)}", 500

@app.route('/tos')
def tos():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>SECURITY PROTOCOLS</h1><div class='tos-grid'><b>01. DATA COLLECTION</b><p>By synchronizing your profile, you authorize the collection of your Snowflake ID for authentication purposes. We do not store passwords or IP addresses.</p><b>02. ANTI-REVERSE ENGINEERING</b><p>Any attempt to debug, decompile, or monitor grid traffic via external software is strictly forbidden and results in a permanent HWID blacklist.</p><b>03. REFUND POLICY</b><p>Due to the digital nature of our services, all access grants are final. Chargebacks are considered fraud and will be reported.</p><b>04. OWNER RIGHTS</b><p>{OWNER_NAME} reserves the right to terminate access at any time for security violations.</p></div><br><a href='/' class='btn btn-p'>Accept Protocols</a></div></div></body></html>")

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
