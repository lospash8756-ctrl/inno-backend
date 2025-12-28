from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import os
import json

# --- CORE ARCHITECTURE V10 ---
app = Flask(__name__)
# Secure fallback for the mandatory ENV variable
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'INNO_ULTIMATE_V10_STABLE_GRID_CORE')

# --- ELITE CONFIGURATION GRID ---
CLIENT_ID = "1454914591661228345"
# ACHTUNG: Füge hier dein NEUES Client Secret ein!
CLIENT_SECRET = "DEIN_NEUES_CLIENT_SECRET_HIER" 
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"

# AUTO-JOIN PROTOCOL
GUILD_ID = "1322234057635037234"
# MANDATORY: Insert your Bot Token here for automatic entry
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER" 

# ANALYTICS WEBHOOKS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# MASTER AUTH URL
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- CYBER TERMINAL INTERFACE (V10 ULTRA-EXTENDED) ---
CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');
    :root { --p: #5865F2; --s: #00d2ff; --bg: #010103; --card: rgba(255,255,255,0.02); --border: rgba(255,255,255,0.08); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: var(--bg); color: #fff; font-family: 'Inter', sans-serif; overflow-x: hidden; }
    
    .glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
            background: radial-gradient(circle at 10% 15%, rgba(88,101,242,0.15), transparent),
                        radial-gradient(circle at 85% 85%, rgba(0,210,255,0.1), transparent); }

    nav { display: flex; justify-content: space-between; padding: 25px 8%; background: rgba(0,0,0,0.85); 
          backdrop-filter: blur(40px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 900; font-size: 26px; color: #fff; text-decoration: none; letter-spacing: 5px; }
    .logo span { color: var(--p); text-shadow: 0 0 15px var(--p); }

    .view-container { min-height: 90vh; display: flex; align-items: center; justify-content: center; padding: 80px 20px; flex-direction: column; }
    .elite-card { background: var(--card); border: 1px solid var(--border); padding: 70px; border-radius: 50px; 
                  backdrop-filter: blur(80px); max-width: 1050px; width: 100%; text-align: center; 
                  box-shadow: 0 40px 100px rgba(0,0,0,0.9); transition: 0.5s; }
    
    h1 { font-size: clamp(35px, 6vw, 75px); font-weight: 900; letter-spacing: -3px; line-height: 0.95; margin-bottom: 25px; }
    .neon-text { background: linear-gradient(135deg, #fff 40%, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .btn { padding: 20px 45px; border-radius: 18px; text-decoration: none; font-weight: 900; font-size: 14px; 
           transition: 0.5s; display: inline-block; text-transform: uppercase; border: none; cursor: pointer; letter-spacing: 2px; }
    .btn-p { background: var(--p); color: #fff; box-shadow: 0 15px 40px rgba(88,101,242,0.4); }

    .tos-scroll { text-align: left; background: rgba(0,0,0,0.3); padding: 45px; border-radius: 35px; height: 500px; 
                  overflow-y: auto; border: 1px solid var(--border); margin-bottom: 30px; font-size: 14px; line-height: 2.2; color: #999; }
    .tos-scroll b { color: var(--s); display: block; margin-top: 30px; text-transform: uppercase; font-size: 12px; }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO<span>PRO</span></a>
        <div style="display:flex; gap:30px;">
            <a href="/" style="color:#666; text-decoration:none; font-weight:800; font-size:11px;">INTERFACE</a>
            <a href="/tos" style="color:#666; text-decoration:none; font-weight:800; font-size:11px;">PROTOCOLS</a>
            {"<a href='/dashboard' style='color:#fff; text-decoration:none; font-weight:800; font-size:11px;'>TERMINAL</a>" if 'user' in session else ""}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"<html><head><title>INNO PRO | Access</title>{CSS}</head><body><div class='glow'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>INNO PRO<br>SYSTEM GRID</h1><p style='color:#444; font-family:\"JetBrains Mono\"; margin-bottom:40px;'>Centralized Security Interface v10.0 // AES-256 Enabled</p><a href='{AUTH_URL}' class='btn btn-p'>Authorize Profile</a></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    return render_template_string(f"<html><head><title>Terminal | {user['name']}</title>{CSS}</head><body><div class='glow'></div>{get_nav()}<div class='view-container'><div class='elite-card'>{f'<div style=\"background:gold; color:black; padding:5px 20px; border-radius:50px; font-weight:900; margin-bottom:20px;\">SYSTEM OWNER</div>' if is_owner else ''}<img src='{user['avatar']}' style='width:120px; border-radius:50%; border:3px solid var(--p); margin-bottom:20px;'><h1 class='neon-text'>{user['name']}</h1><p style='color:lime; font-family:\"JetBrains Mono\";'>AUTHORIZED AGENT</p><br><a href='{DISCORD_INVITE}' class='btn btn-p'>Official Discord</a></div></div></body></html>")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    try:
        # STEP 1: TOKEN HANDSHAKE V10
        r = requests.post("https://discord.com/api/v10/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        if r.status_code != 200:
            return f"Grid Handshake Failure: Server returned {r.status_code}. Response: {r.text}", 500
            
        token_data = r.json()
        access_token = token_data.get("access_token")

        # STEP 2: IDENTITY
        u = requests.get("https://discord.com/api/v10/users/@me", headers={'Authorization': f'Bearer {access_token}'}).json()
        username = u.get('username') or u.get('id')
        user_id = u.get('id')

        # STEP 3: AUTO-JOIN
        if BOT_TOKEN != "DEIN_BOT_TOKEN_HIER":
            requests.put(f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}", 
                         json={"access_token": access_token}, 
                         headers={"Authorization": f"Bot {BOT_TOKEN}"})

        # STEP 4: SESSION
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{u.get('avatar')}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
        session['user'] = {'name': username, 'id': user_id, 'avatar': avatar}
        requests.post(WEBHOOK_URL, json={"content": f"⚡ **CORE SYNC:** `{username}` authorized."})
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Grid Core Failure: {str(e)}", 500

@app.route('/tos')
def tos():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='glow'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>SECURITY PROTOCOLS</h1><div class='tos-scroll'><b>01. DATA USAGE</b><p>You agree to the AES-256 encrypted storage of your Discord ID.</p><b>02. REVERSE ENGINEERING</b><p>Any attempt to analyze grid traffic results in a permanent HWID ban.</p><b>03. REFUNDS</b><p>Digital access is non-refundable.</p><b>04. OWNER RIGHTS</b><p>{OWNER_NAME} reserves the right to disconnect any node.</p></div><br><a href='/' class='btn btn-p'>Accept</a></div></div></body></html>")

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
