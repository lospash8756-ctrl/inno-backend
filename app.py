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
DISCORD_INVITE = "https://discord.gg/DqqXvG45gM"

# --- ELITE CYBER CSS ---
CSS = """
<style>
    :root { --p: #5865F2; --s: #00d2ff; --bg: #020203; --card: rgba(255,255,255,0.03); --border: rgba(255,255,255,0.08); }
    * { margin:0; padding:0; box-sizing:border-box; font-family: 'Inter', 'Poppins', sans-serif; }
    body { background: var(--bg); color: #fff; line-height: 1.6; overflow-x: hidden; }
    
    .bg-animation { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; 
                    background: radial-gradient(circle at 10% 20%, rgba(88,101,242,0.1), transparent),
                                radial-gradient(circle at 90% 80%, rgba(0,210,255,0.08), transparent); }

    nav { display: flex; justify-content: space-between; padding: 25px 8%; background: rgba(0,0,0,0.7); 
          backdrop-filter: blur(20px); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 900; font-size: 24px; color: #fff; text-decoration: none; letter-spacing: 4px; }
    .logo span { color: var(--p); }
    .nav-links a { color: #888; text-decoration: none; margin-left: 30px; font-size: 12px; font-weight: 700; text-transform: uppercase; transition: 0.3s; }
    .nav-links a:hover, .nav-links a.active { color: #fff; text-shadow: 0 0 15px var(--p); }

    .container { min-height: 90vh; display: flex; align-items: center; justify-content: center; padding: 80px 20px; }
    .glass-box { background: var(--card); border: 1px solid var(--border); padding: 60px; border-radius: 40px; 
                 backdrop-filter: blur(40px); max-width: 1000px; width: 100%; box-shadow: 0 30px 60px rgba(0,0,0,0.8); animation: slideIn 0.8s ease; }
    
    @keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    h1 { font-size: clamp(35px, 6vw, 65px); font-weight: 900; margin-bottom: 25px; letter-spacing: -2px; line-height: 1; }
    .gradient-text { background: linear-gradient(90deg, #fff, var(--p), var(--s)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .btn { padding: 18px 40px; border-radius: 15px; text-decoration: none; font-weight: 800; font-size: 14px; transition: 0.4s; display: inline-block; text-transform: uppercase; border: none; cursor: pointer; }
    .btn-main { background: var(--p); color: #fff; box-shadow: 0 10px 30px rgba(88,101,242,0.3); }
    .btn-main:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(88,101,242,0.5); }
    .btn-discord { background: #2c2f33; color: #fff; margin-left: 15px; border: 1px solid #444; }
    .btn-discord:hover { background: #3c4046; }

    .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin-top: 50px; text-align: left; }
    .f-card { background: rgba(255,255,255,0.02); padding: 30px; border-radius: 25px; border: 1px solid var(--border); transition: 0.3s; }
    .f-card:hover { border-color: var(--p); background: rgba(88,101,242,0.03); }
    .f-card i { color: var(--p); font-size: 24px; margin-bottom: 15px; display: block; }
    .f-card h3 { font-size: 18px; margin-bottom: 10px; color: #fff; }
    .f-card p { color: #777; font-size: 14px; }

    .tos-scroll { text-align: left; background: rgba(0,0,0,0.2); padding: 30px; border-radius: 20px; height: 450px; overflow-y: auto; border: 1px solid var(--border); margin-bottom: 30px; }
    .tos-scroll h4 { color: var(--p); margin: 20px 0 10px 0; text-transform: uppercase; font-size: 13px; }
    .tos-scroll p { font-size: 13px; color: #aaa; margin-bottom: 10px; }

    .avatar-img { width: 120px; height: 120px; border-radius: 50%; border: 4px solid var(--p); margin-bottom: 20px; box-shadow: 0 0 30px rgba(88,101,242,0.4); }
</style>
"""

def get_nav():
    return f"""
    <nav>
        <a href="/" class="logo">INNO<span>PRO</span></a>
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
    <html><head>{CSS}</head><body><div class='bg-animation'></div>{get_nav()}
    <div class='container'><div class='glass-box'>
        <h1 class='gradient-text'>EVOLVE YOUR SOFTWARE</h1>
        <p style='color:#666; font-size:20px; max-width:700px; margin: 0 auto 40px auto;'>The most advanced cloud-based authentication and injection system. Built for speed, security, and the elite modding community.</p>
        <div style='display:flex; justify-content:center; gap:15px;'>
            <a href='/login' class='btn btn-main'>Get Access Now</a>
            <a href='{DISCORD_INVITE}' target='_blank' class='btn btn-discord'>Join Discord</a>
        </div>
    </div></div></body></html>
    """)

@app.route('/features')
def features():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class='bg-animation'></div>{get_nav()}
    <div class='container'><div class='glass-box'>
        <h1 class='gradient-text'>ELITE FEATURES</h1>
        <div class='feature-grid'>
            <div class='f-card'><h3>Hyper-Injection</h3><p>Proprietary kernel-level injection methods for maximum compatibility and stealth.</p></div>
            <div class='f-card'><h3>Cloud-Sync</h3><p>Your settings and mods follow you anywhere. No local files required.</p></div>
            <div class='f-card'><h3>HWID Protection</h3><p>Advanced hardware-id locking system to prevent unauthorized account sharing.</p></div>
            <div class='f-card'><h3>Insta-Update</h3><p>Server-side patches are applied instantly without requiring a new client download.</p></div>
            <div class='f-card'><h3>Encrypted Traffic</h3><p>All communication between client and server is secured with AES-256 encryption.</p></div>
            <div class='f-card'><h3>24/7 Support</h3><p>Direct access to the developer team via our verified Discord community.</p></div>
        </div>
    </div></div></body></html>
    """)

@app.route('/tos')
def tos():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class='bg-animation'></div>{get_nav()}
    <div class='container'><div class='glass-box'>
        <h1 class='gradient-text'>TERMS OF SERVICE</h1>
        <div class='tos-scroll'>
            <h4>1. Acceptance of Agreement</h4><p>By using INNO PRO, you enter a legally binding agreement with the administration. Any attempt to bypass security measures is a breach of contract.</p>
            <h4>2. Strict HWID Policy</h4><p>Licenses are locked to one machine. Resetting your HWID is only possible via manual staff review. Sharing your account will result in an instant, non-appealable ban.</p>
            <h4>3. Anti-Debug Measures</h4><p>Running our software alongside debuggers, sniffers, or disassemblers (x64dbg, IDA, Wireshark) is strictly prohibited. Our system will auto-ban any user detected doing so.</p>
            <h4>4. Zero Refund Policy</h4><p>All digital purchases and access rights are final. No refunds will be issued under any circumstances, including service termination or bans.</p>
            <h4>5. Account Security</h4><p>You are responsible for your own credentials. INNO PRO is not liable for accounts lost due to poor user security.</p>
            <h4>6. Third-Party Risks</h4><p>We provide tools "as-is". We are not responsible for any bans or damages on third-party gaming platforms or software environments.</p>
            <h4>7. Ownership</h4><p>All software remains the intellectual property of {OWNER_NAME}. Unauthorized redistribution is a violation of international copyright laws.</p>
        </div>
        <a href='/login' class='btn btn-main'>Accept & Proceed</a>
    </div></div></body></html>
    """)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('home'))
    user = session['user']
    is_owner = user['name'] == OWNER_NAME
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="bg-animation"></div>{get_nav()}
    <div class="container"><div class="glass-box">
        {f'<div style="background:linear-gradient(90deg,#ffd700,#ffa500); color:#000; padding:8px 20px; border-radius:50px; font-weight:900; display:inline-block; margin-bottom:20px;">👑 MASTER DEVELOPER</div>' if is_owner else ''}
        <img src="{user['avatar']}" class="avatar-img">
        <h1 class="gradient-text">{user['name']}</h1>
        <p style="color:#00ff88; font-weight:bold; text-transform:uppercase; letter-spacing:2px;">Rank: {"Administrator" if is_owner else "Elite Member"}</p>
        
        <form action="/send_feedback" method="POST" style="margin-top:30px;">
            <textarea name="feedback" rows="3" placeholder="Bug reports or suggestions directly to {OWNER_NAME}..." style="width:100%; background:rgba(0,0,0,0.5); border:1px solid var(--border); border-radius:15px; color:#fff; padding:20px; resize:none; margin-bottom:15px;"></textarea>
            <button type="submit" class="btn btn-main" style="width:100%;">Submit Intelligence</button>
        </form>
        <br><a href="{DISCORD_INVITE}" class="btn btn-discord" style="margin-left:0; width:100%; margin-top:10px;">Official Community</a>
    </div></div></body></html>
    """)

@app.route('/send_feedback', methods=['POST'])
def send_feedback():
    if 'user' not in session: return redirect(url_for('home'))
    msg = request.form.get('feedback')
    if msg: requests.post(FEEDBACK_WEBHOOK, json={"embeds": [{"title": "📩 INNO INTEL RECEIVED", "description": msg, "color": 5793266, "footer": {"text": f"Agent: {session['user']['name']}"}}]})
    return redirect(url_for('dashboard'))

@app.route('/login')
def login(): return redirect(f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify+guilds+email")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    r = requests.post("https://discord.com/api/oauth2/token", data={'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI}).json()
    token = r.get("access_token")
    u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
    avatar = f"https://cdn.discordapp.com/avatars/{u['id']}/{u['avatar']}.png" if u.get('avatar') else "https://discord.com/assets/6debd47ed1340548d9d098641527c088.png"
    session['user'] = {'name': u['username'], 'id': u['id'], 'avatar': avatar}
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **Login Event:** `{u['username']}` connected to the grid."})
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout(): session.clear(); return redirect(url_for('home'))

if __name__ == "__main__": app.run()
