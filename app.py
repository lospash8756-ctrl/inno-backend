from flask import Flask, request, render_template_string, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "INNO_PRO_ULTIMATE_SECRET_KEY"

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

# --- CSS (Design bleibt High-End) ---
CSS = """
<style>
    :root { --p: #5865F2; --s: #00d2ff; --bg: #030406; --g: rgba(255,255,255,0.05); }
    * { margin:0; padding:0; box-sizing:border-box; font-family: 'Poppins', sans-serif; }
    body { background: var(--bg); color: #fff; overflow-x: hidden; }
    .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
               background: radial-gradient(circle at 20% 30%, rgba(88,101,242,0.15), transparent),
                           radial-gradient(circle at 80% 70%, rgba(0,210,255,0.1), transparent); }
    nav { display: flex; justify-content: space-between; padding: 20px 5%; background: rgba(0,0,0,0.6); 
          backdrop-filter: blur(15px); border-bottom: 1px solid rgba(255,255,255,0.1); position: sticky; top: 0; z-index: 100; }
    .logo { font-weight: 800; font-size: 22px; letter-spacing: 3px; color: var(--p); text-shadow: 0 0 10px var(--p); text-decoration: none; }
    .nav-links a { color: #aaa; text-decoration: none; margin-left: 25px; font-size: 13px; font-weight: 600; transition: 0.3s; text-transform: uppercase; }
    .nav-links a:hover { color: #fff; text-shadow: 0 0 8px #fff; }
    .hero { height: 85vh; display: flex; align-items: center; justify-content: center; text-align: center; padding: 20px; }
    .card { background: var(--g); border: 1px solid rgba(255,255,255,0.1); padding: 50px; border-radius: 30px; 
            backdrop-filter: blur(25px); max-width: 800px; width: 100%; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
    h1 { font-size: clamp(30px, 5vw, 55px); font-weight: 900; line-height: 1.1; margin-bottom: 20px; 
         background: linear-gradient(to right, #fff, var(--p)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    p { color: #888; font-size: 17px; margin-bottom: 35px; }
    .btn { padding: 16px 45px; border-radius: 15px; text-decoration: none; font-weight: 700; font-size: 15px;
           transition: 0.4s; border: none; cursor: pointer; display: inline-block; }
    .btn-p { background: var(--p); color: #fff; box-shadow: 0 10px 25px rgba(88,101,242,0.4); }
    .btn-p:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(88,101,242,0.6); }
    .avatar { width: 100px; height: 100px; border-radius: 50%; border: 3px solid var(--p); margin-bottom: 20px; box-shadow: 0 0 20px var(--p); }
    .dashboard-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 40px; }
    .stat-item { background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); }
</style>
"""

def get_nav():
    login_link = "/dashboard" if 'user' in session else f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email"
    login_text = "DASHBOARD" if 'user' in session else "LOGIN"
    
    return f"""
    <nav>
        <a href="/" class="logo">INNO PRO</a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/tos">TOS</a>
            <a href="{login_link}">{login_text}</a>
            {"<a href='/logout' style='color:#ff4444;'>Logout</a>" if 'user' in session else ""}
        </div>
    </nav>
    """

@app.route('/')
def home():
    # Wenn eingeloggt, zeige einen anderen Button auf der Startseite
    if 'user' in session:
        btn_html = f'<a href="/dashboard" class="btn btn-p">ZURÜCK ZUM DASHBOARD</a>'
        subtitle = f"Willkommen zurück, {session['user']['name']}! Du bist bereits verifiziert."
    else:
        btn_html = f'<a href="https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email" class="btn btn-p">DISCORD LOGIN</a>'
        subtitle = "Das leistungsstärkste Portal für Software-Manipulation. Melde dich an, um dein Profil zu laden."

    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="bg-glow"></div>
    {get_nav()}
    <div class="hero">
        <div class="card">
            <h1>NEXT LEVEL MODDING</h1>
            <p>{subtitle}</p>
            {btn_html}
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
    {get_nav()}
    <div class="hero">
        <div class="card">
            <img src="{user['avatar']}" class="avatar">
            <h1>Profil: {user['name']}</h1>
            <p>Dein Account ist aktiv und mit der Cloud synchronisiert.</p>
            <div class="dashboard-grid">
                <div class="stat-item"><h3>Status</h3><div style="color:#00ff88; font-weight:bold;">PREMIUM</div></div>
                <div class="stat-item"><h3>User-ID</h3><div>{user['id']}</div></div>
                <div class="stat-item"><h3>Region</h3><div>GLOBAL</div></div>
            </div>
            <br><br>
            <a href="#" class="btn btn-p">DOWNLOAD PC-TOOL</a>
        </div>
    </div>
    </body></html>
    """)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    r = requests.post("https://discord.com/api/oauth2/token", data={
        'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
    }).json()
    
    token = r.get("access_token")
    if not token: return "Login Fehler", 500
    
    u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
    
    avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
    session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
    
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **Login:** {u['username']} ist jetzt online."})
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/tos')
def tos():
    return render_template_string(f"<html><head>{CSS}</head><body>{get_nav()}<div class='hero'><div class='card'><h1>TOS</h1><p>Nutzung nur für autorisierte User.</p><a href='/' class='btn btn-p'>ZURÜCK</a></div></div></body></html>")

if __name__ == "__main__":
    app.run()
