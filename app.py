from flask import Flask, request, render_template_string, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "INNO_PRO_ULTIMATE_SECRET_KEY"

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"
FEEDBACK_WEBHOOK = "https://discord.com/api/webhooks/1454940586778824926/j2DBfayK0sb0F3rnTSNH0c0yQvhU7hUP-8JavOjP8_VPRqIY-69Ag9LOFpdco-WlmsMz"

OWNER_NAME = "daring_hare_98117"

# --- MODERN ENGLISH CSS ---
CSS = """
<style>
    :root { --p: #5865F2; --s: #00d2ff; --bg: #030406; --g: rgba(255,255,255,0.05); }
    * { margin:0; padding:0; box-sizing:border-box; font-family: 'Poppins', sans-serif; }
    body { background: var(--bg); color: #fff; line-height: 1.6; }
    .bg-glow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
               background: radial-gradient(circle at 20% 30%, rgba(88,101,242,0.15), transparent),
                           radial-gradient(circle at 80% 70%, rgba(0,210,255,0.1), transparent); }
    nav { display: flex; justify-content: space-between; padding: 20px 5%; background: rgba(0,0,0,0.6); 
          backdrop-filter: blur(15px); border-bottom: 1px solid rgba(255,255,255,0.1); position: sticky; top: 0; z-index: 100; }
    .logo { font-weight: 800; font-size: 22px; color: var(--p); text-decoration: none; letter-spacing: 2px; }
    .nav-links a { color: #aaa; text-decoration: none; margin-left: 20px; font-size: 13px; font-weight: 600; text-transform: uppercase; transition: 0.3s; }
    .nav-links a:hover { color: var(--p); }
    .hero { min-height: 85vh; display: flex; align-items: center; justify-content: center; padding: 60px 20px; }
    .card { background: var(--g); border: 1px solid rgba(255,255,255,0.1); padding: 50px; border-radius: 30px; 
            backdrop-filter: blur(25px); max-width: 900px; width: 100%; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
    h1 { font-size: clamp(30px, 5vw, 55px); font-weight: 900; margin-bottom: 20px; color: #fff; letter-spacing: -1px; }
    .btn { padding: 14px 35px; border-radius: 12px; text-decoration: none; font-weight: 700; cursor: pointer; border: none; transition: 0.3s; display: inline-block; }
    .btn-p { background: var(--p); color: #fff; box-shadow: 0 5px 15px rgba(88,101,242,0.3); }
    .btn-p:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(88,101,242,0.5); }
    .tos-text { text-align: left; color: #bbb; font-size: 14px; max-height: 400px; overflow-y: auto; padding-right: 10px; margin-bottom: 20px; }
    .tos-text b { color: var(--s); }
    .avatar { width: 110px; height: 110px; border-radius: 50%; border: 3px solid var(--p); margin-bottom: 15px; }
    textarea { width: 100%; background: rgba(0,0,0,0.4); border: 1px solid var(--p); border-radius: 12px; color: #fff; padding: 15px; margin-top: 15px; resize: none; }
    .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }
    .feature-item { background: rgba(255,255,255,0.03); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); text-align: left; }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO PRO</a>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/features">Features</a>
            <a href="/tos">TOS</a>
            {"<a href='/dashboard'>Dashboard</a><a href='/logout' style='color:#ff4444;'>Logout</a>" if 'user' in session else "<a href='/login'>Login</a>"}
        </div>
    </nav>
    """

@app.route('/')
def home():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class='bg-glow'></div>{get_nav()}
    <div class='hero'><div class='card'>
        <h1>NEXT-GEN SOFTWARE SOLUTIONS</h1>
        <p style='color:#888; font-size:18px;'>Unlock the true potential of your system with INNO PRO's advanced cloud-integrated technology.</p>
        <br>
        <div class='feature-grid'>
            <div class='feature-item'><h3>Cloud-Auth</h3><p>Secure 24/7 verification via Discord.</p></div>
            <div class='feature-item'><h3>High-Speed</h3><p>Optimized servers for instant downloads.</p></div>
        </div>
        <br><br>
        <a href='/dashboard' class='btn btn-p'>GET STARTED NOW</a>
    </div></div></body></html>
    """)

@app.route('/features')
def features():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class='bg-glow'></div>{get_nav()}
    <div class='hero'><div class='card'>
        <h1>CORE FEATURES</h1>
        <div class='feature-grid'>
            <div class='feature-item'><h3>Injection Engine</h3><p>Undetected and seamless software integration for various environments.</p></div>
            <div class='feature-item'><h3>Auto-Update</h3><p>Your local client stays updated with our cloud repository automatically.</p></div>
            <div class='feature-item'><h3>Global CDN</h3><p>Fastest delivery of tools and resources worldwide.</p></div>
            <div class='feature-item'><h3>Secure Sessions</h3><p>Encrypted user sessions ensure your data remains private.</p></div>
        </div>
        <br><br>
        <a href='/' class='btn btn-p'>BACK TO HOME</a>
    </div></div></body></html>
    """)

@app.route('/tos')
def tos():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class='bg-glow'></div>{get_nav()}
    <div class='hero'><div class='card'>
        <h1>TERMS OF SERVICE</h1>
        <div class='tos-text'>
            <p><b>1. Acceptance of Terms:</b> By accessing INNO PRO, you agree to be bound by these strict regulations. Violation results in a permanent ban.</p><br>
            <p><b>2. License Usage:</b> Software licenses are granted to a single user. Sharing accounts or bypassing HWID locks is strictly prohibited.</p><br>
            <p><b>3. Prohibited Activities:</b> You may not attempt to reverse-engineer, decompile, or debug any part of the INNO PRO infrastructure.</p><br>
            <p><b>4. Data Protection:</b> We only store your Discord ID and username for authentication. No third-party data is collected.</p><br>
            <p><b>5. No Refunds:</b> Due to the nature of digital goods, all transactions and access grants are final.</p><br>
            <p><b>6. Termination:</b> {OWNER_NAME} reserves the right to terminate access at any time for security reasons.</p><br>
            <p><b>7. Liability:</b> Use our tools at your own risk. We are not responsible for any damage or bans on third-party platforms.</p>
        </div>
        <a href='/' class='btn btn-p'>I ACCEPT & UNDERSTAND</a>
    </div></div></body></html>
    """)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="bg-glow"></div>{get_nav()}
    <div class="hero">
        <div class="card">
            {f'<div class="owner-badge" style="background:linear-gradient(45deg,#00d2ff,#5865f2); color:#fff;">🛡️ SYSTEM OWNER</div>' if is_owner else ''}
            <img src="{user['avatar']}" class="avatar">
            <h1>Welcome, {user['name']}</h1>
            <p style="color:#00ff88; font-weight:bold;">Status: {"ADMINISTRATOR" if is_owner else "PREMIUM USER"}</p>
            
            <form action="/send_feedback" method="POST">
                <textarea name="feedback" rows="3" placeholder="Send feedback or bug reports to {OWNER_NAME}..."></textarea>
                <button type="submit" class="btn btn-p" style="width:100%; margin-top:10px;">SUBMIT FEEDBACK</button>
            </form>
            <br><hr style="border:0; border-top:1px solid rgba(255,255,255,0.1);"><br>
            <a href="#" class="btn btn-p" style="background: rgba(255,255,255,0.1);">DOWNLOAD CLIENT V5.2</a>
        </div>
    </div>
    </body></html>
    """)

@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    if 'user' not in session: return redirect(url_for('home'))
    msg = request.form.get('feedback')
    if msg:
        requests.post(FEEDBACK_WEBHOOK, json={
            "embeds": [{
                "title": "📩 New Feedback Received",
                "description": msg,
                "color": 3447003,
                "footer": {"text": f"User: {session['user']['name']} (ID: {session['user']['id']})"}
            }]
        })
    return redirect(url_for('dashboard'))

@app.route('/login')
def login():
    return redirect(f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return redirect(url_for('home'))
    
    token_response = requests.post("https://discord.com/api/oauth2/token", data={
        'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
    }).json()
    
    token = token_response.get("access_token")
    if not token: return "Authentication Failed", 500
    
    u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
    avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
    session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
    
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **Login Event:** {u['username']} has logged in."})
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
