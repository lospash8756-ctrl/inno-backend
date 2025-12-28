import os
import secrets
import logging
from flask import Flask, request, session, redirect, url_for, render_template_string, abort
import requests

# -------------------------------------------------
# BASIC HARDENING
# -------------------------------------------------
logging.basicConfig(level=logging.INFO)

def env(key, required=True):
    value = os.getenv(key)
    if required and not value:
        raise RuntimeError(f"Missing ENV variable: {key}")
    return value

# -------------------------------------------------
# APP INIT
# -------------------------------------------------
app = Flask(__name__)
app.secret_key = env("FLASK_SECRET_KEY")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=True
)

# -------------------------------------------------
# DISCORD CONFIG
# -------------------------------------------------
CLIENT_ID = env("DISCORD_CLIENT_ID")
CLIENT_SECRET = env("DISCORD_CLIENT_SECRET")
REDIRECT_URI = env("DISCORD_REDIRECT_URI")
BOT_TOKEN = env("DISCORD_BOT_TOKEN")

GUILD_ID = "1322234057635037234"
OWNER_NAME = "daring_hare_98117"

WEBHOOK_URL = env("WEBHOOK_URL")
FEEDBACK_WEBHOOK = env("FEEDBACK_WEBHOOK")

OAUTH_SCOPE = "identify email guilds guilds.join"
DISCORD_API = "https://discord.com/api"

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def discord_headers(token):
    return {"Authorization": f"Bearer {token}"}

def bot_headers():
    return {"Authorization": f"Bot {BOT_TOKEN}"}

def safe_request(method, url, **kwargs):
    kwargs.setdefault("timeout", 10)
    r = requests.request(method, url, **kwargs)
    if r.status_code >= 400:
        logging.error(f"Discord API error {r.status_code}: {r.text}")
    return r

def generate_state():
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state
    return state

# -------------------------------------------------
# AUTH URL
# -------------------------------------------------
def auth_url():
    return (
        f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={OAUTH_SCOPE}"
        f"&state={generate_state()}"
    )

# -------------------------------------------------
# ROUTES
# -------------------------------------------------
@app.route("/")
def home():
    return render_template_string("""
    <h1>INNO PRO</h1>
    <a href="{{ url }}">Authorize</a>
    """, url=auth_url())

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")

    if not code or state != session.pop("oauth_state", None):
        abort(403)

    # TOKEN EXCHANGE
    token_res = safe_request(
        "POST",
        f"{DISCORD_API}/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    ).json()

    access_token = token_res.get("access_token")
    if not access_token:
        abort(500)

    # USER FETCH
    user_res = safe_request(
        "GET",
        f"{DISCORD_API}/users/@me",
        headers=discord_headers(access_token)
    )

    if user_res.status_code != 200:
        abort(500)

    u = user_res.json()

    user_id = u["id"]
    username = u.get("global_name") or u["username"]

    avatar = (
        f"https://cdn.discordapp.com/avatars/{user_id}/{u['avatar']}.png"
        if u.get("avatar")
        else "https://cdn.discordapp.com/embed/avatars/0.png"
    )

    # AUTO JOIN
    join = safe_request(
        "PUT",
        f"{DISCORD_API}/guilds/{GUILD_ID}/members/{user_id}",
        json={"access_token": access_token},
        headers=bot_headers()
    )

    logging.info(f"Auto-join status: {join.status_code}")

    # SESSION
    session["user"] = {
        "id": user_id,
        "name": username,
        "avatar": avatar
    }

    safe_request(
        "POST",
        WEBHOOK_URL,
        json={"content": f"⚡ **CORE SYNC:** `{username}` authorized."}
    )

    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    u = session["user"]
    return render_template_string("""
    <h1>{{ u.name }}</h1>
    <img src="{{ u.avatar }}" width="128">
    <p>ID: {{ u.id }}</p>

    <form method="POST" action="/send_feedback">
        <textarea name="feedback" maxlength="500"></textarea>
        <button>Send</button>
    </form>

    <a href="/logout">Logout</a>
    """, u=u)

@app.route("/send_feedback", methods=["POST"])
def send_feedback():
    if "user" not in session:
        abort(403)

    msg = request.form.get("feedback", "").strip()
    if not msg:
        return redirect(url_for("dashboard"))

    safe_request(
        "POST",
        FEEDBACK_WEBHOOK,
        json={
            "embeds": [{
                "title": "📩 Intel Received",
                "description": msg[:500],
                "footer": {"text": f"Agent: {session['user']['name']}"}
            }]
        }
    )

    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# -------------------------------------------------
if __name__ == "__main__":
    app.run()
