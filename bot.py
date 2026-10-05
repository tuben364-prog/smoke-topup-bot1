import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

TOKEN = "8969426584:AAHpj-caruzqeu2fARDvWpOIZNyD5iaHFeg"
ADMIN_USERNAME = "NOTSMOKE12"
TELEBIRR_NO = "0951001729"

WAITING_FOR_ID, WAITING_FOR_RECEIPT = range(2)

# ለ Render የሚያስፈልገው Dummy Web Server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# 1. Main Menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🎮 PUBG Mobile UC", callback_data="cat_pubg"),
            InlineKeyboardButton("💎 Free Fire Diamonds", callback_data="cat_ff")
        ],
        [
            InlineKeyboardButton("🔫 COD Mobile CP", callback_data="cat_cod"),
            InlineKeyboardButton("⚡ Fortnite V-Bucks", callback_data="cat_fn")
        ],
        [
            InlineKeyboardButton("🍎 Apple / iTunes Card", callback_data="cat_apple"),
            InlineKeyboardButton("▶️ Google Play Card", callback_data="cat_google")
        ],
        [
            InlineKeyboardButton("🪙 TikTok Coins", callback_data="cat_tiktok"),
            InlineKeyboardButton("⭐ Telegram Premium", callback_data="cat_prem")
        ],
        [
            InlineKeyboardButton("💳 Payment Methods", callback_data="view_payment")
        ],
        [
            InlineKeyboardButton("📞 Contact Support", url=f"https://t.me/{ADMIN_USERNAME}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        "👋 **Welcome to Smoke Top-Up Bot!**\n\n"
        "Please select an option below to purchase packages directly:"
    )

    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    keyboard = []
    if data == "cat_pubg":
        keyboard = [
            [InlineKeyboardButton("60 UC — 180 ETB", callback_data="buy_PUBG 60 UC_180 ETB")],
            [InlineKeyboardButton("120 UC — 355 ETB", callback_data="buy_PUBG 120 UC_355 ETB")],
            [InlineKeyboardButton("325 UC — 940 ETB", callback_data="buy_PUBG 325 UC_940 ETB")],
            [InlineKeyboardButton("660 UC — 1,850 ETB", callback_data="buy_PUBG 660 UC_1,850 ETB")],
            [InlineKeyboardButton("1,800 UC — 4,800 ETB", callback_data="buy_PUBG 1,800 UC_4,800 ETB")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
        text = "🎮 **Select PUBG UC Package:**"

    elif data == "cat_ff":
        keyboard = [
            [InlineKeyboardButton("100 Diamonds — 160 ETB", callback_data="buy_FF 100 Diamonds_160 ETB")],
            [InlineKeyboardButton("210 Diamonds — 330 ETB", callback_data="buy_FF 210 Diamonds_330 ETB")],
            [InlineKeyboardButton("530 Diamonds — 820 ETB", callback_data="buy_FF 530 Diamonds_820 ETB")],
            [InlineKeyboardButton("1,080 Diamonds — 1,650 ETB", callback_data="buy_FF 1,080 Diamonds_1,650 ETB")],
            [InlineKeyboardButton("Weekly Membership — 380 ETB", callback_data="buy_FF Weekly Member_380 ETB")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
        text = "💎 **Select Free Fire Diamonds Package:**"

    elif data == "cat_cod":
        keyboard = [
            [InlineKeyboardButton("80 CP — 220 ETB", callback_data="buy_COD 80 CP_220 ETB")],
            [InlineKeyboardButton("420 CP — 1,050 ETB", callback_data="buy_COD 420 CP_1,050 ETB")],
            [InlineKeyboardButton("880 CP — 2,100 ETB", callback_data="buy_COD 880 CP_2,100 ETB")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
        text = "🔫 **Select COD Mobile CP Package:**"

    elif data == "cat_tiktok":
        keyboard = [
            [InlineKeyboardButton("70 Coins — 190 ETB", callback_data="buy_TikTok 70 Coins_190 ETB")],
            [InlineKeyboardButton("350 Coins — 890 ETB", callback_data="buy_TikTok 350 Coins_890 ETB")],
            [InlineKeyboardButton("700 Coins — 1,750 ETB", callback_data="buy_TikTok 700 Coins_1,750 ETB")],
            [InlineKeyboardButton("1,400 Coins — 3,450 ETB", callback_data="buy_TikTok 1,400 Coins_3,450 ETB")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
        text = "🪙 **Select TikTok Coins Package:**"

    elif data == "cat_prem":
        keyboard = [
            [InlineKeyboardButton("3 Months — 1,600 ETB", callback_data="buy_TG 3 Months_1,600 ETB")],
            [InlineKeyboardButton("6 Months — 2,400 ETB", callback_data="buy_TG 6 Months_2,400 ETB")],
            [InlineKeyboardButton("12 Months — 4,200 ETB", callback_data="buy_TG 12 Months_4,200 ETB")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
        text = "⭐ **Select Telegram Premium Plan:**"

    elif data in ["cat_apple", "cat_google", "cat_fn"]:
        keyboard = [
            [InlineKeyboardButton("$5 Card — 750 ETB", callback_data="buy_Gift Card $5_750 ETB")],
            [InlineKeyboardButton("$10 Card — 1,450 ETB", callback_data="buy_Gift Card $10_1,450 ETB")],
            [InlineKeyboardButton("$25 Card — 3,550 ETB", callback_data="buy_Gift Card $25_3,550 ETB")],
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ]
        text = "🎁 **Select Gift Card Package:**"

    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def select_package(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, item_name, price = query.data.split("_")
    context.user_data["selected_item"] = item_name
    context.user_data["price"] = price

    cancel_btn = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel Order", callback_data="cancel_order")]])
    msg = (
        f"Selected Package: **{item_name}** ({price})\n\n"
        "👉 **Please send your Player ID / Account Username now:**"
    )
    await query.message.reply_text(msg, reply_markup=cancel_btn, parse_mode="Markdown")
    return WAITING_FOR_ID

async def receive_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id_text = update.message.text.strip()
    context.user_data["player_id"] = user_id_text

    item = context.user_data.get("selected_item")
    price = context.user_data.get("price")

    cancel_btn = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel Order", callback_data="cancel_order")]])
    payment_msg = (
        "✅ **Order Details Recorded:**\n"
        f"• Package: `{item}`\n"
        f"• Account ID: `{user_id_text}`\n"
        f"• Total Price: `{price}`\n\n"
        "💳 **Payment Information:**\n"
        f"📱 **Telebirr:** `{TELEBIRR_NO}`\n"
        "🏦 **CBE Bank:** `Coming Soon`\n\n"
        "📸 **Next Step:** Transfer the exact amount and **send the payment screenshot (receipt photo)** here!"
    )
    await update.message.reply_text(payment_msg, reply_markup=cancel_btn, parse_mode="Markdown")
    return WAITING_FOR_RECEIPT

async def receive_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    item = context.user_data.get("selected_item")
    price = context.user_data.get("price")
    player_id = context.user_data.get("player_id")

    await update.message.reply_text(
        "🎉 **Thank you! Your order has been submitted successfully.**\n\n"
        f"Admin (@{ADMIN_USERNAME}) will verify your payment and process your top-up within a few minutes.",
        parse_mode="Markdown"
    )

    admin_notification = (
        "🚨 **NEW ORDER RECEIVED!**\n\n"
        f"👤 Customer: @{user.username} (ID: `{user.id}`)\n"
        f"🎮 Package: `{item}`\n"
        f"💰 Price: `{price}`\n"
        f"🆔 Target Account ID: `{player_id}`"
    )

    try:
        photo_id = update.message.photo[-1].file_id
        await context.bot.send_photo(
            chat_id=f"@{ADMIN_USERNAME}",
            photo=photo_id,
            caption=admin_notification,
            parse_mode="Markdown"
        )
    except Exception:
        pass

    return ConversationHandler.END

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.reply_text("❌ Order cancelled.")
    await start(update, context)
    return ConversationHandler.END

async def view_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "💳 **Payment Methods:**\n\n"
        f"📱 **Telebirr:** `{TELEBIRR_NO}`\n"
        "🏦 **CBE Bank:** Coming Soon...\n\n"
        f"For any manual assistance, contact @{ADMIN_USERNAME}"
    )
    back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]])
    await query.message.edit_text(text, reply_markup=back_markup, parse_mode="Markdown")

if __name__ == '__main__':
    # Render እንዳይዘጋ ትንሽ የዌብ ሰርቨር ከጀርባ ማስኬጃ
    threading.Thread(target=run_web_server, daemon=True).start()

    app = ApplicationBuilder().token(TOKEN).build()

    order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_package, pattern="^buy_")],
        states={
            WAITING_FOR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_id)],
            WAITING_FOR_RECEIPT: [MessageHandler(filters.PHOTO, receive_receipt)]
        },
        fallbacks=[CallbackQueryHandler(cancel_order, pattern="^cancel_order$")]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(order_conv)
    app.add_handler(CallbackQueryHandler(start, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(show_category, pattern="^cat_"))
    app.add_handler(CallbackQueryHandler(view_payment, pattern="^view_payment$"))

    print("Smoke Top-Up Bot is running...")
    app.run_polling()