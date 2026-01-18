import os
from playwright.async_api import async_playwright

ATERNOS_EMAIL = os.getenv("ATERNOS_EMAIL")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")

class Aternos:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def login(self):
        if self.page:
            return

        self.playwright = await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

        await self.page.goto("https://aternos.org/go/", timeout=30000)

        await self.page.fill("#user", ATERNOS_EMAIL)
        await self.page.fill("#password", ATERNOS_PASSWORD)
        await self.page.click("button[type=submit]")

        await self.page.wait_for_url("**/server/**", timeout=30000)

    async def start_server(self):
        await self.login()
        await self.page.click("button:has-text('Start')")

    async def stop_server(self):
        if self.page:
            await self.page.click("button:has-text('Stop')")

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

        self.browser = None
        self.playwright = None
        self.context = None
        self.page = None
