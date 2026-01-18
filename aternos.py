from playwright.async_api import async_playwright
import os

ATERNOS_EMAIL = os.getenv("ATERNOS_EMAIL")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

class Aternos:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    async def login(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )
        context = await self.browser.new_context()
        self.page = await context.new_page()

        await self.page.goto("https://aternos.org/go/")
        await self.page.fill('input[name="username"]', ATERNOS_EMAIL)
        await self.page.fill('input[name="password"]', ATERNOS_PASSWORD)
        await self.page.click('button[type="submit"]')

        await self.page.wait_for_url("https://aternos.org/server/*", timeout=20000)

    async def start(self):
        if not self.page:
            await self.login()
        await self.page.click('button:has-text("Start")')

    async def stop(self):
        if self.page:
            await self.page.click('button:has-text("Stop")')

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
