# bot.py
import discord
from discord.ext import commands
import asyncio

# Make sure intents are enabled
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# Bot prefix is !
bot = commands.Bot(command_prefix='!', intents=intents)

# Test command to make sure bot responds
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# Example start command (replace with your Aternos logic later)
@bot.command()
async def start(ctx):
    await ctx.send("🚀 Starting server...")
    # Simulate server start delay
    await asyncio.sleep(2)  # Remove or replace with your actual Aternos code
    await ctx.send("✅ Server started!")

# Example stop command with auto-shutdown
@bot.command()
async def stop(ctx):
    await ctx.send("⏹️ Stopping server...")
    await asyncio.sleep(2)  # Simulate server stop
    await ctx.send("✅ Server stopped!")

# Run the bot with token from Railway environment variables
import os
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
