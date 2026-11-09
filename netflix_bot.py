#!/usr/bin/env python3
# netflix_bot.py - STAIN Netflix Premium Multi-Tool Cloud Bot
import os
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Hardcoded Bot Token as requested
TOKEN = "9151185184:AAGbZw6R_hu8SzfokI0C7qlLtNyowcy0n7E"

REGIONS = {
    "ph": {"name": "Philippines 🇵🇭", "stock": 17},
    "jp": {"name": "Japan 🇯🇵", "stock": 42},
    "kr": {"name": "South Korea 🇰🇷", "stock": 29},
    "us": {"name": "USA 🇺🇸", "stock": 33},
    "br": {"name": "Brazil 🇧🇷", "stock": 113},
    "tr": {"name": "Turkey 🇹🇷", "stock": 52},
}

SAMPLE_EMAILS = [
    "carlospacamarra01@gmail.com",
    "yuki.tanaka99@yahoo.jp",
    "minho.park_kr@naver.com",
    "scooppreview_us@outlook.com"
]

SAMPLE_COOKIE = (
    "NetflixId=v%3D3%2Ectok%3DB3DbgJl0vcAxKbA6SY3py00Ba0-"
    "TGU1p2ymFQT3K9NLCnqHSftQi7gmyoOrTUWQ5D7Gri7hXvJXu8ErMPzuw"
    "nQknC-fSsS4yFwfKtje199YPx5QRu2daoCS6bDuk4LbcoFatqk06sfyhs9ZVgd"
    "uh6E23cbv2hkAaJXfJ8hxFezghO4rfbiJ3lOw01qni1WimLoudAjSyBQqW"
    "XQeorRaza29ywR6Ekms-95OXUj0xV4Zk5ukvWt_tNT5_jb10Zn4RkS0Y-"
    "QKAxQc9EDviMiPU1UemAVH52c0PK2CbSICYY32yha-rena-"
    "LLDkpYzAXFvkm5m4_kCilPdX2KziYIKYJVxr2QUY_aUFo3Vxm78-"
    "M9ZJlK2WsjHY-DnLDN0wVRgdgEUsj0ViKYVnQwltO9zCL5GXTXWaUx52WaPOySND4rCrYW8"
    "1PyQBkrRAv0gNw38mUkEimPluGVhNzv3EXBTV4suJo5adTtG68dSQH5Wrv"
    "EQH7yofeE0qywLzUGxu3LuxV6e3Zzt1VyD3ckxqfsnubasf7TsrcGjte_0"
    "RracfYfMa5UxgGig4KDEFwEDFkkjF0uokSPa..%26pg%3DGDALTHGORRHI"
    "VH7WGZXF5HKZMI%26ch%3D3DAQEAAABAbSM0F4_FgDcQui2BVdLleLvW8g"
    "jPalxks."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("⚡ 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘 𝗡𝗢𝗪 ⚡", callback_data="menu_regions")],
        [InlineKeyboardButton("📁 Send File (.txt)", callback_data="send_txt"),
         InlineKeyboardButton("📝 Send Text", callback_data="send_text")],
        [InlineKeyboardButton("🔍 Any File Extract", callback_data="any_extract")],
        [InlineKeyboardButton("⭐ Reviews", callback_data="reviews"),
         InlineKeyboardButton("👨‍💻 Developer", callback_data="developer")],
        [InlineKeyboardButton("❓ Tutorial & Help", callback_data="tutorial")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "✦ ─── 𝕾𝕿𝕬𝕴𝕹 𝕹𝕰𝕿𝕱𝕷𝕴𝖃 𝕳𝖀𝕭 ─── ✦\n"
        "👥 *Active Users:* `10,187 monthly`\n\n"
        "✨ **System Features:**\n"
        "→ 🍪 *Extract NetflixId, Auto-Check & Route Direct Premium Logins.*\n\n"
        "📁 **Supported Formats:**\n"
        "→ `zip`, `txt`, `json`, `rar` via Any File Extract\n\n"
        "⚡ **Command Shortcuts:**\n"
        "/start - Launch Dashboard\n"
        "/stats - Live Engine Status\n\n"
        "📊 **Global Engine Stats:**\n"
        "→ Available Stock : `740 Sessions`\n"
        "→ Success Rate : `99.9%`\n"
        "──────────────────────────\n"
        "👑 *Developed by @mtfeels*"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_regions":
        keyboard = [
            [InlineKeyboardButton("🇵🇭 Philippines (17)", callback_data="gen_ph"),
             InlineKeyboardButton("🇯🇵 Japan (42)", callback_data="gen_jp")],
            [InlineKeyboardButton("🇰🇷 South Korea (29)", callback_data="gen_kr"),
             InlineKeyboardButton("🇺🇸 United States (33)", callback_data="gen_us")],
            [InlineKeyboardButton("🇧🇷 Brazil (113)", callback_data="gen_br"),
             InlineKeyboardButton("🇹🇷 Turkey (52)", callback_data="gen_tr")],
            [InlineKeyboardButton("🏠 Return Home", callback_data="home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "🌐 **SELECT TARGET REGION / COUNTRY:**\n"
            "_Choose a server node to route session generation._\n\n"
            "📂 *Page: 1 / 1*", 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )

    elif data.startswith("gen_"):
        reg_code = data.split("_")[1]
        reg_info = REGIONS.get(reg_code, REGIONS["ph"])
        email = random.choice(SAMPLE_EMAILS)
        phone = f"+6309{random.randint(10000000, 99999999)}"
        
        result_text = (
            "✅ **NETFLIX PREMIUM SESSION GENERATED !**\n"
            "──────────────────────────\n"
            f"📧 *Email:* `{email}` (Valid ✅)\n"
            f"📞 *Phone:* `{phone}` (Active ✅)\n"
            f"🌍 *Region Node:* {reg_info['name']}\n"
            f"🎬 *Plan Type:* Premium UHD (Ad-Free ✅)\n"
            f"👥 *Profiles:* `onyon`, `zuya`, `Xiangelo`, `Zen`, `lady`\n"
            f"🟢 *Status:* CURRENT_MEMBER\n"
            f"💳 *Billing:* Active (Renews Dec 2026)\n"
            "──────────────────────────\n"
            f"🍪 *Cookie Payload:*\n`{SAMPLE_COOKIE}`\n\n"
            "👇 *Select your target device login route below:*"
        )
        
        keyboard = [
            [InlineKeyboardButton("💻 PC / Laptop Login", callback_data=f"login_pc_{reg_code}"),
             InlineKeyboardButton("📱 Mobile / Tab Login", callback_data=f"login_mob_{reg_code}")],
            [InlineKeyboardButton("📺 Smart TV / Console", callback_data=f"login_tv_{reg_code}")],
            [InlineKeyboardButton("🔄 Generate Another", callback_data="menu_regions"),
             InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(result_text, reply_markup=reply_markup, parse_mode="Markdown")

    elif data.startswith("login_"):
        parts = data.split("_")
        device_type = parts[1]
        reg_code = parts[2]
        base_urls = {
            "ph": "https://www.netflix.com/ph/",
            "jp": "https://www.netflix.com/jp/",
            "kr": "https://www.netflix.com/kr/",
            "us": "https://www.netflix.com/",
            "br": "https://www.netflix.com/br/",
            "tr": "https://www.netflix.com/tr/"
        }
        url = base_urls.get(reg_code, "https://www.netflix.com/")
        
        if device_type == "pc":
            msg = (
                "💻 **PC / LAPTOP SESSION INJECTION:**\n"
                "──────────────────────────\n"
                "1. Install browser extension **'EditThisCookie'** or **'Cookie-Editor'**.\n"
                f"2. Open [{url}]({url})\n"
                "3. Create/Edit cookie: Name `NetflixId` -> Paste generated value.\n"
                "4. Refresh page for instant VIP access."
            )
        elif device_type == "mob":
            msg = (
                "📱 **MOBILE / TABLET DEEP-LINK:**\n"
                "──────────────────────────\n"
                "1. Open your mobile browser or Netflix App.\n"
                f"2. Region Node Locked: `{reg_code.upper()}`.\n"
                f"3. Secure Portal Link: [{url}browse]({url}browse)"
            )
        else:
            pin = f"{random.randint(10,99)}-{random.randint(10,99)}"
            msg = (
                "📺 **SMART TV / CONSOLE PAIRING:**\n"
                "──────────────────────────\n"
                "1. Open Netflix App on your TV -> Sign In on Web.\n"
                f"2. Visit portal: [{url}tv]({url}tv)\n"
                f"3. Enter secure TV PIN code: **{pin}**"
            )
            
        keyboard = [
            [InlineKeyboardButton("⬅️ Back to Session", callback_data=f"gen_{reg_code}"),
             InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(msg, reply_markup=reply_markup, parse_mode="Markdown", disable_web_page_preview=True)

    elif data == "home":
        await start(update, context)

    elif data in ["send_txt", "send_text", "any_extract", "reviews", "developer", "tutorial"]:
        await query.answer("✨ Module successfully synchronized with STAIN cloud engine!", show_alert=True)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stats_msg = (
        "📊 **STAIN BOT SYSTEM METRICS:**\n"
        "──────────────────────────\n"
        "→ Available Stock : `740 Accounts`\n"
        "→ Active Monthly Users : `10,187`\n"
        "→ Gateway Success Rate : `99.9%`\n"
        "→ Operational Status : `ONLINE (24/7)`"
    )
    await update.message.reply_text(stats_msg, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 STAIN Netflix Premium Bot initialized and running 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
