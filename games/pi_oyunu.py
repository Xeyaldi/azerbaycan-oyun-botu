import random, time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

PI = "14159265358979323846264338327950288419716939937510"


class PiOyunu(BaseGame):
    def __init__(self):
        super().__init__("pi", "Pi Oyunu")

    def handles_callback(self, data, context, user_id):
        return data.startswith("pi__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        context.user_data["game_state"] = {"idx": 0, "say": 0}
        await self._sual_goster(query, context, edit=True)

    async def _sual_goster(self, q, context, edit=False):
        st  = context.user_data.get("game_state", {})
        idx = st.get("idx", 0)
        say = st.get("say", 0)
        shown = "3." + PI[:idx] if idx > 0 else "3."
        text = (
            f"π *Pi Oyunu*\n\n"
            f"π = `{shown}` *?*\n\n"
            f"Növbəti rəqəm nədir?\n\n"
            f"✅ Düzgün: {say}  •  📍 Mövqe: {idx+1}\n\n"
            "✍️ Rəqəmi yazın (0-9):"
        )
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="pi__bitir")]])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        if query.data == "pi__bitir":
            st  = context.user_data.get("game_state", {})
            say = st.get("say", 0)
            user = query.from_user
            self.add_score(context, user.full_name, say * 5)
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_pi")],
                [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
            ])
            await query.edit_message_text(
                f"⏹ *Pi Oyunu Bitdi!*\n\n🔢 {say} rəqəm düzgün tapdınız!\n⭐ +{say*5} xal",
                parse_mode="Markdown", reply_markup=kb)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st   = context.user_data.get("game_state", {})
        user = update.effective_user
        try:
            secim = int(update.message.text.strip())
            assert 0 <= secim <= 9
        except (ValueError, AssertionError):
            await update.message.reply_text("❌ 0-9 arasında rəqəm yazın!"); return

        idx     = st.get("idx", 0)
        correct = int(PI[idx])

        if secim == correct:
            st["idx"] = idx + 1
            st["say"] = st.get("say", 0) + 1
            self.add_score(context, user.full_name, 5)
            context.user_data["game_state"] = st
            await update.message.reply_text(f"✅ *Düzgün!* +5 xal", parse_mode="Markdown")
            await self._sual_goster(update, context, edit=False)
        else:
            say = st.get("say", 0)
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_pi")],
                [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
            ])
            await update.message.reply_text(
                f"❌ *Yanlış!* Düzgün rəqəm: *{correct}*\n\n"
                f"π = 3.{PI[:idx]}\n\n"
                f"🔢 {say} rəqəm düzgün tapdınız!\n⭐ +{say*5} xal",
                parse_mode="Markdown", reply_markup=kb)
