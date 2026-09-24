"""HandsOn Automation — waitlist server (dev mode).

Serves the landing page AND handles the One-Build Sprint signup:

  POST /signup    -> saves the email to SQLite, "sends" the welcome
                     email (dev-mode: written to data/outbox.log)
  GET  /subscribers -> HTML table of everyone who signed up, newest first
  GET  anything   -> static files (index.html, style.css, script.js)

Python stdlib only: http.server + sqlite3. No frameworks.
Run with:  python3 server.py     (binds 0.0.0.0:3000)
Tests:     python3 -m unittest discover -s tests
"""

import collections
import functools
import hmac
import html
import json
import os
import secrets
import sqlite3
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# ---------------------------------------------------------------- config

PORT = 3000
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
DB_PATH = DATA_DIR / "signups.db"
OUTBOX_PATH = DATA_DIR / "outbox.log"
MAX_BODY_BYTES = 10 * 1024  # 10 KB cap on requests

# The ONLY files the web server may serve. Everything else in the project
# folder (data/, SPECS/, source files) must never be publicly reachable.
WHITELISTED = {"index.html", "style.css", "script.js"}

# The welcome email (dev-mode stub). Honest waitlist copy: the sprint is not
# open yet, so we promise to email the plan when it opens — never an immediate
# delivery we cannot make. Swapping in a real email provider later only means
# changing send_welcome_email() below.
WELCOME_SUBJECT = "You're on the One-Build Sprint list"
WELCOME_BODY = (
    "You're on the list. We'll email your first build plan "
    "when the One-Build Sprint opens.\n\n"
    "- HandsOn Automation"
)

# ----------------------------------------------------------------
# Launch polish — security headers (single point of truth).
#
# Every reply (200/404/409/413/429, static + JSON + HTML) passes
# through this one function, so a header can never be forgotten on
# one path. The Content-Security-Policy deliberately keeps Google
# Fonts working (style-src fonts.googleapis.com, font-src
# fonts.gstatic.com) while allowing only our own local JS/CSS —
# no remote scripts, ever.
# ----------------------------------------------------------------
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "  # local script.js + tiny inline bootstrap (html.js)
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "frame-ancestors 'none'"
)

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Content-Security-Policy": CSP,
}

def add_security_headers(self):
    """Attach the security headers to the response being built.

    Call BEFORE end_headers() — the one chokepoint every handler
    already uses, so nothing can slip through on a 404/409/429 path.
    """
    for name, value in SECURITY_HEADERS.items():
        self.send_header(name, value)


# ---------------------------------------------------------------- logging

def log(level, message):
    """One small logging helper; business code never prints on its own."""
    print(f"[waitlist:{level}] {message}", flush=True)


def log_request(handler_method):
    """Decorator: logs the request line AFTER the handler has answered.

    Business logic stays clean -- handlers just return their status code.
    """

    @functools.wraps(handler_method)
    def wrapper(self):
        status = handler_method(self)
        log("INFO", f"{self.command} {self.path} -> {status}")
        return status

    return wrapper


# ---------------------------------------------------------------- email rules

def normalize_email(email):
    """Trim whitespace and lower-case: one canonical form per address."""
    return email.strip().lower()


def is_valid_email(email):
    """Server-side validation, the single source of truth.

    A small, readable contract: one '@', both sides non-empty, no spaces,
    a dot in the domain, and not absurdly long.
    """
    email = normalize_email(email)
    if not email or len(email) > 254:
        return False
    if email.count("@") != 1 or " " in email:
        return False
    local, domain = email.split("@")
    return bool(local) and bool(domain) and "." in domain


# ---------------------------------------------------------------- database

def open_db(db_path):
    """Open the SQLite database, creating the file and table if needed."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS signups ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "email TEXT NOT NULL UNIQUE, "
        "created_at TEXT NOT NULL DEFAULT (datetime('now')))"
    )
    conn.commit()
    return conn


def store_signup(conn, email):
    """Insert a signup. Returns True if new, False if duplicate."""
    try:
        conn.execute("INSERT INTO signups (email) VALUES (?)", (email,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


# ---------------------------------------------------------------- outbox (dev email)

def send_welcome_email(outbox_path, email):
    """Dev-mode 'sending': append one JSON line per welcome email.

    Every entry is tagged "mode": "dev-stub" so the founder always knows
    these emails were NOT really delivered. This is the ONLY function to
    change when a real provider is added.
    """
    entry = {
        "sent_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "mode": "dev-stub",
        "to": email,
        "subject": WELCOME_SUBJECT,
        "body": WELCOME_BODY,
    }
    with open(outbox_path, "a", encoding="utf-8") as outbox:
        outbox.write(json.dumps(entry) + "\n")


# ---------------------------------------------------------------- rate limiting

class RateLimiter:
    """Simple per-IP limiter: allow up to `limit` calls in a rolling window."""

    def __init__(self, limit=10, window_seconds=3600):
        self.limit = limit
        self.window_seconds = window_seconds
        self.hits = collections.defaultdict(list)
        self._lock = threading.Lock()

    def allow(self, key):
        now = time.time()
        with self._lock:
            recent = [t for t in self.hits[key] if now - t < self.window_seconds]
            if len(recent) >= self.limit:
                self.hits[key] = recent
                return False
            recent.append(now)
            self.hits[key] = recent
            return True


# ---------------------------------------------------------------- HTML for /subscribers

def subscribers_html(rows):
    """Render the subscriber list as a simple table (newest first)."""
    cells = "".join(
        f"<tr><td>{html.escape(email)}</td><td>{html.escape(created)}</td></tr>"
        for email, created in rows
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Subscribers - HandsOn Automation</title>
</head>
<body style="font-family: sans-serif; max-width: 720px; margin: 2rem auto;">
  <h1>One-Build Sprint subscribers</h1>
  <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
    <thead><tr><th>Email</th><th>Signed up</th></tr></thead>
    <tbody>{cells}</tbody>
  </table>
  <p><a href="/">Back to the landing page</a></p>
</body>
</html>"""


def form_page(headline, note):
    """A small, readable HTML page for native (no-JS) form submissions.

    When JavaScript is off, the sign-up form posts as form-encoded data. Reply
    with a simple HTML page instead of raw JSON text that the browser would
    just dump on screen. All copy is honest waitlist language.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(headline, quote=False)} - HandsOn Automation</title>
</head>
<body style="font-family: sans-serif; max-width: 640px; margin: 3rem auto; line-height: 1.5;">
  <h1>{html.escape(headline, quote=False)}</h1>
  <p>{html.escape(note, quote=False)}</p>
  <p><a href="/">Back to the landing page</a></p>
</body>
</html>"""


# ---------------------------------------------------------------- HTTP handler

class WaitlistHandler(SimpleHTTPRequestHandler):
    """Routes /signup and /subscribers; serves static files for the rest."""

    # ------------------------------------------------------------------
    # Security headers — ONE chokepoint. Every response (200/400/404/409/
    # 413/429, static, JSON, HTML, native-form) passes through
    # end_headers(), so hardening this in one place can never be forgotten
    # on a reply path. The CSP is tuned to the real page: Google Fonts via
    # fonts.googleapis.com (styles) and fonts.gstatic.com (font files), our
    # local style.css/script.js from self, a tiny inline bootstrap that adds
    # the `<html class="js">` gate before first paint for motion gating, and
    # a data-URI favicon. No remote scripts, ever.
    # ------------------------------------------------------------------
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "        # local script.js + html.js bootstrap only
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; "
            "img-src 'self' data:; "
            "connect-src 'self'"
        ),
    }

    def end_headers(self):
        for name, value in self.SECURITY_HEADERS.items():
            self.send_header(name, value)
        super().end_headers()

    def log_message(self, format, *args):
        pass  # silence the base class; our log_request decorator logs for us

    # ---------- helpers ----------

    def _reply_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _reply_html(self, status, body, head=False):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head:
            self.wfile.write(data)

    # ---------- routes ----------

    @log_request
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/subscribers":
            return self._subscribers()
        return self._static()

    @log_request
    def do_HEAD(self):
        """HEAD goes through the same access checks as GET.

        The base-class do_HEAD would serve ANY project file (it calls the base
        send_head(), which never consults the whitelist). Routing HEAD here
        keeps private files hidden — no existence/size leaks — while still
        sending the same headers as GET, minus the body.
        """
        path = urlparse(self.path).path
        if path == "/subscribers":
            return self._subscribers(head=True)
        return self._static(head=True)

    @log_request
    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/signup":
            self.send_error(404)
            return 404
        return self._signup()

    # ---------- GET /subscribers (founder only) ----------

    def _subscribers(self, head=False):
        given = parse_qs(urlparse(self.path).query).get("token", [""])[0]
        if not given or not hmac.compare_digest(given, self.server.admin_token):
            self.send_error(404)  # 404, not 401: do not reveal the page exists
            return 404
        conn = open_db(self.server.db_path)
        try:
            rows = conn.execute(
                "SELECT email, created_at FROM signups "
                "ORDER BY created_at DESC, id DESC"  # newest first; id breaks 1-second ties
            ).fetchall()
        finally:
            conn.close()
        self._reply_html(200, subscribers_html(rows), head=head)
        return 200

    # ---------- static files (public whitelist only) ----------

    def _static(self, head=False):
        parsed = urlparse(self.path)
        relative = parsed.path.lstrip("/")
        if not relative:  # "/" means the homepage
            relative = "index.html"

        if relative not in WHITELISTED:
            self.send_error(404)  # private files are never served
            return 404

        candidate = (PROJECT_DIR / relative).resolve()
        if not str(candidate).startswith(str(PROJECT_DIR.resolve())):
            self.send_error(403)  # path escaped the project folder
            return 403

        if not candidate.is_file():
            self.send_error(404)
            return 404

        data = candidate.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(candidate.name))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head:
            self.wfile.write(data)
        return 200

    # ---------- POST /signup ----------

    def _signup(self):
        is_form = (self.headers.get("Content-Type") or "").startswith(
            "application/x-www-form-urlencoded"
        )
        if not self.server.limiter.allow(self.client_address[0]):
            return self._signup_answer(
                429, "too many signups — please try again later", is_form
            )

        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY_BYTES:
            return self._signup_answer(413, "payload too large", is_form)

        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        email = self._parse_email(raw)
        if email is None:
            return self._signup_answer(400, "invalid email", is_form)

        conn = open_db(self.server.db_path)
        try:
            stored = store_signup(conn, email)
        finally:
            conn.close()

        if not stored:
            return self._signup_answer(409, "duplicate email", is_form)

        send_welcome_email(self.server.outbox_path, email)
        return self._signup_answer(201, "ok", is_form)

    def _signup_answer(self, status, message, is_form):
        """Send JSON for the JS fetch, or a readable HTML page for a native form.

        A native form only exists when JavaScript is off (progressive
        enhancement), so the HTML path keeps that flow readable. The JSON path
        is unchanged for the frontend fetch.
        """
        if not is_form:
            payload = {"status": "ok"} if status == 201 else {"error": message}
            self._reply_json(status, payload)
            return status

        if status == 201:
            headline = "You're on the One-Build Sprint list"
            note = "We'll email your first build plan when the One-Build Sprint opens."
        elif status == 409:
            headline = "You're already on the list"
            note = "We'll email your first build plan when the One-Build Sprint opens."
        elif status == 400:
            headline = "That email doesn't look right"
            note = "Go back, double-check your email, and try again."
        elif status == 429:
            headline = "One moment — too many signups"
            note = "Please try again in a minute."
        else:  # 413 and any unknown
            headline = "That signup was too large"
            note = "Please go back and try again."
        self._reply_html(status, form_page(headline, note))
        return status

    def _parse_email(self, raw):
        """Accept JSON {"email": ...} or form-encoded email=...; validate."""
        try:
            data = json.loads(raw)
            email = data.get("email", "")
        except (json.JSONDecodeError, AttributeError):
            params = parse_qs(raw)
            email = params.get("email", [""])[0]
        if not is_valid_email(email):
            return None
        return normalize_email(email)


# ---------------------------------------------------------------- server + main

class WaitlistServer(ThreadingHTTPServer):
    """A tiny subclass that carries our config to the handler."""

    def __init__(self, addr, handler, db_path, outbox_path, admin_token):
        super().__init__(addr, handler)
        self.db_path = db_path
        self.outbox_path = outbox_path
        self.admin_token = admin_token
        self.limiter = RateLimiter()


def create_server(db_path, outbox_path, addr=("0.0.0.0", PORT), admin_token=None):
    """Build a server; tests pass throwaway paths, main() uses the real ones.

    The /subscribers token comes from the ADMIN_TOKEN env var; when it is not
    set, each run gets a fresh random token (never a known default that could
    be guessed from the source code). The startup banner always prints the URL.
    """
    if admin_token is None:
        admin_token = os.environ.get("ADMIN_TOKEN") or secrets.token_urlsafe(16)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    Path(outbox_path).parent.mkdir(parents=True, exist_ok=True)
    conn = open_db(db_path)  # schema exists before the first request
    conn.close()
    return WaitlistServer(addr, WaitlistHandler, db_path, outbox_path, admin_token)


def main():
    hostname = os.environ.get("CODIO_HOSTNAME")
    base = f"https://{hostname}-{PORT}.codio.io/" if hostname else f"http://localhost:{PORT}/"
    print(f"Your site is live at {base}", flush=True)
    server = create_server(str(DB_PATH), str(OUTBOX_PATH), ("0.0.0.0", PORT))
    print("DEV MODE: welcome emails are stubbed — no real email is sent yet.", flush=True)
    if not os.environ.get("ADMIN_TOKEN"):
        print("ADMIN_TOKEN not set — this run uses a fresh random token (see URL below).", flush=True)
    print(f"Founder only — subscribers: {base}subscribers?token={server.admin_token}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()