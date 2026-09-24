"""Tests for the email waitlist feature (build-lab/server.py).

Red/Green TDD: these tests must FAIL until server.py exists (red),
then pass once it is implemented (green).

Run with:  python3 -m unittest discover -s tests
"""

import json
import os
import sqlite3
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from unittest import mock

# Make `import server` work when tests run from the build-lab/ folder.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from server import create_server  # noqa: E402  (fails red until server.py exists)


class SignupTests(unittest.TestCase):
    """Every test gets its own server with a throwaway database + outbox."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "signups.db"
        self.outbox_path = Path(self.tmp.name) / "outbox.log"

        self.server = create_server(
            str(self.db_path),
            str(self.outbox_path),
            addr=("127.0.0.1", 0),
            admin_token="test-token",
        )
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    # ---------- helpers ----------

    def post(self, payload, as_json=True):
        data = (
            json.dumps(payload).encode()
            if as_json
            else urllib.parse.urlencode(payload).encode()
        )
        headers = {"Content-Type": "application/json"} if as_json else {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/signup",
            data=data,
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, resp.read().decode()
        except urllib.error.HTTPError as err:
            return err.code, err.read().decode()

    def get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}") as resp:
            return resp.status, resp.read().decode()

    def get_status(self, path):
        """Status only, tolerating 4xx/5xx responses."""
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}") as resp:
                return resp.status
        except urllib.error.HTTPError as err:
            return err.code

    def head_status(self, path):
        """Status for a HEAD request, tolerating 4xx/5xx responses."""
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}", method="HEAD"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status
        except urllib.error.HTTPError as err:
            return err.code

    def outbox_lines(self):
        if not self.outbox_path.exists():
            return []
        return [line for line in self.outbox_path.read_text().splitlines() if line]

    def stored_emails(self):
        conn = sqlite3.connect(self.db_path)
        try:
            rows = conn.execute("SELECT email FROM signups ORDER BY created_at").fetchall()
            return [row[0] for row in rows]
        finally:
            conn.close()

    # ---------- tests ----------

    def test_valid_signup_returns_201_and_stores_email(self):
        status, body = self.post({"email": "michael@machineworks.com"})
        self.assertEqual(status, 201)
        self.assertIn("ok", body)
        self.assertEqual(self.stored_emails(), ["michael@machineworks.com"])

    def test_valid_signup_writes_welcome_email_to_outbox(self):
        self.post({"email": "michael@machineworks.com"})
        lines = self.outbox_lines()
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertEqual(entry["to"], "michael@machineworks.com")
        self.assertEqual(entry["subject"], "You're on the One-Build Sprint list")
        self.assertIn(
            "We'll email your first build plan when the One-Build Sprint opens",
            entry["body"],
        )

    def test_invalid_email_returns_400_and_stores_nothing(self):
        status, _ = self.post({"email": "not-an-email"})
        self.assertEqual(status, 400)
        self.assertEqual(self.stored_emails(), [])
        self.assertEqual(self.outbox_lines(), [])

    def test_duplicate_email_returns_409_and_stays_unique(self):
        self.post({"email": "michael@machineworks.com"})
        status, _ = self.post({"email": "michael@machineworks.com"})
        self.assertEqual(status, 409)
        self.assertEqual(self.stored_emails(), ["michael@machineworks.com"])
        self.assertEqual(len(self.outbox_lines()), 1)  # only one email "sent"

    def test_subscribers_page_lists_emails_newest_first(self):
        self.post({"email": "first@example.com"})
        self.post({"email": "second@example.com"})  # created after first
        status, html = self.get("/subscribers?token=test-token")
        self.assertEqual(status, 200)
        pos_first = html.find("first@example.com")
        pos_second = html.find("second@example.com")
        self.assertGreater(pos_first, -1)
        self.assertGreater(pos_second, -1)
        self.assertLess(pos_second, pos_first)  # newest appears first in the table

    def test_homepage_is_still_served(self):
        status, html = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("One-Build Sprint", html)

    # ---- launch-polish: security headers on EVERY reply -------------------
    REQUIRED_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

    def _headers_for(self, path):
        """Return headers dict for a path, tolerating 4xx/5xx replies."""
        try:
            with urllib.request.urlopen(
                f"http://127.0.0.1:{self.port}{path}"
            ) as resp:
                return {k.lower(): v for k, v in resp.headers.items()}
        except urllib.error.HTTPError as err:
            return {k.lower(): v for k, v in err.headers.items()}

    def _assert_security_headers(self, path):
        headers = self._headers_for(path)
        for name in self.REQUIRED_HEADERS:
            self.assertIn(name.lower(), headers, f"{name} missing on {path}")

    def test_security_headers_on_homepage(self):
        self._assert_security_headers("/")

    def test_security_headers_on_static_css(self):
        self._assert_security_headers("/style.css")

    def test_security_headers_on_404(self):
        self._assert_security_headers("/server.py")

    def test_nosniff_value_is_correct(self):
        headers = self._headers_for("/")
        self.assertEqual(headers.get("x-content-type-options"), "nosniff")

    def test_form_encoded_post_works_too(self):
        status, _ = self.post({"email": "form@example.com"}, as_json=False)
        self.assertEqual(status, 201)
        self.assertIn("form@example.com", self.stored_emails())

    def test_native_form_submit_returns_readable_html_page(self):
        """A no-JS browser submits the form natively (form-encoded).

        It must get a simple HTML page back, never raw JSON text.
        """
        status, body = self.post({"email": "native@example.com"}, as_json=False)
        self.assertEqual(status, 201)
        self.assertIn("You're on the One-Build Sprint list", body)
        self.assertIn("Back to the landing page", body)
        self.assertIn("native@example.com", self.stored_emails())

    def test_json_signup_keeps_returning_json(self):
        """The JS fetch path must stay JSON for the frontend to parse."""
        status, body = self.post({"email": "json@example.com"})
        self.assertEqual(status, 201)
        self.assertTrue(body.strip().startswith("{"), body)

    # ---------- launch hardening: file whitelist ----------

    def test_private_files_are_not_served(self):
        for path in [
            "/data/signups.db",
            "/data/outbox.log",
            "/server.py",
            "/checks.py",
            "/tests/test_signup.py",
            "/SPECS/requirements.md",
            "/SPECS/2026-09-19-launch-hardening/requirements.md",
        ]:
            self.assertEqual(self.get_status(path), 404, f"{path} should be 404")

    def test_public_assets_are_still_served(self):
        for path in ["/", "/index.html", "/style.css", "/script.js"]:
            self.assertEqual(self.get_status(path), 200, f"{path} should be 200")

    def test_path_traversal_is_rejected(self):
        status = self.get_status("/..%2f..%2fetc/passwd")
        self.assertIn(status, (403, 404))

    def test_head_requests_respect_the_whitelist(self):
        """HEAD must 404 on private files exactly like GET —
        otherwise a HEAD /data/outbox.log reveals PII files exist (and their size)."""
        for path in [
            "/data/signups.db",
            "/data/outbox.log",
            "/server.py",
            "/checks.py",
            "/SPECS/requirements.md",
        ]:
            self.assertEqual(self.head_status(path), 404, f"HEAD {path} should be 404")
        for path in ["/", "/style.css", "/script.js"]:
            self.assertEqual(self.head_status(path), 200, f"HEAD {path} should be 200")

    def test_head_subscribers_requires_token(self):
        """Wording/structure: HEAD /subscribers keeps the same access control as GET."""
        self.assertEqual(self.head_status("/subscribers"), 404)
        self.assertEqual(self.head_status("/subscribers?token=wrong"), 404)
        self.assertEqual(self.head_status("/subscribers?token=test-token"), 200)

    def test_head_never_sends_a_body(self):
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/style.css", method="HEAD"
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.read(), b"")

    # ---------- launch hardening: /subscribers token ----------

    def test_subscribers_requires_token(self):
        self.assertEqual(self.get_status("/subscribers"), 404)              # missing
        self.assertEqual(self.get_status("/subscribers?token=wrong"), 404)  # wrong
        self.assertEqual(self.get_status("/subscribers?token=test-token"), 200)
        self.assertEqual(self.get_status("/subscribers/?token=test-token"), 404)  # no alias

    # ---------- launch hardening: outbox is honest about dev mode ----------

    def test_outbox_entry_marks_dev_stub_mode(self):
        self.post({"email": "dev@example.com"})
        entry = json.loads(self.outbox_lines()[0])
        self.assertEqual(entry["mode"], "dev-stub")

    # ---------- launch hardening: rate limit ----------

    def test_signup_rate_limit_returns_429_after_ten(self):
        for i in range(10):
            status, _ = self.post({"email": f"user{i}@example.com"})
            self.assertEqual(status, 201)
        status, body = self.post({"email": "over@example.com"})
        self.assertEqual(status, 429)
        self.assertIn("try again", body)

    # ---------- launch hardening: admin token is never a known default ----------

    def test_default_admin_token_is_random(self):
        """Without ADMIN_TOKEN, each server gets a fresh unguessable token."""
        def make_server():
            srv = create_server(
                str(Path(self.tmp.name) / "tok_a.db"),
                str(Path(self.tmp.name) / "tok_a.log"),
                addr=("127.0.0.1", 0),
            )
            token = srv.admin_token
            srv.server_close()
            return token

        with mock.patch.dict(os.environ, {}, clear=True):
            first = make_server()
            second = make_server()
        self.assertNotEqual(first, second)
        self.assertGreater(len(first), 12)


if __name__ == "__main__":
    unittest.main()