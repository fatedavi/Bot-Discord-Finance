# Discord Finance Tracker Bot

A Discord bot for tracking team income and expenses with Google Sheets integration.

## Features

- **Slash Commands**: Modern Discord interaction
- **Income Tracking**: Record income with `/masuk`
- **Expense Tracking**: Record expenses with `/keluar`
- **Balance Check**: View total balance with `/balance`
- **Monthly Report**: Financial summary with `/report`
- **Top Contributor**: See top income earner with `/topuser`
- **Recent Transactions**: View last transactions with `/recent`
- **Anti-Spam**: 3-second cooldown per user
- **Logging**: All commands logged to `logs/bot.log`

## Commands

| Command | Description |
|---------|-------------|
| `/masuk <amount> <description>` | Record income |
| `/keluar <amount> <description>` | Record expense |
| `/balance` | Check total balance |
| `/report` | Monthly financial report |
| `/topuser` | Top income contributor |
| `/recent [limit]` | Recent transactions (max 10) |
| `/help` | Show all commands |

## Project Structure

```
finance-discord-bot/
├── bot.py              # Main bot entry point
├── config.py           # Configuration settings
├── commands.py         # All slash commands
├── sheets_service.py   # Google Sheets integration
├── finance_service.py  # Financial calculations
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── credentials.json    # Google Service Account (you need to download)
├── logs/
│   └── bot.log         # Command logs
└── README.md
```

## Google Sheets Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **New Project** and give it a name
3. Wait for the project to be created

### 2. Enable APIs

1. Go to **APIs & Services** > **Library**
2. Search and enable:
   - **Google Sheets API**
   - **Google Drive API**

### 3. Create Service Account

1. Go to **IAM & Admin** > **Service Accounts**
2. Click **Create Service Account**
3. Fill in details:
   - Name: `finance-bot`
   - ID: `finance-bot`
4. Click **Done** (no need for IAM roles)
5. Click on the created service account
6. Go to **Keys** tab
7. Click **Add Key** > **Create new key**
8. Select **JSON** format
9. Click **Create** and download the file

### 4. Save Credentials

1. Rename the downloaded JSON file to `credentials.json`
2. Place it in the project root folder

### 5. Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet named **Finance Tracker**
3. Add headers in row 1:
   | A | B | C | D | E |
   |---|---|---|---|---|
   | Tanggal | User | Type | Amount | Description |

### 6. Share Spreadsheet

1. Open your Google Sheet
2. Click **Share**
3. Enter the service account email (found in your `credentials.json` file as `client_email`)
4. Set as **Editor**
5. Click **Send**

## Discord Bot Setup

### 1. Create Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Give it a name (e.g., "Finance Bot")

### 2. Create Bot

1. Go to **Bot** in the left sidebar
2. Click **Reset Token** and copy it
3. Enable **Message Content Intent** in the Bot settings

### 3. Generate Invite Link

1. Go to **OAuth2** > **URL Generator**
2. Under **Scopes**, check `bot`
3. Under **Bot Permissions**, check:
   - `Send Messages`
   - `Read Message History`
   - `Use Slash Commands`
4. Copy the generated URL
5. Open the URL in your browser
6. Select your Discord server and authorize

## Installation

### 1. Install Python

Make sure you have Python 3.8+ installed:
```bash
python --version
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` file:
```
DISCORD_TOKEN=your_actual_discord_bot_token
GOOGLE_SHEET_NAME=Finance Tracker
```

## Running Locally

```bash
python bot.py
```

You should see:
```
2026-03-13 10:00:00 | INFO | Bot BotName#1234 is ready!
2026-03-13 10:00:00 | INFO | Slash commands registered successfully
```

## Deploy to SkyBots (or similar hosting)

### Option 1: GitHub Deployment

1. Create a GitHub repository
2. Push your code (exclude `.env` and `credentials.json`)
3. Add these environment variables in SkyBots dashboard:
   - `DISCORD_TOKEN`
   - `GOOGLE_SHEET_NAME`
4. Upload `credentials.json` via the hosting panel
5. Set start command: `python bot.py`

### Option 2: Manual Deployment

1. Upload all files to your server
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run with: `python bot.py`

### Using Process Manager (PM2)

```bash
# Install PM2
npm install -g pm2

# Start bot
pm2 start bot.py --name finance-bot

# View logs
pm2 logs finance-bot

# Restart
pm2 restart finance-bot
```

## Google Sheet Example

| Tanggal | User | Type | Amount | Description |
|---------|------|------|--------|-------------|
| 2026-03-13 10:30:00 | Davi | Income | 50000 | Desain logo |
| 2026-03-13 11:00:00 | Davi | Expense | 25000 | Makan siang |
| 2026-03-13 14:00:00 | Budi | Income | 100000 | Freelance project |

## Troubleshooting

### Bot not responding to commands?
- Make sure the bot has permission to read/write messages
- Try restarting the bot
- Check if slash commands are registered

### Google Sheets errors?
- Verify `credentials.json` is in the correct location
- Check that the spreadsheet is shared with the service account email
- Ensure the spreadsheet name matches `GOOGLE_SHEET_NAME`

### Cooldown message?
- Wait 3 seconds between commands
- This is to prevent spam

## License

MIT License
# Bot-Discord-Finance
