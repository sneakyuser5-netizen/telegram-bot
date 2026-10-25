# Telegram Bot

A Python-based Telegram bot project built with `python-telegram-bot` and designed to manage a VPN file catalog, community access flow, AI-powered chat, and admin controls.

## Current repo status

- Language: Python (100%)
- Framework: `python-telegram-bot` 21.9
- Runtime: Python 3
- Persistence: SQLite (`database.db`)
- Web hook/health endpoint: Flask app running on a configurable port
- AI integrations: Cloudflare, Cerebras, and OpenRouter providers
- Bot features: user onboarding, referral tracking, file search/download, tutorials, premium offers, and admin tools

## Project overview

This repository contains a Telegram bot that:

- serves a main interactive menu for users
- allows browsing and requesting VPN-related files
- tracks user registrations and referrals in SQLite
- records file download stats
- exposes admin commands for backup/restore and file management
- integrates with AI services for conversational assistant behavior

## Repository structure

```text
.
├── bot.py                  # Main bot entry point and command/inline menu logic
├── config.py               # Environment configuration for Telegram and AI providers
├── database.py             # SQLite schema initialization
├── database.db             # Local SQLite database
├── requirements.txt        # Python dependencies
├── check_db.py             # Database validation helper
├── fix_files_table.py      # Database repair helper
├── sillydev.conf           # Runtime/service config file
├── test_ai.py              # AI provider smoke test
├── commands/               # Telegram command handlers
├── services/               # AI routing, file management, and business logic
└── .env                    # Local env file (not tracked in repo metadata, expected in deployment)
```

## Key functionality

### Bot logic
- `bot.py` initializes the bot, loads env settings, creates the menu, and registers command/handler callbacks.
- It uses `python-telegram-bot` to manage conversations, callback queries, and admin actions.
- A Flask app is also started in a background thread to expose a basic health endpoint at `/`.

### User + admin features
- Start flow for new users
- Referral and reward tracking
- Channel membership checks before accessing some flows
- File browsing/search for downloadable VPN resources
- Download statistics
- Admin file management and database backup/restore commands

### AI integration
- `services/ai_engine.py` and related modules route messages to AI providers
- `config.py` defines environment variables for Cloudflare, Cerebras, and OpenRouter
- `commands/chat_ai.py` sends user messages to the AI engine and returns responses

### Data layer
- SQLite tables are created in `database.py`
- `users` stores user registrations and referral metadata
- `downloads` tracks category download counts
- `files` stores file metadata such as category, size, and Telegram `file_id`

## Environment variables

The app expects the following values in a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_admin_user_id
CHANNEL_ID=your_channel_id
CHANNEL_LINK=https://t.me/yourchannel
WHATSAPP_URL=https://wa.me/your_number
PLATFORM_URL=https://example.com/platform

CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token
CLOUDFLARE_MODEL=@cf/meta/llama-3.1-8b-instruct

CEREBRAS_API_KEY=your_key
CEREBRAS_MODEL=llama-3.1-8b

OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then configure your environment variables and start the bot:

```bash
python bot.py
```

## Notes

This repository is currently a working Telegram bot codebase with active admin, file distribution, and AI assistant features. It is configured for deployment as a Python service and stores runtime data in a local SQLite database.

## Dependencies

Core dependencies from `requirements.txt`:

- `python-telegram-bot==21.9`
- `python-dotenv==1.0.1`
- `requests`
- `google-generativeai`
- `Flask`
- `httpx==0.27.2`

## License

No explicit license file is present in the repository snapshot reviewed, so licensing details should be confirmed before public or commercial reuse.
