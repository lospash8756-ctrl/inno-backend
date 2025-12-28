from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# --- CONFIG ---
CLIENT_ID = "1454916135790186537"
CLIENT_SECRET = "GlRx9w2sYUzBqo2eFcMLOK347NQSpdAM"
REDIRECT_URI = "https://inno-backend-1.onrender.com/callback"
WEBHOOK_URL = "https://discord.com/api/webhooks/1454890126135001250/gg-LC0F5yHmMwOngEtbtL_VdeDL9hikNMOzej16FhpQWWoBReX600ojnuQ_oe8YCRGQ9"

# Hochwertiges Gaming-Design (HTML + CSS)
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>INNO PRO | Portal</title>
    <style>
        :root {
            --primary: #5865F2;
            --bg: #0b0c10;
            --surface: #1f2833;
            --accent: #66fcf1;
            --text: #c5c6c7;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        header {
            background: rgba(31, 40, 51, 0.95);
            padding: 1rem 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid var(--primary);
            position: sticky; top: 0; z-index: 1000;
        }
        .logo { font-size: 1.5rem; font-weight: bold; color: var(--primary); letter-spacing: 2px; }
        nav a {
            color: var(--text);
            text-decoration: none;
            margin-left: 2rem;
            font-weight: 500;
            transition: 0.3s;
            text-transform: uppercase;
            font-size: 0.9rem;
        }
        nav a:hover { color: var(--primary); }
        .hero {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            background: radial-gradient(circle at center, #1f2833 0%, #0b0c10 100%);
        }
        .main-card {
            background: var(--surface);
            padding: 3rem;
            border-radius: 15px;
            text-align: center;
            max-width: 800px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid rgba(88, 101, 242, 0.2);
        }
        h1 { font-size: 3rem; color: #fff; margin-bottom: 1rem; }
        p { line-height: 1.6; margin-bottom: 2.5rem; color: #9da5b1; font-size: 1.1rem; }
        .btn {
            background: var(--primary);
            color: white;
            padding: 1rem 2.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            display: inline-block;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(88, 101, 242, 0.4);
        }
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(88, 101, 242, 0.6);
            background: #4752C4;
        }
        footer { padding: 1rem; text-align: center; font-size: 0.8rem; color: #45a29e; }
    </style>
</head>
<body>
    <header>
        <div class="logo">INNO PRO</div>
        <nav>
            <a href="/">Home</a>
            <a href="/tos">TOS</a>
            <a href="https://discord.com/oauth2/authorize?client_id=1454916135790186537&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email">Anmelden</a>
        </nav>
    </header>
    <div class="hero">
        {% block content %}{% endblock %}
    </div>
    <footer>&copy; 2025 INNO PRO - Next Gen Modding Solutions</footer>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <div class="main-card">
        <h1>POWERED BY INNO</h1>
        <p>Willkommen im offiziellen INNO PRO Hub. Verifiziere deinen Account, um uneingeschränkten Zugriff auf unsere Modding-Tools, High-Speed Cloud-Downloads und exklusive Community-Features zu erhalten.</p>
        <a href="https://discord.com/oauth2/authorize?client_id=1454916135790186537&response_type=code&redirect_uri=https%3A%2F%2Finno-backend-1.onrender.com%2Fcallback&scope=identify+guilds+email" class="btn">JETZT VERIFIZIEREN</a>
    </div>
    """
    return render_template_string(BASE_LAYOUT, content=content)

@app.route('/tos')
def tos():
    content = """
    <div class="main-card" style="text-align: left;">
        <h1 style="text-align: center;">Nutzungsbedingungen</h1>
        <p>Mit der Anmeldung bei INNO PRO akzeptierst du folgende Bedingungen:</p>
        <ul style="color: #9da5b1; margin-bottom: 2rem; line-height: 2;">
            <li>Die Nutzung der Tools erfolgt auf eigene Gefahr.</li>
            <li>Wir speichern keine Passwörter, nur deine Discord-ID zur Verifizierung.</li>
            <li>Missbrauch der Download-Server führt zum permanenten Ausschluss.</li>
        </ul>
        <div style="text-align: center;">
            <a href="/" class="btn">ZURÜCK ZUR STARTSEITE</a>
        </div>
    </div>
    """
    return render_template_string(BASE_LAYOUT, content=content)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "Fehler: Kein Autorisierungscode erhalten.", 400
    try:
        # Token-Austausch
        r = requests.post("https://discord.com/api/oauth2/token", data={
            'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI
        })
        token = r.json().get("access_token")
        # User-Info holen
        u = requests.get("https://discord.com/api/users/@me", headers={'Authorization': f'Bearer {token}'}).json()
        
        # Webhook senden
        requests.post(WEBHOOK_URL, json={"content": f"🚀 **Login erfolgreich:** {u.get('username')} hat das Web-Portal betreten!"})
        
        content = f"""
        <div class="main-card">
            <h1 style="color: #00ff88;">AUTORISIERT</h1>
            <p>Willkommen, <strong>{u.get('username')}</strong>! Dein Account wurde erfolgreich verifiziert.</p>
            <p>Du kannst dieses Tab jetzt schließen und direkt in dein INNO PRO PC-Tool zurückkehren.</p>
            <a href="/" class="btn" style="background: #45a29e;">ZUM DASHBOARD</a>
        </div>
        """
        return render_template_string(BASE_LAYOUT, content=content)
    except Exception as e:
        return f"Interner Fehler beim Callback: {str(e)}", 500

if __name__ == "__main__":
    app.run()
