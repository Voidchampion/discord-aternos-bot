import os
import sys

print("=== BOT STARTING ===", flush=True)
print("PLAYWRIGHT_BROWSERS_PATH =", os.getenv("PLAYWRIGHT_BROWSERS_PATH"), flush=True)
sys.stdout.flush()

import os
import asyncio
import discord
from discord.ext import commands
from aternos import Aternos

print("PLAYWRIGHT_BROWSERS_PATH =", os.getenv("PLAYWRIGHT_BROWSERS_PATH"))


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
aternos = Aternos()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def start(ctx):
    await ctx.send("🚀 Starting Aternos server...")

    try:
        await aternos.start_server()
        await ctx.send("✅ Server started! Auto shutdown in 2 minutes.")

        await asyncio.sleep(120)

        await aternos.stop_server()
        await ctx.send("⏹️ Server stopped automatically.")

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def stop(ctx):
    try:
        await aternos.stop_server()
        await ctx.send("⏹️ Server stopped.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
