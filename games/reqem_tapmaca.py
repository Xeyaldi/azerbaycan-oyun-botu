import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame


class ReqemTapmaca(BaseGame):
    def __init__(self):
        super().__init__("reqem_tapmaca", "Rəqəm Tapmaca")

    def handles_callback(self, data, context, user_id):
        return data.startswith("reqem_tapmaca__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        context.user_data["game_state"] = {
            "target": random.randint(1, 100), "cehdler": 0, "max": 7
        }
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="reqem_tapmaca__bitir")]])
        await query.edit_message_text(
            "🎲 *Rəqəm Tapmaca*\n\n"
            "1 ilə 100 arasında rəqəm seçdim!\n"
            "7 cəhddə tapa bilərsinizmi? 🎯\n\n"
            "✍️ Rəqəm yazın (1-100):",
            parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        if query.data == "reqem_tapmaca__bitir":
            st = context.user_data.get("game_state", {})
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_reqem_tapmaca")],
                [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
            ])
            await query.edit_message_text(
                f"⏹ Oyun bitdi. Cavab *{st.get('target','')}* idi.",
                parse_mode="Markdown", reply_markup=kb)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st   = context.user_data.get("game_state", {})
        user = update.effective_user
        try:
            guess = int(update.message.text.strip())
        except ValueError:
            await update.message.reply_text("❌ Rəqəm yazın (məs: 42)"); return
        if not (1 <= guess <= 100):
            await update.message.reply_text("❌ 1 ilə 100 arasında yazın!"); return

        target = st["target"]
        st["cehdler"] += 1
        qalan = st["max"] - st["cehdler"]
        kb_stop = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="reqem_tapmaca__bitir")]])
        kb_end  = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_reqem_tapmaca")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])

        if guess == target:
            xal = (qalan + 1) * 10
            self.add_score(context, user.full_name, xal)
            self.clear_active(context)
            await update.message.reply_text(
                f"🎉 *Tapdınız!* Rəqəm *{target}* idi!\n"
                f"🎯 {st['cehdler']} cəhddə tapdınız!\n⭐ +{xal} xal!",
                parse_mode="Markdown", reply_markup=kb_end)
        elif st["cehdler"] >= st["max"]:
            self.clear_active(context)
            await update.message.reply_text(
                f"💔 *Cəhdlər bitti!* Rəqəm *{target}* idi.",
                parse_mode="Markdown", reply_markup=kb_end)
        else:
            hint = "🔼 Daha böyük!" if guess < target else "🔽 Daha kiçik!"
            context.user_data["game_state"] = st
            await update.message.reply_text(
                f"{hint}\n\nSizin: *{guess}* | ❤️ Qalan cəhd: *{qalan}*\n\nYenidən yazın:",
                parse_mode="Markdown", reply_markup=kb_stop)
