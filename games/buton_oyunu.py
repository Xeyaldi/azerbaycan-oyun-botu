import random, time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame


class ButonOyunu(BaseGame):
    def __init__(self):
        super().__init__("buton", "Buton Oyunu")

    def handles_callback(self, data, context, user_id):
        return data.startswith("buton__")

    def _make_kb(self, green):
        emojis = ["🔴"] * 9
        emojis[green] = "🟢"
        kb = []
        for r in range(3):
            row = []
            for c in range(3):
                i = r*3+c
                row.append(InlineKeyboardButton(emojis[i],
                    callback_data=f"buton__press_{i}_{green}"))
            kb.append(row)
        kb.append([InlineKeyboardButton("🔴 Bitir", callback_data="buton__stop")])
        return InlineKeyboardMarkup(kb)

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        green = random.randint(0, 8)
        context.user_data["game_state"] = {"raund": 1, "xal": 0, "t0": time.time()}
        await query.edit_message_text(
            "🎮 *Buton Oyunu* — Raund 1\n\n⭐ Xal: 0\n\n🟢 *Yaşıl düyməyə* tez bas!",
            parse_mode="Markdown", reply_markup=self._make_kb(green))

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data  = query.data
        st    = context.user_data.get("game_state", {})
        user  = query.from_user

        if data == "buton__stop":
            xal = st.get("xal", 0)
            self.add_score(context, user.full_name, xal)
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_buton")],
                [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
            ])
            await query.edit_message_text(
                f"⏹ *Oyun Bitdi!*\n\n⭐ Ümumi xal: *{xal}*",
                parse_mode="Markdown", reply_markup=kb)
            return

        if not data.startswith("buton__press_"):
            return
        parts = data.split("_")
        pressed, green = int(parts[-2]), int(parts[-1])
        elapsed = time.time() - st.get("t0", time.time())

        if pressed == green:
            xal_k = max(5, int(20 - elapsed * 4))
            st["xal"] = st.get("xal", 0) + xal_k
            st["raund"] = st.get("raund", 1) + 1
            self.add_score(context, user.full_name, xal_k)
            if st["raund"] > 8:
                self.clear_active(context)
                kb = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_buton")],
                    [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
                ])
                await query.edit_message_text(
                    f"🎉 *8 Raund Bitdi!*\n\n⭐ Ümumi xal: *{st['xal']}*",
                    parse_mode="Markdown", reply_markup=kb)
                return
            new_green = random.randint(0, 8)
            st["t0"] = time.time()
            context.user_data["game_state"] = st
            await query.edit_message_text(
                f"🎮 *Buton Oyunu* — Raund {st['raund']}\n\n"
                f"✅ +{xal_k} xal ({elapsed:.2f}s)\n"
                f"⭐ Xal: {st['xal']}\n\n🟢 *Yaşıl düyməyə* tez bas!",
                parse_mode="Markdown", reply_markup=self._make_kb(new_green))
        else:
            await query.answer("❌ Yanlış! −3 xal")
            st["xal"] = max(0, st.get("xal", 0) - 3)
            context.user_data["game_state"] = st
