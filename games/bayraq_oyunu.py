import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

# (ölkə adı, bayraq emoji URL, ipucu - ilk hərf)
BAYRAQLАР = [
    {"olke": "Azərbaycan",          "emoji": "🇦🇿", "ipucu": "A"},
    {"olke": "Türkiyə",             "emoji": "🇹🇷", "ipucu": "T"},
    {"olke": "Rusiya",              "emoji": "🇷🇺", "ipucu": "R"},
    {"olke": "Almaniya",            "emoji": "🇩🇪", "ipucu": "A"},
    {"olke": "Fransa",              "emoji": "🇫🇷", "ipucu": "F"},
    {"olke": "İtaliya",             "emoji": "🇮🇹", "ipucu": "İ"},
    {"olke": "İspaniya",            "emoji": "🇪🇸", "ipucu": "İ"},
    {"olke": "Britaniya",           "emoji": "🇬🇧", "ipucu": "B"},
    {"olke": "ABŞ",                 "emoji": "🇺🇸", "ipucu": "A"},
    {"olke": "Yaponiya",            "emoji": "🇯🇵", "ipucu": "Y"},
    {"olke": "Çin",                 "emoji": "🇨🇳", "ipucu": "Ç"},
    {"olke": "Braziliya",           "emoji": "🇧🇷", "ipucu": "B"},
    {"olke": "Hindistan",           "emoji": "🇮🇳", "ipucu": "H"},
    {"olke": "Kanada",              "emoji": "🇨🇦", "ipucu": "K"},
    {"olke": "Avstraliya",          "emoji": "🇦🇺", "ipucu": "A"},
    {"olke": "Gürcüstan",           "emoji": "🇬🇪", "ipucu": "G"},
    {"olke": "Ukrayna",             "emoji": "🇺🇦", "ipucu": "U"},
    {"olke": "Qazaxıstan",          "emoji": "🇰🇿", "ipucu": "Q"},
    {"olke": "İsveç",               "emoji": "🇸🇪", "ipucu": "İ"},
    {"olke": "Norveç",              "emoji": "🇳🇴", "ipucu": "N"},
    {"olke": "Polşa",               "emoji": "🇵🇱", "ipucu": "P"},
    {"olke": "Niderland",           "emoji": "🇳🇱", "ipucu": "N"},
    {"olke": "Portuqaliya",         "emoji": "🇵🇹", "ipucu": "P"},
    {"olke": "Meksika",             "emoji": "🇲🇽", "ipucu": "M"},
    {"olke": "Argentina",           "emoji": "🇦🇷", "ipucu": "A"},
    {"olke": "Cənubi Koreya",       "emoji": "🇰🇷", "ipucu": "C"},
    {"olke": "Mısır",               "emoji": "🇪🇬", "ipucu": "M"},
    {"olke": "Cənubi Afrika",       "emoji": "🇿🇦", "ipucu": "C"},
    {"olke": "Pakistan",            "emoji": "🇵🇰", "ipucu": "P"},
    {"olke": "Səudiyyə Ərəbistanı","emoji": "🇸🇦", "ipucu": "S"},
    {"olke": "İran",                "emoji": "🇮🇷", "ipucu": "İ"},
    {"olke": "Yunanıstan",          "emoji": "🇬🇷", "ipucu": "Y"},
    {"olke": "İsveçrə",             "emoji": "🇨🇭", "ipucu": "İ"},
    {"olke": "Belçika",             "emoji": "🇧🇪", "ipucu": "B"},
    {"olke": "Avstriya",            "emoji": "🇦🇹", "ipucu": "A"},
]

TURLAR   = 10
PAS_HAKKI = 3


def dashes(word):
    return " _ " * len(word)


class BayraqOyunu(BaseGame):
    def __init__(self):
        super().__init__("bayraq", "Bayraq Oyunu")

    def handles_callback(self, data, context, user_id):
        return data.startswith("bayraq__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        pool = random.sample(BAYRAQLАР, min(TURLAR, len(BAYRAQLАР)))
        context.user_data["game_state"] = {
            "pool": pool, "tur": 0, "xal": 0,
            "pas": PAS_HAKKI, "ipucu_gosterildi": False,
        }
        await self._sual_goster(query, context, edit=True)

    async def _sual_goster(self, q, context, edit=False):
        st  = context.user_data["game_state"]
        idx = st["tur"]
        s   = st["pool"][idx]
        ipucu_line = f"💡 İpucu: *{s['ipucu']}*" if st["ipucu_gosterildi"] else \
                     f"💡 İpucu: {dashes(s['olke'])}"
        text = (
            f"🚩 *Bayraq Oyunu* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
            f"Bu bayraq hansı ölkəyə aiddir?\n\n"
            f"{s['emoji']}\n\n"
            f"{ipucu_line}\n\n"
            "✍️ Ölkə adını yazın:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💡 İpucu",  callback_data="bayraq__ipucu"),
             InlineKeyboardButton("⏭ Pas",     callback_data="bayraq__pas")],
            [InlineKeyboardButton("🔴 Bitir",  callback_data="bayraq__bitir")],
        ])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user

        if data == "bayraq__ipucu":
            if st.get("ipucu_gosterildi"):
                await query.answer("İpucu artıq göstərilib!")
                return
            st["ipucu_gosterildi"] = True
            context.user_data["game_state"] = st
            await self._sual_goster(query, context, edit=True)

        elif data == "bayraq__pas":
            if st.get("pas", 0) <= 0:
                await query.answer("Pas hakkınız qalmayıb!", show_alert=True)
                return
            dogru = st["pool"][st["tur"]]["olke"]
            st["pas"] -= 1
            st["tur"] += 1
            st["ipucu_gosterildi"] = False
            await query.answer(f"Pas! Cavab: {dogru}")
            if st["tur"] >= TURLAR:
                await self._oyun_bitdi(query, context, st, user)
            else:
                context.user_data["game_state"] = st
                await self._sual_goster(query, context, edit=True)

        elif data == "bayraq__bitir":
            await self._oyun_bitdi(query, context, st, user)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st   = context.user_data.get("game_state", {})
        user = update.effective_user
        cavab = update.message.text.strip()
        s     = st["pool"][st["tur"]]
        dogru = s["olke"]

        if cavab.lower() == dogru.lower():
            st["xal"] += 10
            await update.message.reply_text(
                f"✅ *Düzgün!* {s['emoji']} = *{dogru}* +10 xal!", parse_mode="Markdown")
        else:
            await update.message.reply_text(
                f"❌ *Yanlış!* {s['emoji']} = *{dogru}*", parse_mode="Markdown")

        st["tur"] += 1
        st["ipucu_gosterildi"] = False
        if st["tur"] >= TURLAR:
            await self._oyun_bitdi(None, context, st, user, msg=update.message)
        else:
            context.user_data["game_state"] = st
            await self._sual_goster(update, context, edit=False)

    async def _oyun_bitdi(self, q, context, st, user, msg=None):
        self.add_score(context, user.full_name, st["xal"])
        self.clear_active(context)
        text = (
            f"🏁 *Bayraq Oyunu Bitdi!*\n\n"
            f"👤 {user.first_name}\n"
            f"⭐ Xal: *{st['xal']}* / {TURLAR*10}\n\n"
            f"🏆 Ümumi xal: *{context.bot_data.get('scores',{}).get(user.full_name,0)}*"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_bayraq")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        if q:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        elif msg:
            await msg.reply_text(text, parse_mode="Markdown", reply_markup=kb)
