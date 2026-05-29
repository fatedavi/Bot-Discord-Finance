"""
Discord Finance Bot Main Module.
Entry point for the bot with logging and anti-spam features.
"""

import os
import random
import pathlib
import logging
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

import config
from commands import setup_commands


# ==============================
# LOGGING SETUP
# ==============================

def setup_logging() -> logging.Logger:

    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("discord_bot")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()


# ==============================
# LOAD ENV
# ==============================

def load_env():

    load_dotenv()

    if not os.getenv("DISCORD_TOKEN"):
        logger.error("DISCORD_TOKEN not found in .env")
        return False

    if not os.path.exists(config.CREDENTIALS_FILE):
        logger.warning(
            f"Credentials file '{config.CREDENTIALS_FILE}' not found"
        )

    return True


# ==============================
# BOT SETUP
# ==============================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


# ==============================
# READY EVENT
# ==============================

@bot.event
async def on_ready():

    logger.info(f"Bot {bot.user} is ready!")
    logger.info(f"Bot ID: {bot.user.id}")

    try:

        await setup_commands(bot)

        # sync slash command ke discord
        synced = await bot.tree.sync()

        logger.info(f"Synced {len(synced)} commands")

    except Exception as e:

        logger.error(f"Failed to register commands: {e}")


# ==============================
# ON MESSAGE (Auto-reply trigger)
# ==============================

ASSETS_DIR = pathlib.Path("assets/img")


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if "siapa wanita cantik" in message.content.lower():
        images = list(ASSETS_DIR.iterdir())
        if images:
            chosen = random.choice(images)
            await message.channel.send(file=discord.File(chosen))

    await bot.process_commands(message)


# ==============================
# ERROR HANDLER
# ==============================

@bot.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.CommandOnCooldown):

        await ctx.send(
            f"⏳ Slow down! Try again in {error.retry_after:.1f}s"
        )

    elif isinstance(error, commands.MissingRequiredArgument):

        await ctx.send(
            f"❌ Missing argument: {error.param.name}"
        )

    elif isinstance(error, commands.BadArgument):

        await ctx.send(
            "❌ Invalid argument"
        )

    else:

        logger.error(f"Command error: {error}")
        await ctx.send("❌ Unexpected error occurred")


# ==============================
# RUN BOT
# ==============================

async def run_bot():

    if not load_env():
        logger.error("Environment failed to load")
        return

    try:

        logger.info("Starting bot...")

        await bot.start(config.DISCORD_TOKEN)

    except KeyboardInterrupt:

        logger.info("Bot shutting down...")
        await bot.close()

    except Exception as e:

        logger.error(f"Unexpected error: {e}")


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    try:
        asyncio.run(run_bot())

    except KeyboardInterrupt:

        logger.info("Bot stopped.")