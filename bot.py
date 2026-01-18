# bot.py
import discord
from discord.ext import commands, tasks
import asyncio
import os
from aternos import AternosBot

intents = discord.Intents.default()
intents.message_content = True  # REQUIRED for commands
bot = commands.Bot(command_prefix="!", intents=intents)

aternos_bot = AternosBot()

# Debug startup
print("=== BOT STARTING ===", flush=True)
print("PLAYWRIGHT_BROWSERS_PATH =", os.getenv("PLAYWRIGHT_BROWSERS_PATH"), flush=True)

@bot.event
async def on_ready():
    print(f"[Bot] Logged in as {bot.user}", flush=True)

# Simple ping command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

# Start command with background task
@bot.command()
async def start(ctx):
    await ctx.send("⚡ Starting Aternos server in background...")

    async def start_task():
        result = await aternos_bot.start()
        await ctx.send(result)

    asyncio.create_task(start_task())

# Stop command with background task
@bot.command()
async def stop(ctx):
    await ctx.send("⚡ Stopping Aternos server in background...")

    async def stop_task():
        result = await aternos_bot.stop()
        await ctx.send(result)

    asyncio.create_task(stop_task())

# Close browser manually if needed
@bot.command()
async def close(ctx):
    await aternos_bot.close()
    await ctx.send("Browser closed ✅")

bot.run(os.getenv("DISCORD_TOKEN"))
