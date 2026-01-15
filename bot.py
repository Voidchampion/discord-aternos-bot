import discord
from discord import app_commands
import asyncio
import os
from aternos import start_server, stop_server

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Logged in as {client.user}")


@tree.command(name="start", description="Start the Aternos server")
async def start(interaction: discord.Interaction):
    await interaction.response.send_message("Starting server...")
    await start_server()

    await interaction.followup.send("Server started. Auto-shutdown in 2 minutes.")

    await asyncio.sleep(120)
    await stop_server()
    await interaction.followup.send("Server auto-shutdown complete.")


@tree.command(name="stop", description="Stop the Aternos server")
async def stop(interaction: discord.Interaction):
    await interaction.response.send_message("Stopping server...")
    await stop_server()
    await interaction.followup.send("Server stopped.")


client.run(TOKEN)
