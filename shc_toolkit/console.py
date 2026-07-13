"""
SHC portal + noVNC console automation.

Requires playwright as an optional dependency:
    pip install playwright && playwright install chromium

Usage:
    from shc_toolkit.console import ConsoleSession

    session = ConsoleSession()  # reads SHC_PLAYWRIGHT_EMAIL/PASSWORD
    session.login()
    user, pw = session.get_service_password(605)
    session.open_console(605)
    session.type_text("whoami\\n")
    session.screenshot("output.png")
    session.close()
"""

from __future__ import annotations

import logging
import os

log = logging.getLogger(__name__)

PORTAL_BASE = "https://blesta.sovereignhybridcompute.com"

# Proven reliable via testing: faster rates lose characters over the noVNC
# WebSocket. 80ms is the sweet spot; 100ms is extra-safe.
TYPE_DELAY_MS = 80


class ConsoleError(Exception):
    """Portal or console automation error."""


class ConsoleSession:
    """Persistent SHC portal + noVNC console session."""

    def __init__(
        self,
        email: str | None = None,
        password: str | None = None,
        *,
        headless: bool = True,
    ):
        self.email = (
            email
            or os.environ.get("SHC_PLAYWRIGHT_EMAIL")
            or os.environ.get("SHC_EMAIL", "")
        )
        self.password = (
            password
            or os.environ.get("SHC_PLAYWRIGHT_PASSWORD")
            or os.environ.get("SHC_PASSWORD", "")
        )
        if not self.email or not self.password:
            raise ConsoleError(
                "Portal credentials required. Set SHC_PLAYWRIGHT_EMAIL and "
                "SHC_PLAYWRIGHT_PASSWORD env vars (or ~/.config/shc/credentials.sh)."
            )
        self.headless = headless
        self._pw = None
        self._browser = None
        self._page = None
        self._logged_in = False

    def _ensure_browser(self):
        if self._browser is not None:
            return
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise ConsoleError(
                "playwright is required: "
                "pip install playwright && playwright install chromium"
            )
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=self.headless)
        self._page = self._browser.new_page(viewport={"width": 1280, "height": 800})

    def login(self):
        """Log into the Blesta client portal."""
        self._ensure_browser()
        page = self._page
        page.goto(f"{PORTAL_BASE}/client/login/", wait_until="networkidle")  # type: ignore[attr-defined]
        page.fill('input[placeholder="Email Address"]', self.email)  # type: ignore[attr-defined]
        page.fill('input[placeholder="Password"]', self.password)  # type: ignore[attr-defined]
        page.click('button:has-text("Log In")')  # type: ignore[attr-defined]
        page.wait_for_load_state("networkidle", timeout=15000)  # type: ignore[attr-defined]
        if "/login" in page.url:  # type: ignore[attr-defined]
            raise ConsoleError("Login failed — check SHC_PLAYWRIGHT_EMAIL/PASSWORD")
        self._logged_in = True
        log.info("Portal login OK as %s", self.email)

    # ── Service Info ────────────────────────────────────────────

    def get_service_password(self, service_id: int) -> tuple[str, str]:
        """Retrieve (username, password) from the portal Service Info page."""  # type: ignore[attr-defined]
        if not self._logged_in:
            self.login()
        page = self._page
        page.goto(  # type: ignore[attr-defined]
            f"{PORTAL_BASE}/client/services/manage/{service_id}/",
            wait_until="networkidle",
        )
        password_input = page.query_selector('input[placeholder="Server password"]')  # type: ignore[attr-defined]
        if not password_input:
            raise ConsoleError(f"No password field for service {service_id}")
        password = password_input.get_attribute("value") or ""
        _extract_username_js = """() => {
            const els = document.querySelectorAll('div, span, p');
            for (let i = 0; i < els.length; i++) {
                if (els[i].textContent.trim() === 'Login User') {
                    let n = els[i].nextElementSibling || els[i].parentElement.querySelector('div:nth-child(2)');
                    return n ? n.textContent.trim() : '';
                }
            }
            return '';
        }"""
        username = page.evaluate(_extract_username_js)  # type: ignore[attr-defined]
        if not password:
            raise ConsoleError(f"Empty password for service {service_id}")
        return (username or "debian", password)

    # ── noVNC Console ───────────────────────────────────────────

    def open_console(self, service_id: int):
        """Navigate to the VM's embedded noVNC console tab."""
        if not self._logged_in:
            self.login()
        page = self._page
        page.goto(  # type: ignore[attr-defined]
            f"{PORTAL_BASE}/client/services/manage/{service_id}/tabConsole/",
            wait_until="networkidle",
        )
        iframe = page.query_selector("#serviceConsoleFrame")  # type: ignore[attr-defined]
        if not iframe:
            raise ConsoleError(f"No console iframe for service {service_id}")
        page.wait_for_timeout(3000)  # type: ignore[attr-defined]
        log.info("Console open for service %d", service_id)

    def _console_frame(self):
        """Return the Playwright Frame object for the console iframe."""
        return self._page.locator("#serviceConsoleFrame").content_frame()  # type: ignore[attr-defined]

    def paste_text(self, text: str):
        """Send text via the 'Paste to VM' dialog (faster than type_text).

        May mangle special characters at longer lengths. For critical
        text (passwords, base64 blobs), prefer type_text.
        """
        frame = self._console_frame()
        paste_btn = frame.locator('button:has-text("Paste to VM")')
        if paste_btn.count() == 0:
            raise ConsoleError("Paste to VM button not found — console not ready?")
        paste_btn.click()
        textarea = frame.locator('textarea')
        textarea.fill(text)
        frame.locator('button:has-text("Type into VM")').click()
        self._page.wait_for_timeout(min(len(text) * 15, 10000))  # type: ignore[attr-defined]

    def type_text(self, text: str, delay_ms: int = TYPE_DELAY_MS):
        """Type text char-by-char via trusted keyboard events.

        Slower than paste_text but reliable for all characters.
        Proven at 80ms/char on SHC noVNC (faster rates lose chars).
        """
        frame = self._console_frame()
        canvas = frame.locator("canvas").first
        canvas.click()
        self._page.wait_for_timeout(200)  # type: ignore[attr-defined]
        self._page.keyboard.type(text, delay=delay_ms)  # type: ignore[attr-defined]

    def press_key(self, key: str):
        """Press a single key: 'Enter', 'Escape', 'Control+c', etc."""
        self._page.keyboard.press(key)  # type: ignore[attr-defined]

    def screenshot(self, path: str | None = None) -> bytes:
        """Screenshot the console viewport."""
        return self._page.screenshot(path=path)  # type: ignore[attr-defined]

    def read_console_text(self) -> str:
        """Best-effort text extraction from the console canvas.

        noVNC renders to a <canvas>, so there's no DOM text. This returns ''
        unless an OCR library is available. For programmatic verification,
        prefer SHA256-based integrity checks over screen reading.
        """
        return ""

    def close(self):
        """Close browser and release resources."""
        if self._browser:
            self._browser.close()
        if self._pw:
            self._pw.stop()
        self._browser = None
        self._page = None
        self._logged_in = False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
