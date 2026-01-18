# bot.py
import discord
from discord.ext import commands, tasks
import asyncio
import os
from aternos import AternosBot

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

aternos_bot = AternosBot()

# Debug environment variable
print("=== BOT STARTING ===", flush=True)
print("PLAYWRIGHT_BROWSERS_PATH =", os.getenv("PLAYWRIGHT_BROWSERS_PATH"), flush=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

@bot.command()
async def start(ctx):
    await ctx.send("Starting Aternos server...")
    try:
        result = await aternos_bot.start()
        await ctx.send(result)
    except Exception as e:
        await ctx.send(f"❌ Failed to start server: {e}")

@bot.command()
async def stop(ctx):
    await ctx.send("Stopping Aternos server...")
    try:
        result = await aternos_bot.stop()
        await ctx.send(result)
    except Exception as e:
        await ctx.send(f"❌ Failed to stop server: {e}")

@bot.command()
async def close(ctx):
    await aternos_bot.close()
    await ctx.send("Browser closed ✅")

bot.run(os.getenv("DISCORD_TOKEN"))
