# main.py
import threading
import os
import nest_asyncio
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
import torch, argparse
import discord
from discord.ext import commands
from ai4bharat.transliteration import XlitEngine

from utils import *

torch.serialization.add_safe_globals([argparse.Namespace])

# Load .env
load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not set in .env")

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


# --- Discord bot setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=":", intents=intents)

# per-user preferred language
user_prefs = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def getlang(ctx):
    """Get your current default language"""
    lang = user_prefs.get(ctx.author.id, "hi")
    await ctx.send(f"Your current default language is {lang}")

@bot.command()
async def setlang(ctx, lang: str):
    try:
        lang_enum = OutLang(lang)
    except ValueError:
        await ctx.send(f"Unsupported language. Use one of: {[l.value for l in OutLang]}")
        return
    user_prefs[ctx.author.id] = lang_enum
    await ctx.send(f"Your language is now set to {lang_enum.value}")

@bot.command()
async def translit(ctx, *, text: str):
    # Check if user has set a preferred language
    lang_enum = user_prefs.get(ctx.author.id)
    if not lang_enum:
        await ctx.send(
            "You haven't set a default language yet. "
            "Please use `!setlang <lang>` to set one. "
            "Use one of: " + ", ".join([l.value for l in OutLang])
        )
        return

    # Proceed with transliteration
    result = await transliterate_sentence(Input(text=text, outlang=lang_enum))
    await ctx.send(result["output"])

# --- Start FastAPI in background thread ---
def start_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3039, log_level="info")

threading.Thread(target=start_api, daemon=True).start()

# --- Patch asyncio for Codespaces / Jupyter environments ---
nest_asyncio.apply()

# --- Start Discord bot as a task in the running loop ---
asyncio.get_event_loop().create_task(bot.start(TOKEN))

# Keep the loop alive (Codespaces / Jupyter)
asyncio.get_event_loop().run_forever()
