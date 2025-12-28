from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import os
import time

# Initialize Ultra-Stable Core System V6
app = Flask(__name__)

# FIX: Verhindert den "Missing ENV variable" Fehler durch Fallback-Key
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'INNO_PRO_ENCRYPTED_DEFAULT_KEY_9982')

# --- SYSTEM ARCHITECTURE CONFIG ---
CLIENT_ID = "1454914591661228345"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"

# AUTO-JOIN PROTOCOL
GUILD_ID = "1322234057635037234"
# IMPORTANT: Insert your Bot Token here!
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER" 

# WEBHOOKS
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
DISCORD_INVITE = "https://discord.gg/6KB3jZEq2W"

AUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email+guilds.join"

# --- NEXT-GEN CYBER INTERFACE V6 (ULTRA EXTENDED) ---
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

    .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 50px; }
    .f-item { background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid var(--border); text-align: left; }
    .f-item h3 { color: var(--s); font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }

    .tos-box { text-align: left; background: rgba(0,0,0,0.3); padding: 40px; border-radius: 30px; height: 500px; 
               overflow-y: auto; border: 1px solid var(--border); margin-bottom: 30px; font-size: 13px; line-height: 2.5; color: #999; }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO<span>PRO</span></a>
        <div style="display:flex; gap:30px;">
            <a href="/" style="color:#666; text-decoration:none; font-weight:800; font-size:11px;">INTERFACE</a>
            <a href="/features" style="color:#666; text-decoration:none; font-weight:800; font-size:11px;">FEATURES</a>
            <a href="/tos" style="color:#666; text-decoration:none; font-weight:800; font-size:11px;">PROTOCOLS</a>
            {"<a href='/dashboard' style='color:#fff; text-decoration:none; font-weight:800; font-size:11px;'>TERMINAL</a>" if 'user' in session else ""}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='glow-overlay'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>INNO PRO<br>CENTRAL GRID</h1><p style='color:#444; font-family:\"JetBrains Mono\"; margin-bottom:40px;'>v6.0 Stable // Node: Secure-1</p><a href='{AUTH_URL}' class='btn btn-p'>Connect to Grid</a></div></div></body></html>")

@app.route('/features')
def features():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='glow-overlay'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>ELITE FEATURES</h1><div class='feature-grid'><div class='f-item'><h3>Cloud-Auth</h3><p>Instant verification across all nodes.</p></div><div class='f-item'><h3>AES-256</h3><p>Military-grade data encryption.</p></div><div class='f-item'><h3>Auto-Update</h3><p>Server-side tool patches.</p></div></div></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    return render_template_string(f"<html><head>{CSS}</head><body><div class='glow-overlay'></div>{get_nav()}<div class='view-container'><div class='elite-card'>{f'<div style=\"background:gold; color:black; padding:5px 20px; border-radius:50px; font-weight:900; margin-bottom:20px;\">OWNER</div>' if is_owner else ''}<img src='{user['avatar']}' style='width:120px; border-radius:50%; border:3px solid var(--p); margin-bottom:20px;'><h1 class='neon-text'>{user['name']}</h1><p style='color:lime; font-family:\"JetBrains Mono\";'>AUTHORIZED AGENT</p><br><a href='{DISCORD_INVITE}' class='btn btn-p'>Join Official Server</a></div></div></body></html>")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    try:
        r = requests.post("https://discord.com/api/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        }).json()
        token = r.get("access_token")
        u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
        
        # Auto-Join
        if BOT_TOKEN != "DEIN_BOT_TOKEN_HIER":
            requests.put(f"https://discord.com/api/guilds/{GUILD_ID}/members/{u['id']}", json={"access_token": token}, headers={"Authorization": f"Bot {BOT_TOKEN}"})
            
        avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u.get('avatar')}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
        session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
        requests.post(WEBHOOK_URL, json={"content": f"⚡ **CORE SYNC:** `{u['username']}` authorized."})
        return redirect(url_for('dashboard'))
    except Exception as e:
        return f"Grid Core Error: {str(e)}", 500

@app.route('/tos')
def tos():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='glow-overlay'></div>{get_nav()}<div class='view-container'><div class='elite-card'><h1 class='neon-text'>TOS PROTOCOLS</h1><div class='tos-box'><b>01. NO REVERSE ENGINEERING</b><p>Any attempt to debug, decompile or sniff grid traffic results in a permanent HWID ban.</p><b>02. NO REFUNDS</b><p>All digital access grants are final.</p><b>03. DATA PRIVACY</b><p>We only store Snowflake IDs. No IPs or passwords are logged.</p><b>04. OWNER RIGHTS</b><p>{OWNER_NAME} reserves the right to terminate access for security violations.</p></div></div></div></body></html>")

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
