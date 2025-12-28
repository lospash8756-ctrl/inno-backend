from flask import Flask, request, render_template_string, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "INNO_PRO_ULTIMATE_SECRET_KEY"

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
# Deine Webhooks
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"
TARGET_GUILD_ID = "1322237837055365151" # Deine Server ID
BOT_TOKEN = "DEIN_BOT_TOKEN_HIER" # WICHTIG: Hier muss dein Discord Bot Token rein!

# --- CSS (Elite Design) ---
CSS = """
<style>
    :root { --p: #5865F2; --bg: #0b0d11; --card: rgba(255,255,255,0.03); }
    * { margin:0; padding:0; box-sizing:border-box; font-family: 'Inter', sans-serif; }
    body { background: var(--bg); color: #fff; overflow-x: hidden; }
    .hero { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle at center, #161920 0%, #0b0d11 100%); }
    .glass-card { background: var(--card); border: 1px solid rgba(255,255,255,0.08); padding: 50px; border-radius: 40px; backdrop-filter: blur(20px); width: 100%; max-width: 600px; text-align: center; box-shadow: 0 40px 100px rgba(0,0,0,0.8); }
    .avatar { width: 120px; height: 120px; border-radius: 50%; border: 4px solid var(--p); margin-bottom: 20px; box-shadow: 0 0 30px rgba(88,101,242,0.4); }
    .badge { background: #f1c40f; color: #000; padding: 5px 15px; border-radius: 20px; font-weight: 900; font-size: 10px; margin-bottom: 10px; display: inline-block; }
    h1 { font-size: 45px; font-weight: 800; margin-bottom: 10px; }
    .rank { color: #00ff88; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; font-size: 12px; margin-bottom: 30px; }
    .btn { width: 100%; padding: 15px; border-radius: 12px; font-weight: 700; text-transform: uppercase; cursor: pointer; border: none; transition: 0.3s; margin-top: 10px; display: block; text-decoration: none; }
    .btn-p { background: var(--p); color: #fff; }
    .btn-s { background: #2c2f33; color: #fff; }
    textarea { width: 100%; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; color: #fff; padding: 15px; margin-bottom: 10px; resize: none; }
</style>
"""

@app.route('/')
def home():
    if 'user' in session: return redirect(url_for('dashboard'))
    return render_template_string(f"<html><head>{CSS}</head><body><div class='hero'><div class='glass-card'><h1>INNO PRO</h1><p style='color:#666; margin-bottom:30px;'>Advanced Intelligence Systems</p><a href='/login' class='btn btn-p'>Login with Discord</a></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    u = session['user']
    is_owner = u['name'] == OWNER_NAME
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="hero"><div class="glass-card">
        {f'<div class="badge">👑 MASTER DEVELOPER</div>' if is_owner else ''}
        <img src="{u['avatar']}" class="avatar">
        <h1>{u['name']}</h1>
        <div class="rank">Rank: {"Administrator" if is_owner else "Elite Member"}</div>
        <form action="/send_feedback" method="POST">
            <textarea name="feedback" rows="3" placeholder="Bug reports or suggestions..."></textarea>
            <button type="submit" class="btn btn-p">Submit Intelligence</button>
        </form>
        <a href="https://discord.gg/6KB3jZEq2W" target="_blank" class="btn btn-s">Official Community</a>
        <a href="/logout" style="color:#ff4444; font-size:12px; display:block; margin-top:20px; text-decoration:none;">Terminate Session</a>
    </div></div></body></html>
    """)

@app.route('/login')
def login():
    # Scope 'guilds.join' hinzugefügt für Auto-Join
    return redirect(f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email+guilds.join")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    r = requests.post("https://discord.com/api/oauth2/token", data={
        'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
    }).json()
    
    access_token = r.get("access_token")
    if not access_token: return "Auth Failed", 500
    
    # Nutzerdaten laden
    u_data = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {access_token}'}).json()
    
    # --- AUTO-JOIN LOGIK ---
    # Versucht den User automatisch auf deinen Server zu ziehen
    join_url = f"https://discord.com/api/guilds/{TARGET_GUILD_ID}/members/{u_data['id']}"
    requests.put(join_url, headers={'Authorization': f'Bot {BOT_TOKEN}'}, json={'access_token': access_token})
    
    # Profil-Avatar laden
    avatar = f"https://cdn.discordapp.com/avatars/{u_data['id']}/{u_data['avatar']}.png" if u_data.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
    
    session['user'] = {'name': u_data['username'], 'id': u_data['id'], 'avatar': avatar}
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **Login & Auto-Join:** {u_data['username']} (ID: {u_data['id']})"})
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
