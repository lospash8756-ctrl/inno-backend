from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import os
import json

# --- CORE INITIALIZATION ---
app = Flask(__name__)
# Fixes the ENV error by providing a stable fallback key
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'INNO_PRO_ULTIMATE_CORE_V8_ENCRYPTED')

# --- ELITE SYSTEM CONFIGURATION ---
CLIENT_ID = "1454914591661228345"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"

# AUTO-JOIN PROTOCOL
GUILD_ID = "1322234057635037234"
# MANDATORY: Insert your Bot Token here to enable automatic server entry
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER" 

# ANALYTICS & FEEDBACK WEBHOOKS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

# FULL SCOPE AUTH URL (Includes identify, email, guilds, and join permissions)
AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- NEXT-GEN CYBER INTERFACE (V8 EXTENDED) ---
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

    .tos-grid { text-align: left; background: rgba(0,0,0,0.3); padding: 40px; border-radius: 30px; height: 500px; 
                overflow-y: auto; border: 1px solid var(--border); margin-bottom: 30px; font-size: 13px; line-height: 2.2; color: #888; }
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
    return render_template_string(f"<html><head><title>INNO PRO | Global Portal</title>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>INNO PRO<br>SYSTEM CORE</h1><p style='color:#444; font-family:\"JetBrains Mono\"; margin-bottom:40px;'>Centralized Security Interface v8.0 // Optimized Build</p><a href='{AUTH_URL}' class='btn btn-p'>Authorize Profile</a></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    return render_template_string(f"<html><head><title>Terminal | {user['name']}</title>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}<div class='view-container'><div class='elite-card'>{f'<div style=\"background:var(--p); color:white; padding:5px 20px; border-radius:50px; font-weight:900; margin-bottom:20px;\">MASTER DEVELOPER</div>' if is_owner else ''}<img src='{user['avatar']}' style='width:130px; border-radius:50%; border:3px solid var(--p); margin-bottom:25px;'><h1 class='neon-text'>{user['name']}</h1><p style='color:lime; font-family:\"JetBrains Mono\";'>ACCESS GRANTED</p><br><a href='{DISCORD_INVITE}' class='btn btn-p'>Official Discord</a></div></div></body></html>")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    try:
        # TOKEN EXCHANGE - Fixed URL and Error Handling
        r = requests.post("https://discord.com/api/v10/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        # Check if Discord sent valid JSON
        try:
            token_data = r.json()
        except Exception:
            return f"Grid Core Failure: Discord sent non-JSON response. Status: {r.status_code}", 500

        access_token = token_data.get("access_token")
        if not access_token: return f"Grid Handshake Failure: {token_data.get('error_description', 'Unknown Error')}", 500

        # Identity Extraction
        u = requests.get("https://discord.com/api/v10/users/@me", headers={'Authorization': f'Bearer {access_token}'}).json()
        username = u.get('username') or u.get('global_name') or u.get('id') or "Unknown_Agent"
        user_id = u.get('id')

        # Auto-Join Protocol
        if BOT_TOKEN != "DEIN_BOT_TOKEN_HIER":
            requests.put(f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{user_id}", 
                         json={"access_token": access_token}, 
                         headers={"Authorization": f"Bot {BOT_TOKEN}"})

        # Save Session
        avatar_hash = u.get('avatar')
        avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png" if avatar_hash else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
        session['user'] = {'name': username, 'id': user_id, 'avatar': avatar}
        
        requests.post(WEBHOOK_URL, json={"content": f"⚡ **CORE SYNC:** `{username}` authorized."})
        return redirect(url_for('dashboard'))

    except Exception as e:
        return f"Grid Core failure: {str(e)}", 500

@app.route('/tos')
def tos():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='glow-layer'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>SECURITY PROTOCOLS</h1><div class='tos-grid'><b>01. USAGE</b><p>You agree to encrypted data collection.</p><b>02. BANS</b><p>Reverse engineering results in a permanent ban.</p></div><br><a href='/' class='btn btn-p'>Accept</a></div></div></body></html>")

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
