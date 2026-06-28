#!/usr/bin/env python3

import os
import sqlite3
import logging
from datetime import datetime
from dotenv import load_dotenv
import time

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from commands.addfile import addfile_handler
from database import init_db
from commands.testfile import testfile_handler
from services.files import (
    get_file,
    record_download,
    list_files_info,
    get_download_stats,
    delete_file
)
from commands.listfiles import listfiles_handler
from commands.deletefile import deletefile_handler
from commands.backupdb import backupdb_handler
from commands.restoredb import restoredb_handler
from commands.applyrestore import applyrestore_handler
from commands.filestats import filestats_handler
from commands.adminpanel import adminpanel_handler

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "")
WHATSAPP_URL = os.getenv("WHATSAPP_URL", "")
PLATFORM_URL = os.getenv("PLATFORM_URL", "")

DB = "database.db"
SEARCH_MODE = {}
BOT_START_TIME = time.time()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def db():
    return sqlite3.connect(DB)


def user_exists(user_id):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE user_id=?", (str(user_id),))
    row = cur.fetchone()
    conn.close()
    return row is not None


def add_user(user_id, referred_by=None):
    conn = db()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id, referrals, referred_by, reward_unlocked, joined_at)
        VALUES (?,0,?,0,?)
        """,
        (str(user_id), referred_by, datetime.now().strftime("%d/%m/%Y"))
    )
    conn.commit()
    conn.close()


def get_user(user_id):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (str(user_id),))
    row = cur.fetchone()
    conn.close()
    return row


def total_users():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    conn.close()
    return count


async def is_joined(context, user_id):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False


def get_uptime():
    seconds = int(time.time() - BOT_START_TIME)
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    return f"{days}d {hours}h {minutes}m"


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎁 Fichier gratuit (7 jours)", callback_data="free")],
        [InlineKeyboardButton("📈 Fichiers Populaires", callback_data="popular_files")],
        [InlineKeyboardButton("🎓 Tutoriels", callback_data="tutorials")],
        [InlineKeyboardButton("📡 VPN Premium (30 jours)", callback_data="premium")],
        [InlineKeyboardButton("🎓 Plateforme de formation", callback_data="platform")],
        [InlineKeyboardButton("🌐 Formation VPN", callback_data="vpn")],
        [InlineKeyboardButton("📰 ℹ️ Informations", callback_data="referral")],
        [InlineKeyboardButton("📝 Demander un fichier", callback_data="request_file")],
        [InlineKeyboardButton("📊 Mes Statistiques", callback_data="stats")],
        [InlineKeyboardButton("🆘 Assistance", callback_data="support")],
        [InlineKeyboardButton("🆕 Nouveaux fichiers", callback_data="new_files")],
        [InlineKeyboardButton("📢 Rejoindre la chaîne", url=CHANNEL_LINK)]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref = None

    if context.args:
        ref = context.args[0]

    new_user = not user_exists(user_id)

    if new_user:
        add_user(user_id, ref if ref != user_id else None)

        if ref and ref != user_id and user_exists(ref):
            conn = db()
            cur = conn.cursor()

            cur.execute(
                "UPDATE users SET referrals=referrals+1 WHERE user_id=?",
                (ref,)
            )

            cur.execute(
                "SELECT referrals,reward_unlocked FROM users WHERE user_id=?",
                (ref,)
            )

            refs, reward = cur.fetchone()

            if refs >= 2 and reward == 0:
                cur.execute(
                    "UPDATE users SET reward_unlocked=1 WHERE user_id=?",
                    (ref,)
                )
                conn.commit()

            conn.commit()
            conn.close()

    me = await context.bot.get_me()
    ref_link = f"https://t.me/{me.username}?start={user_id}"

    user = get_user(user_id)
    referrals = user[1] if user else 0

    await update.message.reply_text(
        f"🎯 BIENVENUE 👋\n\n"
        f"👥 Utilisateurs : {total_users()}\n\n"
        f"🚀 Accédez gratuitement à nos fichiers VPN configurés.\n\n"
        f"✅ Fichiers gratuits (7 jours)\n"
        f"✅ VPN Premium (30 jours)\n"
        f"✅ Formation VPN\n"
        f"✅ Plateforme de formation\n\n"
        f"👇 Explorez les options ci-dessous :",
        reply_markup=menu()
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    uid = q.from_user.id
    data = q.data

    # Admin protection
    if data.startswith("admin_") and uid != ADMIN_ID:
        return

    # Channel join check
    if not await is_joined(context, uid):
        await q.message.reply_text(
            "⚠️ Rejoins la chaîne pour continuer.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Rejoindre", url=CHANNEL_LINK)]
            ])
        )
        return

    # =========================
    # ADMIN MENU
    # =========================

    if data == "admin_menu":
        await q.edit_message_text(
            "🔧 ADMIN PANEL",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📂 Files", callback_data="admin_files")],
                [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
                [InlineKeyboardButton("💾 Database", callback_data="admin_db")],
                [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")]
            ])
        )
        return

    if data == "admin_files":
        await q.edit_message_text(
            "📂 FILE MANAGEMENT",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Add File", callback_data="admin_addfile")],
                [InlineKeyboardButton("📋 List Files", callback_data="admin_listfiles")],
                [InlineKeyboardButton("🗑 Delete File", callback_data="admin_deletefile")],
                [InlineKeyboardButton("📈 Download Stats", callback_data="admin_filestats")],
                [InlineKeyboardButton("🔙 Back", callback_data="admin_menu")]
            ])
        )
        return

    if data == "admin_db":
        await q.edit_message_text(
            "💾 DATABASE MANAGEMENT",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📥 Backup DB", callback_data="admin_backupdb")],
                [InlineKeyboardButton("📤 Restore DB", callback_data="admin_restoredb")],
                [InlineKeyboardButton("🔄 Apply Restore", callback_data="admin_applyrestore")],
                [InlineKeyboardButton("🔙 Back", callback_data="admin_menu")]
            ])
        )
        return

    if data == "admin_backupdb":
        await q.edit_message_text("📥 Use:\n\n/backupdb")
        return

    if data == "admin_restoredb":
        await q.edit_message_text("📤 Use:\n\n/restoredb")
        return

    if data == "admin_applyrestore":
        await q.edit_message_text("🔄 Use:\n\n/applyrestore")
        return

    if data == "admin_broadcast":
        await q.edit_message_text(
            "📢 BROADCAST\n\nUse:\n/broadcast Your message"
        )
        return

    # =========================
    # STATS
    # =========================

    if data == "admin_stats":
        total_files = len(list_files_info())
        total_downloads = 0
        users = total_users()

        stats = get_download_stats()
        for category, count in stats:
            total_downloads += count

        uptime = get_uptime()

        await q.edit_message_text(
            "📊 BOT STATISTICS\n\n"
            f"👥 Total Users: {users}\n"
            f"📂 Total Files: {total_files}\n"
            f"📥 Total Downloads: {total_downloads}\n"
            f"⏱ Uptime: {uptime}"
        )
        return

    if data == "admin_filestats":
        stats = get_download_stats()

        if not stats:
            await q.edit_message_text("📊 No downloads recorded yet.")
            return

        text = "📊 Download Statistics\n\n"

        for category, count in stats:
            text += f"✅ {category} → {count}\n"

        await q.edit_message_text(text)
        return

    # =========================
    # FILES
    # =========================

    if data == "admin_listfiles":
        files = list_files_info()

        if not files:
            await q.edit_message_text("❌ No files stored.")
            return

        text = "📂 Stored Files\n\n"

        for category, size, created_at in files:
            try:
                size_mb = round(int(size) / 1024 / 1024, 2)
                size_text = f"{size_mb} MB"
            except Exception:
                size_text = size

            text += (
                f"✅ {category}\n"
                f"📦 Size: {size_text}\n"
                f"📅 Uploaded: {created_at}\n\n"
            )

        await q.edit_message_text(text)
        return

    if data == "admin_deletefile":
        files = list_files_info()

        if not files:
            await q.edit_message_text("❌ No files to delete.")
            return

        keyboard = []

        for category, size, created_at in files:
            keyboard.append([
                InlineKeyboardButton(
                    f"🗑 {category}",
                    callback_data=f"del_{category}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton("🔙 Back", callback_data="admin_files")
        ])

        await q.edit_message_text(
            "🗑 SELECT FILE TO DELETE",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if data.startswith("del_"):
        category = data.replace("del_", "")

        await q.edit_message_text(
            f"⚠️ Delete {category.upper()}?",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Confirm", callback_data=f"confirmdel_{category}"),
                InlineKeyboardButton("❌ Cancel", callback_data="admin_deletefile")
            ]])
        )
        return

    if data.startswith("confirmdel_"):
        category = data.replace("confirmdel_", "")
        delete_file(category)

        await q.edit_message_text(
            f"✅ {category.upper()} deleted successfully."
        )
        return

    if data == "admin_addfile":
        await q.edit_message_text(
            "📤 Use:\n\n/addfile\n\nThen send the file."
        )
        return

    # =========================
    # FILE ACCESS MENU
    # =========================

    if data == "files_menu":
        await q.edit_message_text(
            "📂 Choose a VPN type:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⚡ HA Tunnel", callback_data="file_hat")],
                [InlineKeyboardButton("📡 SocksIP", callback_data="file_sip")],
                [InlineKeyboardButton("📶 NetMod", callback_data="file_nm")],
                [InlineKeyboardButton("💉 HTTP Injector", callback_data="file_ehi")],
                [InlineKeyboardButton("🔐 HTTP Custom", callback_data="file_hc")],
                [InlineKeyboardButton("🚀 SSH Custom", callback_data="file_ssc")],
                [InlineKeyboardButton("🌐 NPV Tunnel", callback_data="file_npvt")],
                [InlineKeyboardButton("☁️ V2Ray", callback_data="file_v2ray")],
                [InlineKeyboardButton("🔗 LinkLayer", callback_data="file_ink")],
                [InlineKeyboardButton("🌙 Dark Tunnel", callback_data="file_dark")],
                [InlineKeyboardButton("🛡 ZiVPN", callback_data="file_ziv")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data.startswith("file_"):
        category = data.replace("file_", "")
        file_id = get_file(category)

        if not file_id:
            await q.message.reply_text(
                f"❌ No {category.upper()} file available."
            )
            return

        record_download(category)
        await q.message.reply_document(file_id)
        return

    if data == "free":
        await q.edit_message_text(
            "🎁 FICHIERS GRATUITS (7 JOURS)\n\n👇 Accédez aux fichiers disponibles :",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📂 Browse Files", callback_data="files_menu")],
                [InlineKeyboardButton("🔎 Search Files", callback_data="search_files")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "search_files":
        SEARCH_MODE[uid] = True
        await q.edit_message_text(
            "🔍 RECHERCHE DE FICHIERS\n\n"
            "✍️ Envoyez un mot-clé pour rechercher un fichier VPN.\n\n"
            "Exemples :\n"
            "- v2ray\n"
            "- http\n"
            "- ssh\n\n"
            "🚀 Tapez maintenant votre recherche :",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Menu", callback_data="menu")]
            ])
        )
        return

    if data == "vpn":
        await q.edit_message_text(
            "🌐 FORMATION VPN\n\n"
            "Apprenez à créer et configurer vos propres fichiers VPN.\n\n"
            "✅ Création de fichiers VPN\n"
            "✅ Techniques et astuces pratiques\n"
            "✅ Accompagnement personnalisé\n"
            "✅ Méthodes simples à appliquer\n"
            "✅ Possibilité de générer des revenus\n\n"
            "💰 Prix abordable et négociable\n\n"
            "📩 Contactez-nous directement sur WhatsApp pour plus d'informations.\n\n"
            "👇 Cliquez sur le bouton ci-dessous.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 WhatsApp", url=WHATSAPP_URL)],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "premium":
        await q.edit_message_text(
            "📡 VPN PREMIUM (30 JOURS)\n\n"
            "🚀 Profitez d'une connexion rapide, stable et sécurisée pendant 30 jours.\n\n"
            "✅ 250 MB / jour\n"
            "✅ Connexion rapide et fluide\n"
            "✅ Stable pour la navigation\n"
            "✅ Assistance disponible\n\n"
            "💰 Tarif : 500 FCFA\n\n"
            "📩 Pour activer votre abonnement ou obtenir plus d'informations, contactez-nous directement sur WhatsApp.\n\n"
            "👇 Cliquez sur le bouton ci-dessous.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 WhatsApp", url=WHATSAPP_URL)],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "platform":
        await q.edit_message_text(
            "🚀 BCA – LISTE DES FORMATIONS COMPLÈTES\n"
            "100% GRATUITES\n\n"
            "📚 Formations disponibles :\n"
            "• Formation en Intelligence Artificielle (IA)\n"
            "• Formation complète Facebook Ads\n"
            "• Comment créer un bot WhatsApp\n"
            "• Vente de produits digitaux\n"
            "• Marketing d'affiliation\n"
            "• Compte TikTok monétisé\n"
            "• Publicité Facebook & TikTok\n"
            "• CANAL+ gratuitement\n"
            "• CapCut et Canva Pro à vie\n"
            "• Code promo 1XBET et MELBET\n"
            "• Booster les abonnés\n"
            "• Carte Visa virtuelle\n\n"
            "💳 Inscription à vie : 1900 FCFA\n\n"
            "👇 Accédez à la plateforme :",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎓 Plateforme BCA", url=PLATFORM_URL)],
                [InlineKeyboardButton("📩 WhatsApp", url=WHATSAPP_URL)],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "request_file":
        await q.edit_message_text(
            "📝 DEMANDE DE FICHIER VPN\n\n"
            "📩 Contactez l'administrateur pour demander un fichier spécifique.\n\n"
            "Indiquez :\n"
            "• Le type VPN\n"
            "• Le réseau (MTN, Orange, Camtel...)\n"
            "• Le volume souhaité\n\n"
            "👤 Contact admin : @The_whisperer237",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "referral":
        await q.edit_message_text(
            "👥 COMMUNAUTÉ VPN\n\n"
            "🚀 Merci d'utiliser notre plateforme VPN.\n\n"
            "📂 Fichiers VPN gratuits disponibles\n"
            "🛰 VPN Premium disponibles\n"
            "🎓 Formation VPN\n"
            "🛠 Assistance et support\n\n"
            "🔔 De nouvelles fonctionnalités seront bientôt ajoutées.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "stats":
        user = get_user(uid)
        await q.edit_message_text(
            f"📊 MES STATISTIQUES\n\n"
            f"👤 ID : {uid}\n"
            f"📅 Inscrit le : {user[4]}\n\n"
            f"🚀 Merci d'utiliser notre plateforme VPN.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "tutorials":
        await q.edit_message_text(
            "🎓 TUTORIELS VPN\n\n"
            "Choisissez un tutoriel :",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📥 Importer un fichier HAT", callback_data="tutorial_hat")],
                [InlineKeyboardButton("📥 Importer un fichier EHI", callback_data="tutorial_ehi")],
                [InlineKeyboardButton("📥 Importer un fichier SocksIP", callback_data="tutorial_sip")],
                [InlineKeyboardButton("📥 Importer un fichier Dark Tunnel", callback_data="tutorial_dark")],
                [InlineKeyboardButton("📥 Importer un fichier ZiVPN", callback_data="tutorial_ziv")],
                [InlineKeyboardButton("📥 Importer un fichier NPVT", callback_data="tutorial_npvt")],
                [InlineKeyboardButton("📥 Importer un fichier SSC", callback_data="tutorial_ssc")],
                [InlineKeyboardButton("📥 Importer un fichier V2Ray", callback_data="tutorial_v2ray")],
                [InlineKeyboardButton("📥 Importer un fichier LinkLayer", callback_data="tutorial_linklayer")],
                [InlineKeyboardButton("📥 Importer un fichier HTTP Custom", callback_data="tutorial_hc")],
                [InlineKeyboardButton("📥 Importer un fichier NetMod", callback_data="tutorial_nm")],
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "tutorial_hat":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER HAT\n\n"
            "1️⃣ Installez HA Tunnel Plus.\n\n"
            "2️⃣ Téléchargez le fichier .hat depuis ce bot.\n\n"
            "3️⃣ Ouvrez HA Tunnel Plus.\n\n"
            "4️⃣ Cliquez sur IMPORT.\n\n"
            "5️⃣ Sélectionnez votre fichier .hat.\n\n"
            "6️⃣ Connectez-vous.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_ehi":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER EHI\n\n"
            "1️⃣ Installez HTTP Injector.\n\n"
            "2️⃣ Téléchargez le fichier .ehi depuis ce bot.\n\n"
            "3️⃣ Ouvrez HTTP Injector.\n\n"
            "4️⃣ Cliquez sur Import Config.\n\n"
            "5️⃣ Sélectionnez votre fichier .ehi.\n\n"
            "6️⃣ Démarrez la connexion.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_npvt":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER NPVT\n\n"
            "1️⃣ Installez NPV Tunnel.\n\n"
            "2️⃣ Téléchargez le fichier .npvt depuis ce bot.\n\n"
            "3️⃣ Ouvrez NPV Tunnel.\n\n"
            "4️⃣ Cliquez sur Importer.\n\n"
            "5️⃣ Sélectionnez votre fichier .npvt.\n\n"
            "6️⃣ Connectez-vous.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_ssc":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER SSC\n\n"
            "1️⃣ Installez SSH Custom.\n\n"
            "2️⃣ Téléchargez le fichier .ssc depuis ce bot.\n\n"
            "3️⃣ Ouvrez SSH Custom.\n\n"
            "4️⃣ Cliquez sur Import Config.\n\n"
            "5️⃣ Sélectionnez votre fichier .ssc.\n\n"
            "6️⃣ Lancez la connexion.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_v2ray":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER V2RAY\n\n"
            "1️⃣ Installez V2RayNG ou V2Ray VPN.\n\n"
            "2️⃣ Téléchargez le fichier V2Ray depuis ce bot.\n\n"
            "3️⃣ Ouvrez l'application.\n\n"
            "4️⃣ Cliquez sur Importer.\n\n"
            "5️⃣ Sélectionnez votre fichier.\n\n"
            "6️⃣ Lancez la connexion.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_linklayer":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER LINKLAYER\n\n"
            "1️⃣ Installez LinkLayer VPN.\n\n"
            "2️⃣ Téléchargez le fichier depuis ce bot.\n\n"
            "3️⃣ Ouvrez LinkLayer.\n\n"
            "4️⃣ Cliquez sur Import Config.\n\n"
            "5️⃣ Sélectionnez le fichier téléchargé.\n\n"
            "6️⃣ Connectez-vous.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_hc":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER HTTP CUSTOM\n\n"
            "1️⃣ Installez HTTP Custom.\n\n"
            "2️⃣ Téléchargez le fichier depuis ce bot.\n\n"
            "3️⃣ Ouvrez HTTP Custom.\n\n"
            "4️⃣ Cliquez sur Import Config.\n\n"
            "5️⃣ Sélectionnez votre fichier.\n\n"
            "6️⃣ Démarrez la connexion.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_nm":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER NETMOD\n\n"
            "1️⃣ Installez NetMod VPN.\n\n"
            "2️⃣ Téléchargez le fichier depuis ce bot.\n\n"
            "3️⃣ Ouvrez NetMod.\n\n"
            "4️⃣ Cliquez sur Import Config.\n\n"
            "5️⃣ Sélectionnez votre fichier.\n\n"
            "6️⃣ Connectez-vous.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_sip":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER SOCKSIP\n\n"
            "1️⃣ Installez SocksIP Tunnel.\n\n"
            "2️⃣ Téléchargez le fichier depuis ce bot.\n\n"
            "3️⃣ Ouvrez SocksIP Tunnel.\n\n"
            "4️⃣ Cliquez sur Import Config.\n\n"
            "5️⃣ Sélectionnez votre fichier.\n\n"
            "6️⃣ Connectez-vous.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_dark":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER DARK TUNNEL\n\n"
            "1️⃣ Installez Dark Tunnel.\n\n"
            "2️⃣ Téléchargez le fichier depuis ce bot.\n\n"
            "3️⃣ Ouvrez Dark Tunnel.\n\n"
            "4️⃣ Cliquez sur Importer.\n\n"
            "5️⃣ Sélectionnez votre fichier.\n\n"
            "6️⃣ Lancez la connexion.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "tutorial_ziv":
        await q.edit_message_text(
            "🎓 COMMENT IMPORTER UN FICHIER ZIVPN\n\n"
            "1️⃣ Installez ZiVPN.\n\n"
            "2️⃣ Téléchargez le fichier depuis ce bot.\n\n"
            "3️⃣ Ouvrez ZiVPN.\n\n"
            "4️⃣ Cliquez sur Import Config.\n\n"
            "5️⃣ Sélectionnez votre fichier.\n\n"
            "6️⃣ Connectez-vous.\n\n"
            "✅ Terminé.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Tutoriels", callback_data="tutorials")]
            ])
        )
        return

    if data == "support":
        await q.edit_message_text(
            "🆘 ASSISTANCE\n\n"
            "❓ Besoin d'aide ?\n"
            "📩 Contactez l'administrateur.\n\n"
            "👤 Support : @The_whisperer237\n\n"
            "⏰ Réponse généralement rapide.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "new_files":
        await q.edit_message_text(
            "🆕 NOUVEAUX FICHIERS\n\n"
            "🚧 Fonction en cours d'amélioration.\n\n"
            "📂 Les derniers fichiers ajoutés seront affichés ici automatiquement.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Menu", callback_data="menu")]
            ])
        )
        return

    if data == "popular_files":
        stats = get_download_stats()
        text = "📈 FICHIERS POPULAIRES\n\n"

        if not stats:
            text += "Aucune statistique disponible."
        else:
            medals = ["🥇", "🥈", "🥉"]

            for i, row in enumerate(stats[:3]):
                category = row[0].upper()
                count = row[1]
                medal = medals[i] if i < 3 else "📂"
                text += f"{medal} {category} — {count} téléchargements\n"

            text += "\n🔥 Les fichiers les plus utilisés par la communauté."

        await q.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Menu", callback_data="menu")]
            ])
        )
        return

    if data == "menu":
        await q.edit_message_text(
            "🎯 MENU PRINCIPAL\n\n"
            "Sélectionnez une option :",
            reply_markup=menu()
        )
        return


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.lower()

    if SEARCH_MODE.get(user_id):
        conn = db()
        cur = conn.cursor()

        cur.execute(
            "SELECT name, file_id FROM files WHERE name LIKE ?",
            (f"%{text}%",)
        )

        results = cur.fetchall()
        conn.close()

        SEARCH_MODE[user_id] = False

        if not results:
            await update.message.reply_text("❌ Aucun fichier trouvé.")
            return

        msg = "🔍 Résultats :\n\n"

        for name, file_id in results:
            msg += f"📁 {name}\n"

        await update.message.reply_text(msg)
        return


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    msg = " ".join(context.args)
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    users = cur.fetchall()
    conn.close()

    sent = 0
    for u in users:
        try:
            await context.bot.send_message(int(u[0]), msg)
            sent += 1
        except Exception:
            pass

    await update.message.reply_text(f"✅ Envoyé à {sent} utilisateurs")


async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        f"📊 Statistiques\n\n👥 Utilisateurs : {total_users()}"
    )


def main():
    init_db()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("stats", stats_cmd))

    app.add_handler(listfiles_handler)
    app.add_handler(deletefile_handler)
    app.add_handler(addfile_handler)
    app.add_handler(testfile_handler)
    app.add_handler(backupdb_handler)
    app.add_handler(restoredb_handler)
    app.add_handler(applyrestore_handler)
    app.add_handler(filestats_handler)
    app.add_handler(adminpanel_handler)

    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
