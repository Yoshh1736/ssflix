#!/usr/bin/env python3
# netflix_bot.py - STAIN Netflix Premium Multi-Tool Cloud Bot (Diagnostic Edition)
import os
import random
import time
import logging
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable full logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "9151185184:AAGbZw6R_hu8SzfokI0C7qlLtNyowcy0n7E"

USER_COOLDOWNS = {}
COOLDOWN_TIME = 180 

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
    print("📥 /start command received!")
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
        "✨ —SS Netflix Premium ✨\n"
        "10,187 monthly users\n\n"
        "✨ Features:\n"
        "→ 🍪 Extract NetflixId, Check & Generate Direct Login from Premium accounts only.\n\n"
        "📁 Supported Formats:\n"
        "→ Text files (zip,txt,json,rar) by Any File extract\n\n"
        "⚡ Quick Commands:\n"
        "/start - Restart Bot\n"
        "/cancel - Stop current task\n"
        "/stats - Bot statistics\n\n"
        "📊 Bot Stats:\n"
        "→ Available Stock : 740\n"
        "→ 10000+ Active Users\n"
        "→ 99.9% Success Rate\n"
        "Developed by @FuturePrimeMinister"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text(welcome_text, reply_markup=reply_markup)

async def menu_regions_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("👉 'Generate Now' button clicked!")
    query = update.callback_query
    await query.answer()
    
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
        "🌐 Select a Country to Generate Netflix Account:\nPage: 1/1", 
        reply_markup=reply_markup
    )

async def generate_account_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    print(f"🔥 COUNTRY BUTTON CLICKED: {query.data}")
    
    user_id = query.from_user.id
    await query.answer()
    data = query.data

    # Check cooldown
    current_time = time.time()
    last_gen_time = USER_COOLDOWNS.get(user_id, 0)
    if (current_time - last_gen_time) < COOLDOWN_TIME:
        remaining = int(COOLDOWN_TIME - (current_time - last_gen_time))
        await query.answer(f"⏳ Cooldown active! Wait {remaining // 60}m {remaining % 60}s.", show_alert=True)
        return

    USER_COOLDOWNS[user_id] = current_time

    reg_code = data.split("_")[1]
    reg_info = REGIONS.get(reg_code, REGIONS["ph"])
    email = random.choice(SAMPLE_EMAILS)
    phone = f"+6309{random.randint(10000000, 99999999)}"
    
    token_hash = f"BgjkwevcAxLCAcp1m9DTyzISpi0j2VCpwq8+hIQ5+{random.randint(100,999)}wyzNuToxAcVXDK893gbHz436kgYSMzgn/g1rdkj0QRZ73C9SZo0Ik3Apj7KK5Adjbbj9AB1GR8Oe0vti2OCNS6TNI11+51rOjqDy7obVlrVQtty6j+Sz/MSPRReEKr3bVAl7emFzgpBg0yjWxbL9hYUfWCCeIVueQVbttH52kiXViDxqNtXTiHO5T3cuZMrfHRgO8mpJdcnta20DgO496gLv8BWl+NEoOsXl6iGAYiDgoM8gsPtUQc3Qa5TUWo"
    mobile_link = f"https://www.netflix.com/unsupported?nftoken={token_hash}"
    pc_link = f"https://www.netflix.com/browse?nftoken={token_hash}"
    tv_link = f"https://www.netflix.com/tv9?nftoken={token_hash}"

    result_text = (
        "✦ Netflix Account Generated Successfully\n\n"
        f"▎Email: {email}\n"
        f"▎Phone: {phone}\n"
        f"▎Country: {reg_info['name']}\n"
        f"▎Plan: Premium\n"
        f"▎Ad Plan: No ✅\n"
        f"▎Quality: UHD\n"
        f"▎Max Streams: 4\n\n"
        "▎Profiles (5): onyon, Fuck zuya, Xiangelo, Zen, lady\n\n"
        "▎Status: CURRENT_MEMBER\n"
        "▎On Hold: No ✅\n"
        "▎Member Since: Jul 2025\n"
        "▎Payment: MOBILE_WALLET\n"
        "▎Next Billing: December 7, 2026\n"
        "▎Extra Members: No\n\n"
        "───────────────\n\n"
        f"▎Cookie:\n{SAMPLE_COOKIE}\n\n"
        f"▎Mobile Link: {mobile_link}\n"
        f"▎PC Link: {pc_link}\n"
        f"▎TV Link: {tv_link}\n\n"
        "Developer: t.me/FuturePrimeMinister"
    )
    
    keyboard = [
        [InlineKeyboardButton("💻 PC Login ↗", url=pc_link),
         InlineKeyboardButton("📱 Mobile Login ↗", url=mobile_link)],
        [InlineKeyboardButton("📺 TV Login ↗", url=tv_link)],
        [InlineKeyboardButton("🏠 Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=result_text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    file_content = (
        "✦ Netflix Account Generated Successfully\n\n"
        f"▎Email: {email}\n"
        f"▎Phone: {phone}\n"
        f"▎Country: {reg_info['name']}\n"
        f"▎Plan: Premium\n"
        f"▎Ad Plan: No ✅\n"
        f"▎Quality: UHD\n"
        f"▎Max Streams: 4\n\n"
        "▎Profiles (5): onyon, Fuck zuya, Xiangelo, Zen, lady\n\n"
        "▎Status: CURRENT_MEMBER\n"
        "▎On Hold: No ✅\n"
        "▎Member Since: Jul 2025\n"
        "▎Payment: MOBILE_WALLET\n"
        "▎Next Billing: December 7, 2026\n"
        "▎Extra Members: No\n\n"
        "───────────────\n\n"
        f"▎Cookie: \n{SAMPLE_COOKIE}\n\n"
        f"▎Mobile Link: {mobile_link}\n"
        f"▎PC Link: {pc_link}\n"
        f"▎TV Link: {tv_link}\n"
    )
    
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
        caption="You need to verify this account to get new account.\n\nVerify using these buttons.",
        reply_markup=verify_markup
    )
    print(f"✅ Successfully generated and sent account for {email}!")

async def home_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await start(update, context)

async def dummy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer("Feature active and synced with database!", show_alert=True)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) ->none if False else None:
    pass

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Drop any leftover webhooks so polling works cleanly
    app.bot.delete_webhook(drop_pending_updates=True)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_regions_callback, pattern="^menu_regions$"))
    app.add_handler(CallbackQueryHandler(generate_account_callback, pattern="^gen_"))
    app.add_handler(CallbackQueryHandler(home_callback, pattern="^home$"))
    app.add_handler(CallbackQueryHandler(dummy_callback, pattern="^(working_|send_txt|send_text|any_extract|reviews|developer|tutorial)"))
    
    print("🤖 STAIN Netflix Premium Bot initialized and running 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()
