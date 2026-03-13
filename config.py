"""
Configuration module for the Discord Finance Bot.
Handles environment variables and app settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Finance Tracker')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'credentials.json')

COOLDOWN_SECONDS = 3
COOLDOWN_TYPE = "user"

SHEET_HEADERS = ['Tanggal', 'User', 'Type', 'Amount', 'Description']

LOG_FILE = 'logs/bot.log'
