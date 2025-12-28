from flask import Flask, request, render_template_string, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "INNO_PRO_ULTIMATE_SECRET_KEY" # Speichert die Session-Daten

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

# --- HIGH-END CSS ---
CSS = """
<style>
    :root { --p: #5865F2; --s: #00d2ff; --bg: #030406; --g: rgba(255,255,255,0.05); }
    * { margin:0; padding:0; box-sizing:border-box; font-family: 'Poppins', sans-serif; }
    body { background: var(--bg); color: #fff; overflow-x: hidden; }
    
    /* Hintergrund-Animation */
    .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
               background: radial-gradient(circle at 20% 30%, rgba(88,101,242,0.15), transparent),
                           radial-gradient(circle at 80% 70%, rgba(0,210,255,0.1), transparent); }

    nav { display: flex; justify-content: space-between; padding: 20px 5%; background: rgba(0,0,0,0.6); 
          backdrop-filter: blur(15px); border-bottom: 1px solid rgba(255,255,255,0.1); sticky: top; }
    .logo { font-weight: 800; font-size: 22px; letter-spacing: 3px; color: var(--p); text-shadow: 0 0 10px var(--p); }
    .nav-links a { color: #aaa; text-decoration: none; margin-left: 25px; font-size: 13px; font-weight: 600; transition: 0.3s; }
    .nav-links a:hover { color: #fff; text-shadow: 0 0 8px #fff; }

    .hero { height: 80vh; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px; }
    .card { background: var(--g); border: 1px solid rgba(255,255,255,0.1); padding: 50px; border-radius: 30px; 
            backdrop-filter: blur(25px); max-width: 800px; width: 100%; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
    
    h1 { font-size: 55px; font-weight: 900; line-height: 1.1; margin-bottom: 20px; 
         background: linear-gradient(to right, #fff, var(--p)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    p { color: #888; font-size: 17px; margin-bottom: 35px; }

    .btn { padding: 16px 45px; border-radius: 15px; text-decoration: none; font-weight: 700; font-size: 15px;
           transition: 0.4s; border: none; cursor: pointer; display: inline-block; }
    .btn-p { background: var(--p); color: #fff; box-shadow: 0 10px 25px rgba(88,101,242,0.4); }
    .btn-p:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(88,101,242,0.6); }

    .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 40px; }
    .stat-item { background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); }
    .stat-item h3 { color: var(--s); font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }
    .avatar { width: 100px; height: 100px; border-radius: 50%; border: 3px solid var(--p); margin-bottom: 20px; box-shadow: 0 0 20px var(--p); }
</style>
"""

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="bg-glow"></div>
    <nav><div class="logo">INNO PRO</div><div class="nav-links"><a href="/">HOME</a><a href="/tos">TOS</a></div></nav>
    <div class="hero">
        <div class="card">
            <h1>NEXT LEVEL MODDING</h1>
            <p>Das leistungsstärkste Portal für Software-Manipulation und Cloud-Verifizierung. Melde dich an, um dein Profil zu laden.</p>
            <a href="https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email" class="btn btn-p">DISCORD LOGIN</a>
        </div>
    </div>
    </body></html>
    """)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    user = session['user']
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="bg-glow"></div>
    <nav><div class="logo">INNO PRO</div><div class="nav-links"><a href="/logout">LOGOUT</a></div></nav>
    <div class="hero">
        <div class="card">
            <img src="{user['avatar']}" class="avatar">
            <h1>Willkommen, {user['name']}</h1>
            <p>Dein Account ist sicher verschlüsselt und verifiziert.</p>
            <div class="dashboard-grid">
                <div class="stat-item"><h3>Status</h3><div style="color:#00ff88; font-weight:bold;">PREMIUM</div></div>
                <div class="stat-item"><h3>User-ID</h3><div>{user['id']}</div></div>
                <div class="stat-item"><h3>Region</h3><div>DE</div></div>
            </div>
            <br><br>
            <a href="#" class="btn btn-p">TOOL DOWNLOADEN</a>
        </div>
    </div>
    </body></html>
    """)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Fehler", 400
    r = requests.post("https://discord.com/api/oauth2/token", data={
        'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
    }).json()
    token = r.get("access_token")
    u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
    
    # Speichert die Daten in der Session (Account-Daten merken)
    avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
    session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
    
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **Account gespeichert:** {u['username']}"})
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/tos')
def tos():
    return f"<html><head>{CSS}</head><body><div class='hero'><div class='card'><h1>TOS</h1><p>Daten werden sicher via Session-Cookie gespeichert.</p><a href='/' class='btn btn-p'>ZURÜCK</a></div></div></body></html>"

if __name__ == "__main__":
    app.run()
