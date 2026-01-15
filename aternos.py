from playwright.async_api import async_playwright
import asyncio
import os

ATERNOS_EMAIL = os.getenv("ATERNOS_EMAIL")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")
SERVER_NAME = os.getenv("ATERNOS_SERVER_NAME")


async def start_server():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://aternos.org/go/")

        # Login
        await page.fill('input[name="user"]', ATERNOS_EMAIL)
        await page.fill('input[name="password"]', ATERNOS_PASSWORD)
        await page.click('button[type="submit"]')

        await page.wait_for_timeout(5000)

        # Select server
        await page.click(f"text={SERVER_NAME}")
        await page.wait_for_timeout(3000)

        # Start server
        await page.click("#start")
        await page.wait_for_timeout(5000)

        await browser.close()


async def stop_server():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://aternos.org/go/")

        await page.fill('input[name="user"]', ATERNOS_EMAIL)
        await page.fill('input[name="password"]', ATERNOS_PASSWORD)
        await page.click('button[type="submit"]')

        await page.wait_for_timeout(5000)
        await page.click(f"text={SERVER_NAME}")
        await page.wait_for_timeout(3000)

        await page.click("#stop")
        await page.wait_for_timeout(5000)

        await browser.close()
# aternos automation 
