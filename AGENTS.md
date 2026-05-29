# AGENTS.md — Discord Finance Tracker Bot

## Run

```bash
pip install -r requirements.txt
python bot.py
```

## Prerequisites

- `.env` with `DISCORD_TOKEN` (and optionally `GOOGLE_SHEET_NAME`, default `Finance Tracker`)
- `credentials.json` — Google Service Account key, gitignored
- Google Sheet shared with the service account email (Editor role)
- **Message Content Intent** must be enabled in Discord Developer Portal > Bot (required for the `on_message` auto-reply trigger)

## Env / Config

`config.py` reads env vars with defaults. `.env` is gitignored. **Never commit `.env` or `credentials.json`.**

`config.py` uses `GOOGLE_SHEET_NAME` env var — the existing `.env` file contains `SPREADSHEET_ID` which is **unused** by the current code (the sheet is opened by name via `gspread.Client.open()`).

## Architecture

Single-package Python app, no monorepo.

| File | Role |
|---|---|
| `bot.py` | Entrypoint. `asyncio.run(run_bot())` — sets up logging, loads `.env`, starts bot. Slash commands synced on every start in `on_ready()`. Also handles `on_message` auto-reply for "siapa wanita cantik" trigger. |
| `config.py` | Constants: token, sheet name, cooldown, sheet headers, log path |
| `commands.py` | All 8 slash commands defined inside `setup_commands(bot)`, registered via `bot.tree.add_command()`. Commands: `/masuk`, `/keluar`, `/balance`, `/report`, `/topuser`, `/recent`, `/help`, `/pdf` (image → PDF only) |
| `sheets_service.py` | Singleton `SheetsService` via `get_sheets_service()` module-level pattern. Authenticates with `credentials.json`, opens sheet by name. |
| `finance_service.py` | Singleton `FinanceService` via `get_finance_service()`. Uses `pandas` for aggregation. |

## Commands

All are slash commands. Amounts are in IDR (Rp). Cooldown: 3s per user (`config.COOLDOWN_TYPE = "user"`, `config.COOLDOWN_SECONDS = 3`).

Responses use `discord.Embed` — green for income, red for expenses, blue for balance/info, gold for reports.

## Tests

None. No test directory, no test framework configured.

## Style / Conventions

- Commands defined as inner functions inside `setup_commands(bot)`, decorated with `@app_commands.command`
- `amount` is `app_commands.Range[int, 1]` (must be positive), `/recent` limit is `app_commands.Range[int, 1, 10]`
- Currency formatting: `f'Rp {amount:,}'`
- Error responses sent with `ephemeral=True`
- Logging: `logging` module, format `%(asctime)s | %(levelname)s | %(message)s`, dual output to console and `logs/bot.log`

## Known quirks

- Slash commands are re-synced to Discord every time the bot starts (in `on_ready()`). This means startup takes a few extra seconds.
- `credentials.json` is checked for existence at startup but **not** required to start (warning only).
- The config `.env.example` documents `CREDENTIALS_FILE` and `GOOGLE_SHEET_NAME` env vars, but the repo's real `.env` uses `SPREADSHEET_ID` instead — this variable is not read by the current codebase.
- Auto-reply images are stored in `assets/img/`. The bot picks a random file when someone types "siapa wanita cantik" in any channel.
