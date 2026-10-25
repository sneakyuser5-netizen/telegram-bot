# Telegram Bot

A Python Telegram bot project built with `python-telegram-bot` and designed for VPN file distribution, AI-powered chat, user onboarding, and admin management.

## Current repository status

- Language: Python (100%)
- Primary framework: `python-telegram-bot` 21.9
- Persistence: SQLite (`database.db`)
- Web layer: Flask health endpoint on a configurable port
- AI providers: Cloudflare, Cerebras, and OpenRouter
- Core functionality: user registration, referrals, file browsing/search, download tracking, tutorials, premium offers, and admin tools

## Overview

This bot provides an interactive Telegram interface for users to:

- access curated VPN-related files
- search and download available files
- view free/premium product offers and training content
- interact with an AI assistant for general chat
- receive support and tutorial guidance

Administrators can also:

- upload and remove files
- review download statistics
- manage database backups/restores
- broadcast messages to registered users

## Repository structure

```text
.
├── bot.py               # Main bot entry point and callback/menu logic
├── config.py            # Environment configuration for Telegram and AI providers
├── database.py          # SQLite database initialization and schema setup
├── database.db          # Local SQLite database file
├── requirements.txt     # Python package dependencies
├── check_db.py          # Database validation helper
├── fix_files_table.py   # SQLite repair helper
├── sillydev.conf        # Runtime or deployment configuration
├── test_ai.py           # AI provider smoke test
├── commands/            # Telegram command handlers and flows
├── services/            # AI logic, file management, and business services
├── .env                 # Local environment file (expected in deployment)
└── README.md            # Project documentation
```

## Main features

### Bot experience
- interactive start menu and user onboarding
- referral tracking with reward logic
- channel membership verification before some actions
- searchable file access flow
- support, tutorials, and promotional sections

### Admin capabilities
- add/list/delete stored files
- view file statistics and download totals
- backup and restore SQLite data
- apply restore actions
- broadcast messages to bot users

### AI integration
`config.py` defines environment-based access for:

- Cloudflare
- Cerebras
- OpenRouter

The `commands/chat_ai.py` handler routes user messages to the AI engine via `services.ai_engine`, enabling assistant-style responses in chat.

### Data layer
The SQLite tables created in `database.py` include:

- `users`: user ID, referral details, reward state, join date
- `downloads`: category download counters
- `files`: file metadata like category, size, file IDs, creation time

## Environment configuration

Create a `.env` file with values similar to the following:

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

Then start the bot:

```bash
python bot.py
```

## Dependencies

Installed from `requirements.txt`:

- `python-telegram-bot==21.9`
- `python-dotenv==1.0.1`
- `requests`
- `google-generativeai`
- `Flask`
- `httpx==0.27.2`

## Notes

This repository is a working Telegram bot codebase for a file-sharing and support workflow, with active AI integration and admin controls. It is designed to run as a Python service and stores runtime state in a local SQLite database.

No explicit license file was found in the reviewed repository snapshot, so licensing terms should be confirmed before public or commercial reuse.
