# aternos.py
from playwright.async_api import async_playwright
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
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        self.context = await self.browser.new_context(ignore_https_errors=True)
        self.page = await self.context.new_page()

        # Go to login page
        await self.page.goto("https://aternos.org/go/", timeout=120000, wait_until="networkidle")

        # Fill login form
        await self.page.fill('input[name="user"]', self.email)
        await self.page.fill('input[name="password"]', self.password)
        await self.page.click('button[type="submit"]')

        # Wait for server page
        await self.page.wait_for_selector('button[data-action="start"]', timeout=120000)

        # Click start
        await self.page.click('button[data-action="start"]')

        # Wait for server to start
        await self.page.wait_for_selector('button[data-action="stop"]', timeout=120000)
        return "Server started ✅"

    async def stop(self):
        if not self.page:
            return "Browser not running ❌"
        # Go to server page
        await self.page.goto("https://aternos.org/go/", timeout=120000, wait_until="networkidle")
        await self.page.wait_for_selector('button[data-action="stop"]', timeout=120000)
        await self.page.click('button[data-action="stop"]')
        await self.page.wait_for_selector('button[data-action="start"]', timeout=120000)
        return "Server stopped ✅"

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
