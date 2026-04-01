import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

DATA = [
    ("Dədə Qorqud","Xalq dastanı"),("Leyli və Məcnun","Füzuli"),
    ("Xəmsə","Nizami Gəncəvi"),("Hophopnamə","M.Ə.Sabir"),
    ("Ölülər","C.Məmmədquluzadə"),("Arşın mal alan","Ü.Hacıbəyov"),
    ("Koroğlu","Xalq dastanı"),("Aydın","C.Cabbarlı"),
    ("Şamo","Seyid Hüseyn"),("Dağlar qızı Rübabə","İlyas Əfəndiyev"),
    ("Hamlet","William Shakespeare"),("Müharibə və Sülh","Lev Tolstoy"),
    ("Don Kixot","Servantes"),("Romeo və Cülyetta","William Shakespeare"),
    ("Cinayət və Cəza","Dostoyevski"),("Ana","Maksim Qorki"),
    ("Kiçik Prens","Antoine de Saint-Exupéry"),("1984","George Orwell"),
    ("Harry Potter","J.K. Rowling"),("Torpaq","Mir Cəlal"),
    ("Odisseya","Homer"),("Faust","Höte"),("Şiir Divanı","Nəsimi"),
    ("Səfərlər kitabı","Xaqani Şirvani"),("Əsli və Kərəm","Xalq dastanı"),
]

TURLAR    = 10
PAS_HAKKI = 2


def dashes(word):
    return " _ " * len(word)


class EserMuellif(BaseGame):
    def __init__(self):
        super().__init__("eser_muellif", "Əsər-Müəllif")

    def handles_callback(self, data, context, user_id):
        return data.startswith("eser_muellif__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        pool = random.sample(DATA, min(TURLAR, len(DATA)))
        context.user_data["game_state"] = {
            "pool": pool, "tur": 0, "xal": 0,
            "pas": PAS_HAKKI, "ipucu_gosterildi": False,
        }
        await self._sual_goster(query, context, edit=True)

    async def _sual_goster(self, q, context, edit=False):
        st   = context.user_data["game_state"]
        idx  = st["tur"]
        pair = st["pool"][idx]
        dogru = pair[1]
        ipucu_line = f"💡 İlk hərf: *{dogru[0]}*" if st["ipucu_gosterildi"] else \
                     f"💡 İpucu: {dashes(dogru)}"
        text = (
            f"📚 *Əsər-Müəllif* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
            f"📖 *\"{pair[0]}\"*\n\nBu əsərin müəllifi kimdir?\n\n"
            f"{ipucu_line}\n\n"
            "✍️ Müəllifi yazın:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💡 İpucu",  callback_data="eser_muellif__ipucu"),
             InlineKeyboardButton("⏭ Pas",     callback_data="eser_muellif__pas")],
            [InlineKeyboardButton("🔴 Bitir",  callback_data="eser_muellif__bitir")],
        ])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user
        if data == "eser_muellif__ipucu":
            if st.get("ipucu_gosterildi"):
                await query.answer("İpucu artıq göstərilib!"); return
            st["ipucu_gosterildi"] = True
            context.user_data["game_state"] = st
            await self._sual_goster(query, context, edit=True)
        elif data == "eser_muellif__pas":
            if st.get("pas", 0) <= 0:
                await query.answer("Pas hakkınız qalmayıb!", show_alert=True); return
            dogru = st["pool"][st["tur"]][1]
            st["pas"] -= 1; st["tur"] += 1; st["ipucu_gosterildi"] = False
            await query.answer(f"Pas! Cavab: {dogru}")
            if st["tur"] >= TURLAR:
                await self._oyun_bitdi(query, context, st, user)
            else:
                context.user_data["game_state"] = st
                await self._sual_goster(query, context, edit=True)
        elif data == "eser_muellif__bitir":
            await self._oyun_bitdi(query, context, st, user)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st    = context.user_data.get("game_state", {})
        user  = update.effective_user
        cavab = update.message.text.strip()
        dogru = st["pool"][st["tur"]][1]
        if cavab.lower() == dogru.lower():
            st["xal"] += 10
            await update.message.reply_text(f"✅ *Düzgün!* *{dogru}* +10 xal!", parse_mode="Markdown")
        else:
            await update.message.reply_text(f"❌ *Yanlış!* Düzgün: *{dogru}*", parse_mode="Markdown")
        st["tur"] += 1; st["ipucu_gosterildi"] = False
        if st["tur"] >= TURLAR:
            await self._oyun_bitdi(None, context, st, user, msg=update.message)
        else:
            context.user_data["game_state"] = st
            await self._sual_goster(update, context, edit=False)

    async def _oyun_bitdi(self, q, context, st, user, msg=None):
        self.add_score(context, user.full_name, st["xal"])
        self.clear_active(context)
        text = (f"🏁 *Əsər-Müəllif Bitdi!*\n\n👤 {user.first_name}\n"
                f"⭐ Xal: *{st['xal']}* / {TURLAR*10}\n\n"
                f"🏆 Ümumi: *{context.bot_data.get('scores',{}).get(user.full_name,0)}*")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_eser_muellif")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        if q: await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        elif msg: await msg.reply_text(text, parse_mode="Markdown", reply_markup=kb)
