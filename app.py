from flask import Flask, request, render_template_string, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "INNO_PRO_ULTIMATE_SECRET_KEY"

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
# Dein bestehender Login-Webhook
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
# NEU: Dein Feedback-Webhook
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"

# --- CSS ---
CSS = """
<style>
    :root { --p: #5865F2; --s: #00d2ff; --bg: #030406; --g: rgba(255,255,255,0.05); }
    * { margin:0; padding:0; box-sizing:border-box; font-family: 'Poppins', sans-serif; }
    body { background: var(--bg); color: #fff; }
    .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
               background: radial-gradient(circle at 20% 30%, rgba(88,101,242,0.15), transparent),
                           radial-gradient(circle at 80% 70%, rgba(0,210,255,0.1), transparent); }
    nav { display: flex; justify-content: space-between; padding: 20px 5%; background: rgba(0,0,0,0.6); 
          backdrop-filter: blur(15px); border-bottom: 1px solid rgba(255,255,255,0.1); position: sticky; top: 0; z-index: 100; }
    .logo { font-weight: 800; font-size: 22px; color: var(--p); text-decoration: none; letter-spacing: 2px; }
    .nav-links a { color: #aaa; text-decoration: none; margin-left: 20px; font-size: 13px; font-weight: 600; }
    .hero { min-height: 85vh; display: flex; align-items: center; justify-content: center; padding: 40px 20px; }
    .card { background: var(--g); border: 1px solid rgba(255,255,255,0.1); padding: 50px; border-radius: 30px; 
            backdrop-filter: blur(25px); max-width: 800px; width: 100%; text-align: center; }
    h1 { font-size: clamp(30px, 5vw, 50px); font-weight: 900; margin-bottom: 20px; color: #fff; }
    .owner-badge { background: linear-gradient(45deg, #ffd700, #ff8c00); color: #000; padding: 5px 15px; 
                   border-radius: 20px; font-size: 12px; font-weight: 800; margin-bottom: 10px; display: inline-block; }
    .btn { padding: 14px 30px; border-radius: 12px; text-decoration: none; font-weight: 700; cursor: pointer; border: none; transition: 0.3s; display: inline-block; }
    .btn-p { background: var(--p); color: #fff; }
    .btn-f { background: rgba(255,255,255,0.1); color: #fff; margin-top: 20px; font-size: 12px; }
    .btn:hover { transform: translateY(-3px); opacity: 0.9; }
    textarea { width: 100%; background: rgba(0,0,0,0.3); border: 1px solid var(--p); border-radius: 10px; color: #fff; padding: 15px; margin-top: 15px; resize: none; }
    .avatar { width: 100px; height: 100px; border-radius: 50%; border: 3px solid var(--p); margin-bottom: 15px; }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO PRO</a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/tos">TOS</a>
            {"<a href='/dashboard'>Dashboard</a><a href='/logout' style='color:#ff4444;'>Logout</a>" if 'user' in session else "<a href='/login'>Login</a>"}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"<html><head>{CSS}</head><body><div class='bg-glow'></div>{get_nav()}<div class='hero'><div class='card'><h1>INNO PRO HUB</h1><p>Willkommen beim führenden Portal für Software-Innovation.</p><br><a href='/dashboard' class='btn btn-p'>JETZT STARTEN</a></div></div></body></html>")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="bg-glow"></div>{get_nav()}
    <div class="hero">
        <div class="card">
            {f'<div class="owner-badge">👑 SYSTEM OWNER</div>' if is_owner else ''}
            <img src="{user['avatar']}" class="avatar">
            <h1>Profil: {user['name']}</h1>
            <p style="color:#00ff88;">Status: {"ADMINISTRATOR" if is_owner else "PREMIUM USER"}</p>
            
            <form action="/send_feedback" method="POST">
                <textarea name="feedback" rows="3" placeholder="Dein Feedback an den Owner..."></textarea>
                <button type="submit" class="btn btn-p" style="width:100%; margin-top:10px;">FEEDBACK ABSENDEN</button>
            </form>
            
            <br><hr style="border:0; border-top:1px solid rgba(255,255,255,0.1);"><br>
            <a href="#" class="btn btn-f">DOWNLOAD TOOL V5.2</a>
        </div>
    </div>
    </body></html>
    """)

@app.route('/send_feedback', method=['POST'])
def send_feedback():
    if 'user' not in session: return redirect(url_for('home'))
    msg = request.form.get('feedback')
    if msg:
        requests.post(FEEDBACK_WEBHOOK, json={
            "embeds": [{
                "title": "📩 Neues User-Feedback",
                "description": msg,
                "color": 3447003,
                "footer": {"text": f"Von: {session['user']['name']} (ID: {session['user']['id']})"}
            }]
        })
    return redirect(url_for('dashboard'))

@app.route('/login')
def login():
    return redirect(f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    r = requests.post("https://discord.com/api/oauth2/token", data={
        'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
    }).json()
    token = r.get("access_token")
    u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
    
    avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
    session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
    
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **Login:** {u['username']}"})
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/tos')
def tos():
    return render_template_string(f"<html><head>{CSS}</head><body>{get_nav()}<div class='hero'><div class='card'><h1>TOS</h1><p>Keine Rückerstattung auf digitale Güter.</p></div></div></body></html>")

if __name__ == "__main__":
    app.run()
