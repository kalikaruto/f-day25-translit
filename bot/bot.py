import os
import discord
from discord import app_commands
import aiohttp
from dotenv import load_dotenv

from utils import *

load_dotenv()
TOKEN = os.environ.get("DISCORD_TOKEN")
BACKEND_URL = os.environ.get("BACKEND_URL")
GUILD_ID= os.environ.get("GUILD_ID")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not set in .env")
if not BACKEND_URL:
    raise ValueError("BACKEND_URL not set in .env")
if not GUILD_ID:
    raise ValueError("GUILD_ID not set in .env")

guild = discord.Object(id=int(GUILD_ID))

class MyBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged on as {self.user}')
        
        try:
            guild = discord.Object(id=int(GUILD_ID)) 
            # self.tree.clear_commands(guild=guild)
            synced = await self.tree.sync(guild=guild)
            
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = MyBot(intents=intents)

# per-user preferred language
user_prefs_lang_codes = {}
user_prefs_src_script_types = {}

async def call_backend(text, lang, src):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/transliterate/sentence",
            json={
                "text": text,
                "lang": lang.value,
                "srclang": src.value
            },
        ) as resp:
            return await resp.json()

async def warmup_backend(lang_code, src_lang):
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                f"{BACKEND_URL}/transliterate/sentence",
                json={
                    "text": "warmup",
                    "lang": lang_code.value,
                    "srclang": src_lang.value,
                },
                timeout=10
            )
    except Exception as e:
        print("Warmup error:", e)


@client.tree.command(name="ping", description="Ping the bot", guild=guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong")

@client.tree.command(name="list", description="List your current default transliteration settings", guild=guild)
async def gl(interaction: discord.Interaction):
    def format_table(items):
        lines = ["Code\t\tLabel"]
        for item in items:
            lines.append(f"{item['code']}\t\t{item['label']}")
        return "\n".join(lines)

    lang_table = format_table(LANG_INFO)
    src_table = format_table(SRC_SCRIPT_TYPES_INFO)
    msg = f"NOTE: Use the Code column for setting your language. \n\n **Supported Languages:**\n{lang_table}\n\n**Source Script Types:**\n{src_table}"
    await interaction.response.send_message(msg)

@client.tree.command(name="help", description="Show help for bot commands", guild=guild)
async def help_cmd(interaction: discord.Interaction):
    help_text = (
        "**Bot Commands:**\n"
        "/ping - Check if the bot is online\n"
        "/list - List supported languages and source script types\n"
        "/getlang - Show your current default transliteration settings\n"
        "/setlang <src_script_type>-<lang_code> - Set your preferred transliteration (e.g., /setlang roman-hi)\n"
        "/translit <text> - Transliterate text using your settings\n"
        "/help - Show this help message\n"
        "\n"
        "Example usage:\n"
        "`/setlang roman-hi`\n"
        "`/translit namaste`\n"
    )
    await interaction.response.send_message(help_text)

@client.tree.command(name="getlang", description="Get your current default language", guild=guild)
async def gl(interaction: discord.Interaction):
    lang_code = user_prefs_lang_codes.get(interaction.user.id, Lang.hi)
    srclang = user_prefs_src_script_types.get(interaction.user.id, SrcLang.roman)
    await interaction.response.send_message(f"Your current default transliteration is from {'roman' if srclang==SrcLang.roman else lang_code.value} to {lang_code.value if srclang==SrcLang.roman else 'roman'}.")

@client.tree.command(name="setlang", description="Set your language", guild=guild)
@app_commands.describe(lang="<src_script_type>-<lang_code>")
async def sl(interaction: discord.Interaction, lang: str):
    print(f"Setting language for user {interaction.user.id} to {lang}")
    try:
        src, out = lang.split("-")
        lang_code = Lang[out]
        src_lang = SrcLang[src]
    except KeyError:
        await interaction.response.send_message(
            f"Unsupported language. Options for source script types: {[l.value for l in SrcLang]}, lang codes: {[l.value for l in Lang]}"
        )
        return
    except ValueError:
        await interaction.response.send_message(
            "Invalid format. Use /sl <src>-<lang_code> e.g., /sl indic-hi or /sl roman-ta"
        )
        return
    user_prefs_lang_codes[interaction.user.id] = lang_code
    user_prefs_src_script_types[interaction.user.id] = src_lang
    await interaction.response.send_message(
        f"Set your preferred transliteration from {src if src==SrcLang.roman.value else lang_code.value} to {lang_code.value if src==SrcLang.roman.value else SrcLang.roman.value}."
    )
    # ---- WARM UP ENGINE HERE (non-blocking) ----
    client.loop.create_task(warmup_backend(lang_code, src_lang))

@client.tree.command(name="translit", description="Transliterate text", guild=guild)
@app_commands.describe(text="Text to transliterate")
async def tl(interaction: discord.Interaction, text: str):
    await interaction.response.defer()  # avoid unknown interaction

    lang_code = user_prefs_lang_codes.get(interaction.user.id, Lang.hi)
    src_lang = user_prefs_src_script_types.get(interaction.user.id, SrcLang.roman)
    if not lang_code or not src_lang:
        return await interaction.followup.send("Set your language first with /sl")
    
    res = await call_backend(text, lang_code, src_lang)
    await interaction.followup.send(res["output"])

client.run(TOKEN)
