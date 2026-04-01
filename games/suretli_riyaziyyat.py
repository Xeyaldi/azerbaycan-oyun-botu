import random, time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame


def gen_sual(level=1):
    ops = ["+", "-"] if level == 1 else ["+", "-", "*"]
    op  = random.choice(ops)
    lim = 20 * level
    if op == "+":
        a, b = random.randint(1, lim), random.randint(1, lim); ans = a + b
    elif op == "-":
        a, b = random.randint(lim//2, lim), random.randint(1, lim//2); ans = a - b
    else:
        a, b = random.randint(2, min(12,lim)), random.randint(2, min(12,lim)); ans = a * b
    return f"{a} {op} {b}", ans


class SuretliRiyaziyyat(BaseGame):
    def __init__(self):
        super().__init__("suretli_riyaz", "Sürətli Riyaziyyat")

    def handles_callback(self, data, context, user_id):
        return data.startswith("suretli_riyaz__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        sual, cavab = gen_sual(1)
        context.user_data["game_state"] = {
            "cavab": cavab, "sual": sual, "seriya": 0, "t0": time.time()
        }
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="suretli_riyaz__bitir")]])
        await query.edit_message_text(
            f"⚡ *Sürətli Riyaziyyat*\n\n"
            f"🔢 *{sual} = ?*\n\n"
            f"🔥 Seriya: 0\n\n"
            "✍️ Cavabı yazın:",
            parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        if query.data == "suretli_riyaz__bitir":
            st = context.user_data.get("game_state", {})
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_suretli_riyaz")],
                [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
            ])
            await query.edit_message_text(
                f"⏹ *Oyun Bitdi!*\n\n🔥 Seriya: {st.get('seriya',0)}",
                parse_mode="Markdown", reply_markup=kb)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st   = context.user_data.get("game_state", {})
        user = update.effective_user
        try:
            secim = int(update.message.text.strip())
        except ValueError:
            await update.message.reply_text("❌ Rəqəm yazın!"); return

        dogru  = st.get("cavab")
        seriya = st.get("seriya", 0)
        keçen  = time.time() - st.get("t0", time.time())
        kb_stop = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="suretli_riyaz__bitir")]])
        kb_end  = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_suretli_riyaz")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])

        if secim == dogru:
            seriya += 1
            xal = 10 + seriya * 2
            self.add_score(context, user.full_name, xal)
            level = min((seriya // 3) + 1, 5)
            sual, cavab = gen_sual(level)
            st.update({"cavab": cavab, "sual": sual, "seriya": seriya, "t0": time.time()})
            context.user_data["game_state"] = st
            await update.message.reply_text(
                f"✅ *Düzgün!* +{xal} xal ({keçen:.1f}s)\n\n"
                f"⚡ *Sürətli Riyaziyyat*\n\n"
                f"🔢 *{sual} = ?*\n\n"
                f"🔥 Seriya: {seriya}\n\n✍️ Cavabı yazın:",
                parse_mode="Markdown", reply_markup=kb_stop)
        else:
            self.clear_active(context)
            await update.message.reply_text(
                f"❌ *Yanlış!* Düzgün: *{dogru}*\n\n🔥 Seriya: {seriya} sualda bitdi!",
                parse_mode="Markdown", reply_markup=kb_end)
