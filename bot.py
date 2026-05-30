"""
Discord Finance Bot Main Module.
Entry point for the bot with logging and anti-spam features.
"""

import os
import random
import logging
import asyncio
from datetime import datetime
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

import config
from config import ANNIVERSARY_TEXT, ASSETS_DIR
from commands import setup_commands
from gallery import GalleryView


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

    check_anniversary.start()


# ==============================
# ON MESSAGE (Auto-reply trigger)
# ==============================

_anniversary_sent_date = None


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if "siapa wanita cantik menurut dapiw" in message.content.lower():
        images = list(ASSETS_DIR.iterdir())
        if images:
            chosen = random.choice(images)
            file = discord.File(chosen, filename="image.jpeg")
            embed = discord.Embed(
                description=(
                    "**Shalsabila Thabina Firdaus,**\n\n"
                    "Aku nggak tahu sejak kapan, tapi rasanya kamu sudah jadi bagian "
                    "dari banyak hal yang aku syukuri setiap hari. Ada sesuatu tentang "
                    "kamu yang selalu berhasil membuat semuanya terasa lebih ringan. "
                    "Bahkan di hari yang melelahkan, hanya melihat namamu muncul saja "
                    "kadang sudah cukup membuat suasana hati berubah jadi lebih baik.\n\n"
                    "Aku suka caramu tertawa, caramu bercerita, dan caramu menjadi "
                    "diri sendiri tanpa perlu berusaha menjadi orang lain. Mungkin kamu "
                    "nggak menyadarinya, tapi hal-hal sederhana yang kamu lakukan sering "
                    "kali meninggalkan kesan yang nggak sederhana.\n\n"
                    "Kalau ada satu hal yang ingin aku sampaikan, itu adalah terima "
                    "kasih. Terima kasih karena sudah hadir dan menjadi seseorang yang "
                    "begitu berarti. Semoga apa pun yang sedang kamu perjuangkan "
                    "berjalan lancar, dan semoga kebahagiaan selalu menemukan jalannya "
                    "untuk datang kepadamu.\n\n"
                    "Karena sejujurnya, melihat kamu bahagia adalah salah satu hal "
                    "yang membuatku ikut merasa bahagia."
                ),
                color=discord.Color.magenta()
            )
            embed.set_image(url="attachment://image.jpeg")
            embed.set_footer(text="- Dapiw")
            await message.channel.send(file=file, embed=embed)

    await bot.process_commands(message)


# ==============================
# ANNIVERSARY SCHEDULER
# ==============================

@tasks.loop(hours=1)
async def check_anniversary():

    global _anniversary_sent_date
    now = datetime.now()

    if (now.month, now.day) == (11, 28):

        if _anniversary_sent_date == now.date():
            return

        _anniversary_sent_date = now.date()
        logger.info("Triggering anniversary message!")

        channel = bot.get_channel(config.ANIVERSARY_CHANNEL_ID)

        if not channel:
            logger.error("Anniversary channel not found!")
            return

        await send_anniversary_message(channel)

    elif _anniversary_sent_date is not None:

        _anniversary_sent_date = None


@check_anniversary.before_loop
async def before_check_anniversary():

    await bot.wait_until_ready()


async def send_anniversary_message(channel):

    images = sorted(ASSETS_DIR.iterdir())

    if not images:
        logger.warning("No images found for anniversary")
        await channel.send(embed=discord.Embed(
            title="🎉 Happy Anniversary ❤️",
            description=ANNIVERSARY_TEXT,
            color=discord.Color.magenta()
        ))
        return

    first = images[0]
    file = discord.File(first, filename="gallery.jpeg")
    view = GalleryView(images, title="🎉 Happy Anniversary ❤️", description=ANNIVERSARY_TEXT)
    embed = view._build_embed()
    await channel.send(file=file, embed=embed, view=view)

    logger.info(f"Anniversary message sent with {len(images)} images")


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