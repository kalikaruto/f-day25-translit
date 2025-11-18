# main.py
import threading
import os
import nest_asyncio
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
import torch, argparse
import discord
from discord import app_commands
from ai4bharat.transliteration import XlitEngine

from utils import *

torch.serialization.add_safe_globals([argparse.Namespace])

# Load .env
load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
GUILD_ID= os.environ.get("GUILD_ID")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not set in .env")

if not GUILD_ID:
    raise ValueError("GUILD_ID not set in .env")

guild = discord.Object(id=int(GUILD_ID))

# --- FastAPI setup ---
app = FastAPI()
engines = {}

def get_engine(lang: str):
    if lang not in engines:
        engines[lang] = XlitEngine(lang, beam_width=10, rescore=True)
    return engines[lang]

@app.post("/transliterate/sentence")
async def transliterate_sentence(data: Input):
    engine = get_engine(data.outlang.value)  # use .value to get ISO code
    out = engine.translit_sentence(data.text)
    return {"input": data.text, "outlang": data.outlang.value, "output": out}

@app.get("/outlang")
async def list_languages():
    return {"supported": LANG_INFO}


# --- Discord bot client setup ---
class MyBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        try:
            guild = discord.Object(id=GUILD_ID) 
            synced = await self.tree.sync(guild=guild)
            
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = MyBot(intents=intents)

# per-user preferred language
user_prefs = {}

@client.tree.command(name="ping", description="Ping the bot", guild=guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

@client.tree.command(name="getlang", description="Get your current default language", guild=guild)
async def getlang(interaction: discord.Interaction):
    lang_enum = user_prefs.get(interaction.user.id, "hi")
    await interaction.response.send_message(f"Your current default language is {lang_enum}")

@client.tree.command(name="setlang", description="Set your language", guild=guild)
@app_commands.describe(lang="Language code")
async def setlang(interaction: discord.Interaction, lang: str):
    print(f"Setting language for user {interaction.user.id} to {lang}")
    try:
        lang_enum = OutLang(lang)
    except ValueError:
        await interaction.response.send_message(
            f"Unsupported language. Use one of: {[l.value for l in OutLang]}"
        )
        return
    
    user_prefs[interaction.user.id] = lang_enum
    await interaction.response.send_message(
        f"Your language is now set to {lang_enum.value}"
    )

@client.tree.command(name="translit", description="Transliterate text", guild=guild)
@app_commands.describe(text="Text to transliterate")
async def translit(interaction: discord.Interaction, text: str):
    lang_enum = user_prefs.get(interaction.user.id)
    if not lang_enum:
        await interaction.response.send_message(
            "You haven't set a default language yet. "
            "Please use `/setlang <lang>` to set one. "
            "Use one of: " + ", ".join([l.value for l in OutLang])
        )
        return

    result = await transliterate_sentence(Input(text=text, outlang=lang_enum))
    await interaction.response.send_message(result["output"])

# --- Start FastAPI in background thread ---
def start_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3039, log_level="info")

threading.Thread(target=start_api, daemon=True).start()

# --- Patch asyncio for Codespaces / Jupyter environments ---
nest_asyncio.apply()

# --- Start Discord bot as a task in the running loop ---
asyncio.get_event_loop().create_task(client.run(TOKEN))

# Keep the loop alive (Codespaces / Jupyter)
asyncio.get_event_loop().run_forever()
