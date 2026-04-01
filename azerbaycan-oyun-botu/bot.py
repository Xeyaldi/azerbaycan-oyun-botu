import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from games.soz_izahi import SozIzahi
from games.bosluq_doldurma import BosluqDoldurma
from games.bilgi_oyunu import BilgiOyunu
from games.xox import XOX
from games.bayraq_oyunu import BayraqOyunu
from games.paytaxt_tapmaca import PaytaxtTapmaca
from games.soz_zenciri import SozZenciri

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

GAMES = {
    "soz_izahi": SozIzahi(),
    "bosluq": BosluqDoldurma(),
    "bilgi": BilgiOyunu(),
    "xox": XOX(),
    "bayraq": BayraqOyunu(),
    "paytaxt": PaytaxtTapmaca(),
    "soz_zenciri": SozZenciri(),
}

def ana_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎯 Söz İzahı", callback_data="oyun_soz_izahi"),
         InlineKeyboardButton("📝 Boşluq Doldurma", callback_data="oyun_bosluq")],
        [InlineKeyboardButton("🧠 Bilik Oyunu", callback_data="oyun_bilgi"),
         InlineKeyboardButton("⭕ XOX", callback_data="oyun_xox")],
        [InlineKeyboardButton("🚩 Bayraq Oyunu", callback_data="oyun_bayraq"),
         InlineKeyboardButton("🏛 Paytaxt Tapmaca", callback_data="oyun_paytaxt")],
        [InlineKeyboardButton("🔗 Söz Zənciri", callback_data="oyun_soz_zenciri")],
        [InlineKeyboardButton("📊 Liderlik Cədvəli", callback_data="liderlik"),
         InlineKeyboardButton("❓ Yardım", callback_data="yardim")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"Salam, {user.first_name}! 👋\n\n"
        "🎮 *Azərbaycan Oyun Botuna xoş gəldiniz!*\n\n"
        "Aşağıdakı oyunlardan birini seçərək başlaya bilərsiniz:"
    )
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=ana_menu_keyboard()
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 *Ana Menü*\n\nOyun seçin:",
        parse_mode="Markdown",
        reply_markup=ana_menu_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "ana_menu":
        await query.edit_message_text(
            "🎮 *Ana Menü*\n\nOyun seçin:",
            parse_mode="Markdown",
            reply_markup=ana_menu_keyboard()
        )
        return

    if data == "liderlik":
        await show_leaderboard(query, context)
        return

    if data == "yardim":
        await show_help(query, context)
        return

    if data.startswith("oyun_"):
        game_key = data.replace("oyun_", "")
        if game_key in GAMES:
            game = GAMES[game_key]
            await game.start_game(query, context)
        return

    # Delegate to active game
    for game_key, game in GAMES.items():
        if game.handles_callback(data, context, query.from_user.id):
            await game.handle_callback(query, context)
            return

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Check if user is in an active game
    active_game = context.user_data.get("active_game")
    if active_game and active_game in GAMES:
        game = GAMES[active_game]
        await game.handle_message(update, context)
        return

    await update.message.reply_text(
        "Oyun seçmək üçün /menu yazın və ya /start ilə başlayın.",
        reply_markup=ana_menu_keyboard()
    )

async def show_leaderboard(query, context: ContextTypes.DEFAULT_TYPE):
    scores = context.bot_data.get("scores", {})
    if not scores:
        text = "📊 *Liderlik Cədvəli*\n\nHələ heç kim xal qazanmayıb. İlk siz olun! 🏆"
    else:
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
        text = "📊 *Liderlik Cədvəli (Top 10)*\n\n"
        medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
        for i, (name, score) in enumerate(sorted_scores):
            text += f"{medals[i]} {name}: *{score}* xal\n"

    keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]]
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_help(query, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "❓ *Yardım*\n\n"
        "🎯 *Söz İzahı* — Söz verilir, izah et!\n"
        "📝 *Boşluq Doldurma* — Cümləni tamamla\n"
        "🧠 *Bilik Oyunu* — Sualları cavabla\n"
        "⭕ *XOX* — Klassik tic-tac-toe\n"
        "🚩 *Bayraq Oyunu* — Bayrağı tap\n"
        "🏛 *Paytaxt Tapmaca* — Paytaxtı tap\n"
        "🔗 *Söz Zənciri* — Sözü davam etdir\n\n"
        "📌 *Komandalar:*\n"
        "/start — Botu başlat\n"
        "/menu — Ana menü\n"
        "/xal — Xalınıza baxın\n"
        "/dur — Oyunu dayandır"
    )
    keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]]
    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def xal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    scores = context.bot_data.get("scores", {})
    user_score = scores.get(user.full_name, 0)
    await update.message.reply_text(
        f"⭐ *{user.first_name}*, sizdə *{user_score}* xal var!",
        parse_mode="Markdown"
    )

async def dur_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("active_game", None)
    context.user_data.pop("game_state", None)
    await update.message.reply_text(
        "⏹ Oyun dayandırıldı.",
        reply_markup=ana_menu_keyboard()
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("xal", xal_command))
    app.add_handler(CommandHandler("dur", dur_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("✅ Bot işə düşdü...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
