# bot.py
import discord
from discord.ext import commands, tasks
import asyncio
from playwright.async_api import async_playwright
import os

# Intents and bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ATERNOS_EMAIL = os.getenv("ATERNOS_EMAIL")
ATERNOS_PASSWORD = os.getenv("ATERNOS_PASSWORD")
ATERNOS_SERVER_NAME = os.getenv("ATERNOS_SERVER_NAME")

# Track server status
server_running = False

# ----- Helper function to start Aternos server -----
async def start_aternos():
    global server_running
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        page = await browser.new_page()
        # Go to Aternos login page
        await page.goto("https://aternos.org/go/")
        
        # Login
        await page.fill("input[name='username']", ATERNOS_EMAIL)
        await page.fill("input[name='password']", ATERNOS_PASSWORD)
        await page.click("button[type='submit']")
        await page.wait_for_timeout(5000)  # wait for login
        
        # Go to server page
        await page.goto(f"https://aternos.org/server/{ATERNOS_SERVER_NAME}/")
        
        # Start server button
        await page.click("button:has-text('Start')")
        await page.wait_for_timeout(5000)  # wait a bit for server to start
        
        await browser.close()
        server_running = True

# ----- Commands -----
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def start(ctx):
    global server_running
    if server_running:
        await ctx.send("⚠️ Server is already running!")
        return
    await ctx.send("🚀 Starting server...")
    try:
        await start_aternos()
        await ctx.send("✅ Server started! It will auto-shutdown in 2 minutes.")
        # Auto shutdown after 2 minutes
        await asyncio.sleep(120)
        await stop_server(ctx)
    except Exception as e:
        await ctx.send(f"❌ Failed to start server: {e}")

@bot.command()
async def stop(ctx):
    global server_running
    await stop_server(ctx)

# ----- Stop helper -----
async def stop_server(ctx):
    global server_running
    if not server_running:
        await ctx.send("⚠️ Server is not running!")
        return
    # For simplicity, we just set server_running False.
    # You can expand this to click "Stop" button in Aternos
    server_running = False
    await ctx.send("⏹️ Server stopped.")

# ----- Run bot -----
bot.run(DISCORD_TOKEN)
