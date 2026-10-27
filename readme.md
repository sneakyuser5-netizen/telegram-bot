
# Whisper AI — Telegram Bot

**Whisper AI** is a Python-powered Telegram bot developed by The-Whisperer. It combines conversational AI, VPN file distribution, digital-service information, user onboarding, and administrative tools in one platform.

The project is built with `python-telegram-bot`, SQLite, Flask, and multiple AI providers.

## Features

### Conversational AI
- AI-powered conversations for general questions and business enquiries.
- Context-aware follow-up responses using conversation history.
- Support for English and French conversations.
- Multiple AI providers with fallback routing.
- Business-specific answers based on the project's official service information.

### VPN Files and Digital Services
- Browse and search available VPN-related files.
- Access free VPN files through the bot's menu.
- View premium offers and training information.
- Receive tutorials and support guidance.

### User Management
- User registration and onboarding.
- Referral tracking and reward-related functionality.
- Download tracking and statistics.
- Channel membership checks where configured.

### Administration
- Upload, list, and delete files.
- Review file statistics and download totals.
- Back up and restore the SQLite database.
- Manage restoration workflows.
- Broadcast messages to registered users.

## AI Providers

The project currently includes integrations for:

| Provider | Configuration |
| --- | --- |
| Cloudflare Workers AI | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_MODEL` |
| Google Gemini | `GEMINI_API_KEY`, `GEMINI_MODEL` |
| OpenRouter | `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` |

The AI router attempts the configured providers in sequence. Actual availability depends on valid credentials, provider service status, account limits, and model availability.

## Official Services

### Biz Connect Academy (BCA)

Biz Connect Academy is an online learning platform offering practical digital-skills training.

Listed topics include:
- AI video creation
- WhatsApp bot creation
- Selling digital products
- Affiliate marketing
- TikTok monetization
- Virtual bank cards
- Growing social-network followers
- CapCut and Canva Pro
- Promo codes for 1xBet and MelBet
- Facebook and TikTok advertising campaigns

**Price:** 2,900 FCFA  
**Access:** Lifetime access  
**Registration:** https://bizconnectacademy.com/register?ref=ONLINECA

Supported countries include Burkina Faso, Cameroon, Chad, Central African Republic, Congo, Côte d'Ivoire, Gabon, Guinea, Guinea-Bissau, Mali, Niger, Senegal, Togo, Benin, Gambia, and the Democratic Republic of the Congo.

### Premium VPN
- Price: 500 FCFA
- Duration: 30 days
- Daily data allowance: 250 MB

### VPN Training
Practical training on creating, configuring, and managing VPN files. Pricing is negotiable.

### Free VPN Files
VPN files are made available through the bot and updated periodically.

### NIU Assistance
Assistance with obtaining a Numéro d'Identifiant Unique (NIU), the unique identification number used for relevant administrative and tax purposes in Cameroon.

**Listed price:** 1,000 FCFA.

### Contact and Support
- Telegram: https://t.me/The_whisperer237
- WhatsApp: +237 641 037 454

Service details and availability may change. The bot should not promise guaranteed income or results.

## Technology Stack

- **Language:** Python
- **Telegram framework:** `python-telegram-bot` 21.9
- **Database:** SQLite
- **Web endpoint:** Flask
- **Configuration:** `python-dotenv`
- **HTTP client:** `httpx`
- **AI integrations:** Cloudflare Workers AI, Google Gemini, OpenRouter

## Repository Structure

```text
telegram-bot/
├── bot.py
├── config.py
├── database.py
├── requirements.txt
├── check_db.py
├── fix_files_table.py
├── test_ai.py
├── commands/
│   └── Telegram command handlers
├── services/
│   ├── ai_engine.py
│   ├── ai_router.py
│   ├── cloudflare_service.py
│   ├── gemini_service.py
│   ├── openrouter_service.py
│   └── Business and file-management services
└── 
