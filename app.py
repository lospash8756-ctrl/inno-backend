from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

# Das ultimative Gaming-Design (CSS)
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>INNO PRO | Portal</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #5865F2;
            --accent: #00d2ff;
            --bg: #050608;
            --glass: rgba(255, 255, 255, 0.03);
            --border: rgba(255, 255, 255, 0.1);
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: var(--bg);
            color: #fff;
            font-family: 'Poppins', sans-serif;
            overflow-x: hidden;
            background: radial-gradient(circle at top right, rgba(88, 101, 242, 0.15), transparent),
                        radial-gradient(circle at bottom left, rgba(0, 210, 255, 0.1), transparent);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        /* Navbar */
        nav {
            padding: 20px 50px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(15px);
            border-bottom: 1px solid var(--border);
            position: sticky; top: 0; z-index: 100;
        }
        .logo { font-weight: 800; font-size: 24px; letter-spacing: 2px; color: var(--primary); text-transform: uppercase; }
        .nav-links a {
            color: #aaa; text-decoration: none; margin-left: 30px; font-weight: 500;
            transition: 0.3s; font-size: 14px; text-transform: uppercase;
        }
        .nav-links a:hover { color: #fff; text-shadow: 0 0 10px var(--primary); }
        
        /* Hero Content */
        .container {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }
        .glass-card {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            padding: 60px;
            border-radius: 30px;
            text-align: center;
            max-width: 700px;
            width: 100%;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
            animation: fadeIn 1s ease-out;
        }
        h1 { font-size: 50px; font-weight: 800; margin-bottom: 20px; background: linear-gradient(90deg, #fff, var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        p { color: #888; line-height: 1.8; margin-bottom: 40px; font-size: 16px; }
        
        /* Buttons */
        .btn {
            padding: 15px 40px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            transition: 0.4s;
            display: inline-block;
            border: none;
            cursor: pointer;
        }
        .btn-primary {
            background: var(--primary);
            color: #fff;
            box-shadow: 0 10px 20px rgba(88, 101, 242, 0.3);
        }
        .btn-primary:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(88, 101, 242, 0.5);
            background: #4752C4;
        }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <nav>
        <div class="logo">INNO PRO</div>
        <div class="nav-links">
            <a href="/">Home</a>
            <a href="/tos">TOS</a>
            <a href="https://discord.com/api/oauth2/authorize?client_id={{ client_id }}&redirect_uri={{ redirect_uri }}&response_type=code&scope=identify+guilds+email">Anmelden</a>
        </div>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <div class="glass-card">
        <h1>Next-Gen Modding</h1>
        <p>Willkommen beim INNO PRO Web-Portal. Verifiziere deinen Account, um Zugriff auf exklusive Mod-Features, High-Speed Downloads und unser Community-Dashboard zu erhalten.</p>
        <a href="https://discord.com/api/oauth2/authorize?client_id=1454916135790186537&redirect_uri=https://inno-backend-1.onrender.com/callback&response_type=code&scope=identify+guilds+email" class="btn btn-primary">Jetzt mit Discord anmelden</a>
    </div>
    """
    return render_template_string(BASE_LAYOUT, content=content)

@app.route('/tos')
def tos():
    content = """
    <div class="glass-card" style="text-align: left;">
        <h1>Terms of Service</h1>
        <p>Durch die Nutzung von INNO PRO akzeptierst du folgende Bedingungen:</p>
        <ul style="color: #888; margin-bottom: 30px; list-style-position: inside;">
            <li>Keine missbräuchliche Nutzung der API</li>
            <li>Daten werden nur zur Verifizierung verwendet</li>
            <li>Mod-Downloads erfolgen auf eigene Gefahr</li>
        </ul>
        <a href="/" class="btn btn-primary">Zurück zur Übersicht</a>
    </div>
    """
    return render_template_string(BASE_LAYOUT, content=content)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Fehler: Kein Code", 400
    try:
        # Token & User Logik
        r = requests.post("https://discord.com/api/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        })
        token = r.json().get("access_token")
        u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
        
        # Webhook Alert
        requests.post(WEBHOOK_URL, json={"content": f"🚀 **Web-Login:** {u.get('username')} hat sich verifiziert!"})
        
        content = f"""
        <div class="glass-card">
            <h1 style="color: #00ff88;">✓ Verifiziert</h1>
            <p>Willkommen zurück, <strong>{u.get('username')}</strong>! Dein Account wurde erfolgreich verknüpft.</p>
            <p>Du kannst dieses Fenster jetzt schließen und zum Inno Pro Tool zurückkehren.</p>
            <a href="/" class="btn btn-primary">Dashboard öffnen</a>
        </div>
        """
        return render_template_string(BASE_LAYOUT, content=content)
    except Exception as e:
        return f"Fehler: {str(e)}", 500

if __name__ == "__main__":
    app.run()
