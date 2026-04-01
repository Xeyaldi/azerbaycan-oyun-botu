import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

SOZLER = ["qalib","qanat","sabah","salam","tarix","zaman","aslan",
          "insan","gunes","bulud","deniz","kitab","bayrq","torpq",
          "meşei","dağli","evler","çayır","nefts","şəhər","vətən",
          "kəndl","köhnə","yolun","sudan","qızıl","daşlı","ağacl"]
SOZLER_5 = list({s for s in SOZLER if len(s) == 5})
extra = ["qalib","qanat","sabah","salam","tarix","zaman","aslan","insan"]
SOZLER_5 = list(set(SOZLER_5 + extra))
MAX = 6


def check(guess, target):
    marks = ["⬛"] * 5
    used  = [False] * 5
    for i in range(5):
        if guess[i] == target[i]:
            marks[i] = "🟩"; used[i] = True
    for i in range(5):
        if marks[i] == "🟩": continue
        for j in range(5):
            if not used[j] and guess[i] == target[j]:
                marks[i] = "🟨"; used[j] = True; break
    return marks


class SozSarmali(BaseGame):
    def __init__(self):
        super().__init__("soz_sarmali", "Söz Sarmalı")

    def handles_callback(self, data, context, user_id):
        return data.startswith("soz_sarmali__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        target = random.choice(SOZLER_5)
        context.user_data["game_state"] = {"target": target, "cehdler": [], "bitmis": False}
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="soz_sarmali__bitir")]])
        await query.edit_message_text(
            "🔄 *Söz Sarmalı (Wordle)*\n\n"
            "5 hərfli Azərbaycan sözünü 6 cəhddə tap!\n\n"
            "🟩 Düzgün hərf, düzgün yer\n"
            "🟨 Düzgün hərf, yanlış yer\n"
            "⬛ Hərf yoxdur\n\n"
            f"❓ Cəhd: 0/{MAX}\n\n"
            "✍️ 5 hərfli söz yazın:",
            parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        if query.data == "soz_sarmali__bitir":
            st = context.user_data.get("game_state", {})
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_soz_sarmali")],
                [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
            ])
            await query.edit_message_text(
                f"⏹ Oyun bitdi. Söz *{st.get('target','').upper()}* idi.",
                parse_mode="Markdown", reply_markup=kb)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st = context.user_data.get("game_state", {})
        if st.get("bitmis"): return
        user   = update.effective_user
        guess  = update.message.text.strip().lower()
        target = st.get("target", "")
        if len(guess) != 5:
            await update.message.reply_text("❌ Mütləq 5 hərfli söz yazın!"); return
        if not guess.isalpha():
            await update.message.reply_text("❌ Yalnız hərf istifadə edin!"); return
        marks   = check(guess, target)
        cehdler = st.get("cehdler", [])
        cehdler.append((guess.upper(), marks))
        st["cehdler"] = cehdler
        board = ""
        for g, m in cehdler:
            board += " ".join(m) + "\n"
            board += " ".join(list(g)) + "\n\n"
        n = len(cehdler)
        kb_end = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_soz_sarmali")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        if guess == target:
            st["bitmis"] = True
            xal = (MAX - n + 1) * 15
            self.add_score(context, user.full_name, xal)
            self.clear_active(context)
            await update.message.reply_text(
                f"🎉 *Tapdınız!* Söz: *{target.upper()}*\n\n{board}⭐ +{xal} xal! ({n} cəhd)",
                parse_mode="Markdown", reply_markup=kb_end)
        elif n >= MAX:
            st["bitmis"] = True
            self.clear_active(context)
            await update.message.reply_text(
                f"💔 *Cəhdlər bitti!* Düzgün: *{target.upper()}*\n\n{board}",
                parse_mode="Markdown", reply_markup=kb_end)
        else:
            context.user_data["game_state"] = st
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔴 Bitir", callback_data="soz_sarmali__bitir")]])
            await update.message.reply_text(
                f"🔄 *Söz Sarmalı*\n\n{board}❓ Cəhd: {n}/{MAX}\n\n✍️ Davam edin:",
                parse_mode="Markdown", reply_markup=kb)
