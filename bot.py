import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

from games.soz_izahi         import SozIzahi
from games.bosluq_doldurma   import BosluqDoldurma
from games.bilgi_oyunu        import BilgiOyunu
from games.xox                import XOX
from games.bayraq_oyunu       import BayraqOyunu
from games.paytaxt_tapmaca    import PaytaxtTapmaca
from games.soz_zenciri        import SozZenciri
from games.soz_sarmali        import SozSarmali
from games.suretli_riyaziyyat import SuretliRiyaziyyat
from games.reqem_tapmaca      import ReqemTapmaca
from games.plaka_oyunu        import PlakaOyunu
from games.tap_gorelim        import TapGorelim
from games.pi_oyunu           import PiOyunu
from games.dogru_cesaret      import DogruCesaret
from games.buton_oyunu        import ButonOyunu
from games.yaddash_shimseyi   import YaddasShimseyi
from games.isti_soyuq         import IstiSoyuq
from games.eser_muellif       import EserMuellif

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config Vars (Heroku → Settings → Config Vars) ─────────────────────────────
BOT_TOKEN    = os.environ.get("BOT_TOKEN",    "YOUR_BOT_TOKEN_HERE")
OWNER_LINK   = os.environ.get("OWNER_LINK",   "https://t.me/your_username")
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/your_channel")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "your_bot_username")

# ── Game registry ─────────────────────────────────────────────────────────────
GAMES: dict = {
    "soz_izahi":     SozIzahi(),
    "bosluq":        BosluqDoldurma(),
    "bilgi":         BilgiOyunu(),
    "xox":           XOX(),
    "bayraq":        BayraqOyunu(),
    "paytaxt":       PaytaxtTapmaca(),
    "soz_zenciri":   SozZenciri(),
    "soz_sarmali":   SozSarmali(),
    "suretli_riyaz": SuretliRiyaziyyat(),
    "reqem_tapmaca": ReqemTapmaca(),
    "plaka":         PlakaOyunu(),
    "tap_gorelim":   TapGorelim(),
    "pi":            PiOyunu(),
    "dogru_cesaret": DogruCesaret(),
    "buton":         ButonOyunu(),
    "yaddash":       YaddasShimseyi(),
    "isti_soyuq":    IstiSoyuq(),
    "eser_muellif":  EserMuellif(),
}

# ── Helpers ───────────────────────────────────────────────────────────────────
def is_group(update: Update) -> bool:
    return update.effective_chat.type in ("group", "supergroup")


def start_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 Sahib",   url=OWNER_LINK),
            InlineKeyboardButton("📢 Kanal",   url=CHANNEL_LINK),
        ],
        [
            InlineKeyboardButton("❓ Kömək",   callback_data="komek"),
            InlineKeyboardButton("🎮 Oyunlar", callback_data="oyun_menu"),
        ],
        [
            InlineKeyboardButton(
                "➕ Qrupa Əlavə Et",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            )
        ],
    ])


def oyun_menu_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎯 Söz İzahı",         callback_data="oyun_soz_izahi"),
            InlineKeyboardButton("📝 Boşluq Doldurma",   callback_data="oyun_bosluq"),
        ],
        [
            InlineKeyboardButton("🔄 Söz Sarmalı",        callback_data="oyun_soz_sarmali"),
            InlineKeyboardButton("⚡ Sürətli Riyaziyyat", callback_data="oyun_suretli_riyaz"),
        ],
        [
            InlineKeyboardButton("🎲 Rəqəm Tapmaca",     callback_data="oyun_reqem_tapmaca"),
            InlineKeyboardButton("❓ Tap Görəlim",        callback_data="oyun_tap_gorelim"),
        ],
        [
            InlineKeyboardButton("🧠 Bilik Oyunu",        callback_data="oyun_bilgi"),
            InlineKeyboardButton("🚩 Bayraq Oyunu",       callback_data="oyun_bayraq"),
        ],
        [
            InlineKeyboardButton("🔗 Söz Zənciri",        callback_data="oyun_soz_zenciri"),
            InlineKeyboardButton("🏛 Paytaxt Tapmaca",    callback_data="oyun_paytaxt"),
        ],
        [
            InlineKeyboardButton("🚗 Plaka Oyunu",        callback_data="oyun_plaka"),
            InlineKeyboardButton("π  Pi Oyunu",           callback_data="oyun_pi"),
        ],
        [
            InlineKeyboardButton("⭕ XOX (2 nəfər)",      callback_data="oyun_xox"),
            InlineKeyboardButton("🎭 Doğru/Cəsarət",     callback_data="oyun_dogru_cesaret"),
        ],
        [
            InlineKeyboardButton("🎮 Buton Oyunu",        callback_data="oyun_buton"),
            InlineKeyboardButton("⚡ Yaddaş Şimşəyi",     callback_data="oyun_yaddash"),
        ],
        [
            InlineKeyboardButton("🌡 İsti Soyuq",         callback_data="oyun_isti_soyuq"),
            InlineKeyboardButton("📚 Əsər-Müəllif",       callback_data="oyun_eser_muellif"),
        ],
        [
            InlineKeyboardButton("📊 Liderlik Cədvəli",   callback_data="liderlik"),
        ],
        [
            InlineKeyboardButton("🔙 Geri",               callback_data="start_menu"),
        ],
    ])


ONLY_GROUP_TEXT = (
    "🎮 Oyunlar yalnız *qrupda* işləyir!\n\n"
    "Botu qrupunuza əlavə edin:"
)


def only_group_kb():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Qrupa Əlavə Et",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            )
        ],
        [InlineKeyboardButton("🔙 Geri", callback_data="start_menu")],
    ])


def start_text(name: str) -> str:
    return (
        f"👋 Salam, *{name}*!\n\n"
        "🎮 *Azərbaycan Oyun Botuna xoş gəldiniz!*\n\n"
        "Qrupunuzu əyləndirmək üçün *18 Azərbaycan dilli oyun*!\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 Söz İzahı  •  📝 Boşluq Doldurma\n"
        "🔄 Söz Sarmalı  •  ⚡ Sürətli Riyaziyyat\n"
        "🎲 Rəqəm Tapmaca  •  ❓ Tap Görəlim\n"
        "🧠 Bilik Oyunu  •  🚩 Bayraq Oyunu\n"
        "🔗 Söz Zənciri  •  🏛 Paytaxt Tapmaca\n"
        "🚗 Plaka Oyunu  •  π Pi Oyunu\n"
        "⭕ XOX (2 nəfər)  •  🎭 Doğru/Cəsarət\n"
        "🎮 Buton Oyunu  •  ⚡ Yaddaş Şimşəyi\n"
        "🌡 İsti Soyuq  •  📚 Əsər-Müəllif\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "✍️ Oyunların çoxunda *özünüz yazırsınız* — buton yox!\n\n"
        "⚠️ Oyunlar *yalnız qrupda* işləyir!\n"
        "➡️ Botu qrupunuza əlavə edin:"
    )


def komek_text() -> str:
    return (
        "❓ *Kömək — Komandalar və Oyunlar*\n\n"
        "📌 */start* — Botu başlat\n"
        "📌 */menu* — Oyun menyusu _(qrupda)_\n"
        "📌 */xal* — Xalınıza baxın\n"
        "📌 */dur* — Aktiv oyunu dayandır\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 *Söz İzahı* — İzahı oxu, sözü *yaz*, 10 tur, ipucu + pas\n"
        "📝 *Boşluq Doldurma* — Cümləni tamamla, *yaz*, 10 tur\n"
        "🔄 *Söz Sarmalı* — Wordle, 5 hərf *yaz*, 6 cəhd\n"
        "⚡ *Sürətli Riyaziyyat* — Cavabı *yaz*, sonsuz seriya\n"
        "🎲 *Rəqəm Tapmaca* — 1-100, *yaz*, 7 cəhd\n"
        "❓ *Tap Görəlim* — Doğru/Yanlış düymə, 10 tur\n"
        "🧠 *Bilik Oyunu* — Sualı *yaz*, 10 tur, ipucu + pas\n"
        "🚩 *Bayraq Oyunu* — Ölkəni *yaz*, 10 tur, ipucu + pas\n"
        "🔗 *Söz Zənciri* — Son hərflə yeni söz *yaz*\n"
        "🏛 *Paytaxt Tapmaca* — 2 mod, *yaz*, 10 tur, ipucu + pas\n"
        "🚗 *Plaka Oyunu* — 2 mod, *yaz*, 10 tur, ipucu + pas\n"
        "π *Pi Oyunu* — Növbəti rəqəmi *yaz*\n"
        "⭕ *XOX* — 2 nəfər, qrupda düymə ilə oynayın\n"
        "🎭 *Doğru/Cəsarət* — Sual və tapşırıq düymə\n"
        "🎮 *Buton Oyunu* — Yaşıl düyməyə tez bas, 8 raund\n"
        "⚡ *Yaddaş Şimşəyi* — Emoji ardıcıllığı\n"
        "🌡 *İsti Soyuq* — 1-50, *yaz*, ipucu ilə\n"
        "📚 *Əsər-Müəllif* — Müəllifi *yaz*, 10 tur, ipucu + pas\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "⚠️ *Bütün oyunlar yalnız qrupda işləyir!*"
    )


# ── /start ────────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if is_group(update):
        await update.message.reply_text(
            f"👋 Salam, *{user.first_name}*!\n\n"
            "🎮 *Azərbaycan Oyun Botu* hazırdır!\n\n"
            "▶️ */menu* yazaraq oyunları görün.",
            parse_mode="Markdown",
        )
        return
    await update.message.reply_text(
        start_text(user.first_name),
        parse_mode="Markdown",
        reply_markup=start_kb(),
    )


# ── /menu ─────────────────────────────────────────────────────────────────────
async def cmd_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group(update):
        await update.message.reply_text(
            ONLY_GROUP_TEXT, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "➕ Qrupa Əlavə Et",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ]]),
        )
        return
    await update.message.reply_text(
        "🎮 *Oyun Menyusu*\n\nOyun seçin:",
        parse_mode="Markdown",
        reply_markup=oyun_menu_kb(),
    )


# ── /xal ──────────────────────────────────────────────────────────────────────
async def cmd_xal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    xal  = context.bot_data.get("scores", {}).get(user.full_name, 0)
    await update.message.reply_text(
        f"⭐ *{user.first_name}*, sizdə *{xal}* xal var!",
        parse_mode="Markdown",
    )


# ── /dur ──────────────────────────────────────────────────────────────────────
async def cmd_dur(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("active_game", None)
    context.user_data.pop("game_state",  None)
    chat_id = update.effective_chat.id
    context.bot_data.pop(f"xox_{chat_id}", None)
    await update.message.reply_text(
        "⏹ *Oyun dayandırıldı.*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🎮 Oyun Menyusu", callback_data="oyun_menu"),
        ]]),
    )


# ── Callback router ───────────────────────────────────────────────────────────
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query      = update.callback_query
    await query.answer()
    data       = query.data
    is_private = query.message.chat.type == "private"

    # ── Navigation ───────────────────────────────────────────────────────────
    if data == "start_menu":
        await query.edit_message_text(
            start_text(query.from_user.first_name),
            parse_mode="Markdown",
            reply_markup=start_kb(),
        )
        return

    if data == "komek":
        kb = [[InlineKeyboardButton("🔙 Geri", callback_data="start_menu")]]
        await query.edit_message_text(
            komek_text(), parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb),
        )
        return

    if data in ("oyun_menu", "ana_menu"):
        if is_private:
            await query.edit_message_text(
                ONLY_GROUP_TEXT, parse_mode="Markdown",
                reply_markup=only_group_kb(),
            )
            return
        await query.edit_message_text(
            "🎮 *Oyun Menyusu*\n\nOyun seçin:",
            parse_mode="Markdown",
            reply_markup=oyun_menu_kb(),
        )
        return

    if data == "liderlik":
        await show_liderlik(query, context, is_private)
        return

    # ── Game start ───────────────────────────────────────────────────────────
    if data.startswith("oyun_"):
        game_key = data[len("oyun_"):]
        if is_private:
            await query.edit_message_text(
                ONLY_GROUP_TEXT, parse_mode="Markdown",
                reply_markup=only_group_kb(),
            )
            return
        if game_key in GAMES:
            await GAMES[game_key].start_game(query, context)
        return

    # ── Game callbacks ───────────────────────────────────────────────────────
    for game in GAMES.values():
        if game.handles_callback(data, context, query.from_user.id):
            await game.handle_callback(query, context)
            return


# ── Message handler ───────────────────────────────────────────────────────────
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group(update):
        await update.message.reply_text(
            "👋 Oyunlar yalnız *qrupda* işləyir!\n\nBotu qrupunuza əlavə edin:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "➕ Qrupa Əlavə Et",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ]]),
        )
        return

    active = context.user_data.get("active_game")
    if active and active in GAMES:
        await GAMES[active].handle_message(update, context)


# ── Leaderboard ───────────────────────────────────────────────────────────────
async def show_liderlik(query, context, is_private: bool):
    scores = context.bot_data.get("scores", {})
    back   = "start_menu" if is_private else "ana_menu"
    if not scores:
        text = "📊 *Liderlik Cədvəli*\n\nHələ heç kim xal qazanmayıb! 🏆"
    else:
        top    = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
        medals = ["🥇","🥈","🥉"] + ["🏅"] * 7
        text   = "📊 *Liderlik Cədvəli — Top 10*\n\n"
        for i, (name, xal) in enumerate(top):
            text += f"{medals[i]} {name}: *{xal}* xal\n"
    kb = [[InlineKeyboardButton("🔙 Geri", callback_data=back)]]
    await query.edit_message_text(
        text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb),
    )


# ── bosluq_doldurma inline (buton ilə işləyir, çünki variant seçilir) ─────────
# Bu oyun üçün ayrıca inline handler lazımdır
async def bosluq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """BosluqDoldurma üçün ayrıca handler — variant seçmə düymələri"""
    pass  # bot.py-dəki callback_handler bütün oyunları idarə edir


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("menu",  cmd_menu))
    app.add_handler(CommandHandler("xal",   cmd_xal))
    app.add_handler(CommandHandler("dur",   cmd_dur))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message_handler,
    ))

    logger.info("✅ Bot işə düşdü...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
