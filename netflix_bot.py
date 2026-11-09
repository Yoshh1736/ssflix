#!/usr/init/env python3
# netflix_bot.py - STAIN Netflix Premium Multi-Tool Cloud Bot (Exact Match Edition)
import os
import random
import logging
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

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
        [InlineKeyboardButton("🎬 Generate Now", callback_data="menu_regions")],
        [InlineKeyboardButton("📂 Send file(txt)", callback_data="send_txt"),
         InlineKeyboardButton("📝 Send Text", callback_data="send_text")],
        [InlineKeyboardButton("🔍 Any File Extract", callback_data="any_extract")],
        [InlineKeyboardButton("⭐ Reviews", callback_data="reviews"),
         InlineKeyboardButton("👨‍💻 Developer", callback_data="developer")],
        [InlineKeyboardButton("Tutorial ⁉️", callback_data="tutorial")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "✨ **—SS Netflix Premium** ✨\n"
        "10,187 monthly users\n\n"
        "✨ **Features:**\n"
        "→ 🍪 Extract NetflixId, Check & Generate Direct Login from Premium accounts only.\n\n"
        "📁 **Supported Formats:**\n"
        "→ Text files (zip,txt,json,rar) by 📎 **Any File extract**\n\n"
        "⚡ **Quick Commands:**\n"
        "/start - Restart Bot\n"
        "/cancel - Stop current task\n"
        "/stats - Bot statistics\n\n"
        "📊 **Bot Stats:**\n"
        "→ Available Stock : 740\n"
        "→ 10000+ Active Users\n"
        "→ 99.9% Success Rate\n"
        "Developed by @FuturePrimeMinister"
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
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "🌐 **Select a Country to Generate Netflix Account:**\n*Page: 1/1*", 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )

    elif data.startswith("gen_"):
        reg_code = data.split("_")[1]
        reg_info = REGIONS.get(reg_code, REGIONS["ph"])
        email = random.choice(SAMPLE_EMAILS)
        phone = f"+6309{random.randint(10000000, 99999999)}"
        
        result_text = (
            "✅ **Netflix Account Generated Successfully !**\n\n"
            f"📧 **Email:** `{email}` (Yes ✅)\n"
            f"📞 **Phone:** `{phone}` (Yes ✅)\n"
            f"🌍 **Country:** {reg_info['name']}\n"
            f"🎬 **Plan:** Premium (Ad Plan: No ✅)\n"
            f"📺 **Quality:** UHD\n"
            f"👥 **Max Streams:** 4\n"
            f"👥 **Profiles (5):** onyon, Fuck zuya, Xiangelo, Zen, lady\n"
            f"🟢 **Status:** CURRENT_MEMBER (On Hold: No ✅)\n"
            f"📅 **Member Since:** Jul 2025\n"
            f"💳 **Payment:** MOBILE_WALLET\n"
            f"⏳ **Next Billing:** December 7, 2026\n"
            f"➕ **Extra Members:** No\n\n"
            f"🍪 **Cookie:** `{SAMPLE_COOKIE}`\n\n"
            "Developer: t.me/FuturePrimeMinister"
        )
        
        keyboard = [
            [InlineKeyboardButton("💻 PC Login ↗", callback_data=f"login_pc_{reg_code}"),
             InlineKeyboardButton("📱 Mobile Login ↗", callback_data=f"login_mob_{reg_code}")],
            [InlineKeyboardButton("📺 TV Login ↗", callback_data=f"login_tv_{reg_code}")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Edit the message to show the generated account details
        await query.message.edit_text(result_text, reply_markup=reply_markup, parse_mode="Markdown")

        # Also send the .txt file and verification buttons like the reference screenshot
        file_content = f"Email: {email}\nPhone: {phone}\nCountry: {reg_info['name']}\nCookie: {SAMPLE_COOKIE}\n"
        file_bytes = BytesIO(file_content.encode("utf-8"))
        file_bytes.name = f"{email}.txt"

        verify_keyboard = [
            [InlineKeyboardButton("Working ✅", callback_data="working_yes"),
             InlineKeyboardButton("Not Working ❌", callback_data="working_no")]
        ]
        verify_markup = InlineKeyboardMarkup(verify_keyboard)

        await context.bot.send_document(
            chat_id=query.message.chat_id,
            document=InputFile(file_bytes),
            caption=(
                "You need to verify this account to get new account.\n\n"
                "Verfy using this buttons."
            ),
            reply_markup=verify_markup
        )

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
                "💻 **PC / Laptop Login Instructions:**\n\n"
                "1. Install browser extension **'EditThisCookie'** or **'Cookie-Editor'**.\n"
                f"2. Go to [{url}]({url})\n"
                "3. Import or set Cookie Name: `NetflixId` with the generated cookie value.\n"
                "4. Refresh the page to access premium session instantly."
            )
        elif device_type == "mob":
            msg = (
                "📱 **Mobile / Tablet Login Instructions:**\n\n"
                "1. Open mobile browser or Netflix app.\n"
                f"2. Session payload synced for region `{reg_code.upper()}`.\n"
                f"3. Direct authentication link: [{url}browse]({url}browse)"
            )
        else:
            pin = f"{random.randint(10,99)}-{random.randint(10,99)}"
            msg = (
                "📺 **Smart TV / Console Login Instructions:**\n\n"
                "1. Open Netflix on your TV and go to Sign In on Web.\n"
                f"2. Visit [{url}tv]({url}tv)\n"
                f"3. Enter pairing PIN: **{pin}**"
            )
            
        keyboard = [
            [InlineKeyboardButton("🏠 Home", callback_data="home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(msg, reply_markup=reply_markup, parse_mode="Markdown", disable_web_page_preview=True)

    elif data == "home":
        await start(update, context)

    elif data in ["working_yes", "working_no"]:
        await query.answer("Thank you for your feedback! Stock replenished.", show_alert=True)

    elif data in ["send_txt", "send_text", "any_extract", "reviews", "developer", "tutorial"]:
        await query.answer("Feature active and synced with database!", show_alert=True)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("📊 **Bot Stats:**\n→ Available Stock : 740\n→ 10000+ Active Users\n→ 99.9% Success Rate", parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 STAIN Netflix Premium Bot initialized and running 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
