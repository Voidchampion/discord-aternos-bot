# aternos.py
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import asyncio
import os

class AternosBot:
    def __init__(self):
        self.email = os.getenv("ATERNOS_EMAIL")
        self.password = os.getenv("ATERNOS_PASSWORD")
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        print("[Aternos] Starting browser...", flush=True)
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            self.context = await self.browser.new_context(ignore_https_errors=True)
            self.page = await self.context.new_page()

            print("[Aternos] Going to login page...", flush=True)
            await self.page.goto("https://aternos.org/go/", timeout=120000, wait_until="networkidle")

            # Login
            await self.page.fill('input[name="user"]', self.email)
            await self.page.fill('input[name="password"]', self.password)
            await self.page.click('button[type="submit"]')

            print("[Aternos] Waiting for start button...", flush=True)
            await self.page.wait_for_selector('button[data-action="start"]', timeout=120000)

            # Start server
            await self.page.click('button[data-action="start"]')
            await self.page.wait_for_selector('button[data-action="stop"]', timeout=120000)
            print("[Aternos] Server started ✅", flush=True)
            return "Server started ✅"

        except PlaywrightTimeoutError:
            return "❌ Timeout while starting server. Server may be slow or unreachable."
        except Exception as e:
            return f"❌ Error: {e}"

    async def stop(self):
        if not self.page:
            return "Browser not running ❌"
        try:
            print("[Aternos] Going to server page to stop...", flush=True)
            await self.page.goto("https://aternos.org/go/", timeout=120000, wait_until="networkidle")
            await self.page.wait_for_selector('button[data-action="stop"]', timeout=120000)
            await self.page.click('button[data-action="stop"]')
            await self.page.wait_for_selector('button[data-action="start"]', timeout=120000)
            print("[Aternos] Server stopped ✅", flush=True)
            return "Server stopped ✅"
        except PlaywrightTimeoutError:
            return "❌ Timeout while stopping server."
        except Exception as e:
            return f"❌ Error: {e}"

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("[Aternos] Browser closed ✅", flush=True)
