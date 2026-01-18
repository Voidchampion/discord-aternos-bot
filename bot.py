import discord
from discord.ext import commands
import asyncio
import os
import aiohttp

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def test_conn(ctx):
    """Test if container can reach Aternos"""
    await ctx.send("Testing connectivity to Aternos...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://aternos.org/go/", timeout=10) as resp:
                await ctx.send(f"✅ Success! Status code: {resp.status}")
    except Exception as e:
        await ctx.send(f"❌ Failed to reach Aternos: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
