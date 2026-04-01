import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame


class IstiSoyuq(BaseGame):
    def __init__(self):
        super().__init__("isti_soyuq", "İsti Soyuq")

    def handles_callback(self, data, context, user_id):
        return data.startswith("isti_soyuq__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        context.user_data["game_state"] = {
            "target": random.randint(1, 50), "cehdler": 0
        }
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="isti_soyuq__bitir")]])
        await query.edit_message_text(
            "🌡 *İsti Soyuq*\n\n"
            "1 ilə 50 arasında rəqəm seçdim!\n\n"
            "🔥🔥🔥 Qaynar → çox yaxınsınız (1-3)\n"
            "🔥🔥 İsti → yaxınsınız (4-7)\n"
            "🌡 Ilıq → orta (8-12)\n"
            "❄️ Soyuq → uzaqsınız (13-30)\n"
            "🥶 Donmuş → çox uzaqsınız (31+)\n\n"
            "✍️ Rəqəm yazın (1-50):",
            parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        if query.data == "isti_soyuq__bitir":
            st = context.user_data.get("game_state", {})
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_isti_soyuq")],
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
            await update.message.reply_text("❌ Rəqəm yazın (1-50)"); return
        if not (1 <= guess <= 50):
            await update.message.reply_text("❌ 1 ilə 50 arasında yazın!"); return

        target = st["target"]
        st["cehdler"] = st.get("cehdler", 0) + 1
        diff = abs(guess - target)
        kb_stop = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="isti_soyuq__bitir")]])
        kb_end  = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_isti_soyuq")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])

        if guess == target:
            xal = max(10, 50 - st["cehdler"] * 4)
            self.add_score(context, user.full_name, xal)
            self.clear_active(context)
            await update.message.reply_text(
                f"🎉 *Tapdınız!* Rəqəm *{target}* idi!\n"
                f"🎯 {st['cehdler']} cəhddə tapdınız!\n⭐ +{xal} xal!",
                parse_mode="Markdown", reply_markup=kb_end)
        else:
            temp = ("🔥🔥🔥 QAYNAR!" if diff<=3 else "🔥🔥 Çox İsti!" if diff<=7
                    else "🌡 İsti" if diff<=12 else "❄️ Soyuq" if diff<=30 else "🥶 Donmuş!")
            yon = "⬆️ Daha böyük" if guess < target else "⬇️ Daha kiçik"
            context.user_data["game_state"] = st
            await update.message.reply_text(
                f"{temp}\n{yon}\n\nSizin: *{guess}* | Cəhd: {st['cehdler']}\n\nYenidən yazın:",
                parse_mode="Markdown", reply_markup=kb_stop)
