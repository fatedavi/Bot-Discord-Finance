"""
Configuration module for the Discord Finance Bot.
Handles environment variables and app settings.
"""
import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Finance Tracker')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'credentials.json')

COOLDOWN_SECONDS = 3
COOLDOWN_TYPE = "user"

SHEET_HEADERS = ['Tanggal', 'User', 'Type', 'Amount', 'Description']

LOG_FILE = 'logs/bot.log'

ANIVERSARY_CHANNEL_ID = 1469735670976348326
ASSETS_DIR = pathlib.Path("assets/img")
ANNIVERSARY_TEXT = (
    "**Happy Anniversary, Sayangkuuu** ❤️\n\n"
    "Nggak terasa ya, kita udah setahun aja. Rasanya baru kemarin "
    "kita memulai semuanya, saling mengenal, saling memahami, sampai akhirnya "
    "bisa melewati banyak hal bersama.\n\n"
    "Terima kasih sudah menjadi bagian dari perjalanan hidupku. Terima kasih "
    "untuk setiap tawa, cerita, perhatian, dan semua momen yang sudah kita "
    "lewati bersama. Mungkin hubungan kita nggak selalu sempurna, tapi aku "
    "bersyukur karena kita selalu berusaha untuk tetap berjalan berdampingan.\n\n"
    "Aku berharap hari ini bukan hanya menjadi pengingat tentang berapa lama "
    "kita bersama, tapi juga tentang betapa berharganya setiap waktu yang sudah "
    "kita lalui. Semoga ke depannya kita masih bisa membuat lebih banyak "
    "kenangan, merayakan lebih banyak pencapaian, dan saling menemani dalam "
    "keadaan apa pun.\n\n"
    "Aku mungkin tidak selalu bisa mengungkapkan semuanya dengan kata-kata, "
    "tapi satu hal yang pasti, aku sangat bersyukur karena ada kamu di hidupku.\n\n"
    "Selamat anniversary, sayang. Terima kasih sudah bertahan, terima kasih "
    "sudah percaya, dan terima kasih sudah menjadi rumah yang selalu ingin "
    "aku tuju.\n\n"
    "Aku sayang kamu, hari ini, besok, dan seterusnya. ❤️✨\n\n"
    "— Dari seseorang yang selalu bersyukur memilikimu."
)
