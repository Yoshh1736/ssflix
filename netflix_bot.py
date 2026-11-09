#!/usr/bin/env python3
# netflix_bot.py - STAIN NETFLIX HUB (Elite Edition)
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
    "ph": {"name": "Philippines 🇵🇭", "stock": 42},
    "jp": {"name": "Japan 🇯🇵", "stock": 89},
    "kr": {"name": "South Korea 🇰🇷", "stock": 64},
    "us": {"name": "United States 🇺🇸", "stock": 120},
    "br": {"name": "Brazil 🇧🇷", "stock": 215},
    "tr": {"name": "Turkey 🇹🇷", "stock": 98},
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
        [InlineKeyboardButton("⚡ GENERATE NOW ⚡", callback_data="menu_regions")],
        [InlineKeyboardButton("📂 Send File (.txt)", callback_data="send_txt"),
         InlineKeyboardButton("📝 Send Text", callback_data="send_text")],
        [InlineKeyboardButton("🔍 Any File Extract", callback_data="any_extract")],
        [InlineKeyboardButton("⭐ Reviews", callback_data="reviews"),
         InlineKeyboardButton("👨‍💻 Developer", callback_data="developer")],
        [InlineKeyboardButton("❓ Tutorial & Help", callback_data="tutorial")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "✦ ─── STAIN NETFLIX HUB ─── ✦\n"
        "👥 Active Users: `14,890 monthly`\n\n"
        "✨ **System Features:**\n"
        "→ 🍪 *Extract NetflixId, Auto-Check & Route Direct Premium Sessions.*\n\n"
        "📁 **Supported Formats:**\n"
        "→ `zip`, `txt`, `json`, `rar` via Any File Extract\n\n"
        "⚡ **Command Shortcuts:**\n"
        "/start - Launch Dashboard\n"
        "/stats - Live Engine Status\n\n"
        "📊 **Global Engine Stats:**\n"
        "→ Available Stock : `945 Sessions`\n"
        "→ Success Rate : `99.99%`\n"
        "──────────────────────────\n"
        "👑 **Developed by @mtfeels**"
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
        [InlineKeyboardButton("🇵🇭 Philippines (42)", callback_data="gen_ph"),
         InlineKeyboardButton("🇯🇵 Japan (89)", callback_data="gen_jp")],
        [InlineKeyboardButton("🇰🇷 South Korea (64)", callback_data="gen_kr"),
         InlineKeyboardButton("🇺🇸 United States (120)", callback_data="gen_us")],
        [InlineKeyboardButton("🇧🇷 Brazil (215)", callback_data="gen_br"),
         InlineKeyboardButton("🇹🇷 Turkey (98)", callback_data="gen_tr")],
        [InlineKeyboardButton("🏠 Return Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(
        "🌐 **SELECT TARGET REGION / COUNTRY:**\n"
        "_Choose a high-speed proxy node below._\n\n"
        "📂 *Page: 1 / 1*", 
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
        "✦ ── STAIN SESSION GENERATOR ── ✦\n\n"
        f"▎Email: `{email}`\n"
        f"▎Phone: `{phone}`\n"
        f"▎Country: {reg_info['name']}\n"
        f"▎Plan: Premium UHD\n"
        f"▎Ad Plan: No ✅\n"
        f"▎Quality: 4K Ultra HD\n"
        f"▎Max Streams: 4 Screens\n\n"
        "▎Profiles (5): `onyon`, `Fuck zuya`, `Xiangelo`, `Zen`, `lady`\n\n"
        "▎Status: CURRENT_MEMBER\n"
        "▎On Hold: No ✅\n"
        "▎Member Since: Jul Auth\n"
        "▎Payment: MOBILE_WALLET\n"
        "▎Next Billing: December 7, 2026\n"
        "▎Extra Members: None\n\n"
        "──────────────────────────\n\n"
        f"▎Cookie Payload:\n`{SAMPLE_COOKIE}`\n\n"
        f"▎Mobile Link: {mobile_link}\n"
        f"▎PC Link: {pc_link}\n"
        f"▎TV Link: {tv_link}\n\n"
        "👑 **Developed by @mtfeels**"
    )
    
    keyboard = [
        [InlineKeyboardButton("💻 PC Login ↗", url=pc_link),
         InlineKeyboardButton("📱 Mobile Login ↗", url=mobile_link)],
        [InlineKeyboardButton("📺 TV Login ↗", url=tv_link)],
        [InlineKeyboardButton("🏠 Return Home", callback_data="home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=result_text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    file_content = (
        "✦ ── STAIN SESSION GENERATOR ── ✦\n\n"
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
        "──────────────────────────\n\n"
        f"▎Cookie: \n{SAMPLE_COOKIE}\n\n"
        f"▎Mobile Link: {mobile_link}\n"
        f"▎PC Link: {pc_link}\n"
        f"▎TV Link: {tv_link}\n\n"
        "👑 Developed by @mtfeels\n"
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
        caption="🔒 You need to verify this account to unlock the next generation.\n\n⚡ Verify using the buttons below.",
        reply_markup=verify_markup
    )
    print(f"✅ Successfully generated and sent account for {email}!")

async def home_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await start(update, context)

async def dummy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer("✨ System module active & synchronized with @mtfeels cloud!", show_alert=True)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    
    print("🤖 STAIN Netflix Premium Bot initialized and running 24/7 by @mtfeels...")
    app.run_polling()

if __name__ == "__main__":
    main()
