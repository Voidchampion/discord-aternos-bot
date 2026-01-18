import discord
from discord.ext import commands
import asyncio
import os
from aternos import Aternos

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

aternos = Aternos()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def start(ctx):
    await ctx.send("🚀 Starting server...")
    try:
        await aternos.start()
        await ctx.send("✅ Server started! Auto shutdown in 2 minutes.")
        await asyncio.sleep(120)
        await aternos.stop()
        await ctx.send("⏹️ Server stopped automatically.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def stop(ctx):
    try:
        await aternos.stop()
        await ctx.send("⏹️ Server stopped.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
