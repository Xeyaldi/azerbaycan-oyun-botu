import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

SUALLAR = [
    {"s": "Azərbaycanın paytaxtı hansı şəhərdir?",              "c": "Bakı"},
    {"s": "Bakı hansı dənizin sahilindədir?",                   "c": "Xəzər"},
    {"s": "Azərbaycan hansı ildə müstəqilliyini elan etdi?",    "c": "1991"},
    {"s": "Dünyada ən böyük okean hansıdır?",                   "c": "Sakit okean"},
    {"s": "İnsan bədənində neçə sümük var?",                    "c": "206"},
    {"s": "Su neçə dərəcədə qaynayır?",                        "c": "100"},
    {"s": "Yer kürəsinin ən hündür nöqtəsi hansı dağdır?",     "c": "Everest"},
    {"s": "Günəş sistemindəki planetlərin sayı neçədir?",       "c": "8"},
    {"s": "DNA-nın tam adı nədir?",                             "c": "Deoksiribonuklein turşusu"},
    {"s": "Azərbaycanın ən uzun çayı hansıdır?",               "c": "Kür"},
    {"s": "Bakı metrosu neçənci ildə açılıb?",                 "c": "1967"},
    {"s": "Dünyada ən çox danışılan dil hansıdır?",            "c": "Mandarin"},
    {"s": "Mis elementi hansı simvolla göstərilir?",            "c": "Cu"},
    {"s": "Ən kiçik planet hansıdır?",                          "c": "Merkuri"},
    {"s": "Ən böyük planet hansıdır?",                          "c": "Yupiter"},
    {"s": "Okeanlar Yer kürəsinin neçə faizini örtür?",        "c": "71"},
    {"s": "Dünyada ən böyük ölkə hansıdır?",                   "c": "Rusiya"},
    {"s": "Azərbaycanda neçə rayon var?",                       "c": "66"},
    {"s": "Hansı heyvan dünyanın ən sürətli quşudur?",         "c": "Şahin"},
    {"s": "Avropanın ən uzun çayı hansıdır?",                   "c": "Volqa"},
    {"s": "İnsan bədəninin ən böyük orqanı nədir?",            "c": "Dəri"},
    {"s": "Hava neçə dərəcədə su donur?",                      "c": "0"},
    {"s": "Bir ildə neçə ay var?",                             "c": "12"},
    {"s": "Yer kürəsinin ən dərin nöqtəsi haradadır?",         "c": "Mariana çuxuru"},
    {"s": "Dünyada ən çox işlədilən proqramlaşdırma dili?",    "c": "Python"},
    {"s": "Azərbaycanda hansı valyuta istifadə olunur?",        "c": "Manat"},
    {"s": "İnsan bədəninin ən böyük sümüyü hansıdır?",         "c": "Bud sümüyü"},
    {"s": "Fotosintez prosesi nədir?",                          "c": "Bitkilərin işıqdan qida alması"},
    {"s": "Ən ağır metal hansıdır?",                           "c": "Osmium"},
    {"s": "Avropanın ən yüksək dağı hansıdır?",                "c": "Elbrus"},
]

TURLAR    = 10
PAS_HAKKI = 2


def dashes(word):
    return " _ " * len(word)


class BilgiOyunu(BaseGame):
    def __init__(self):
        super().__init__("bilgi", "Bilik Oyunu")

    def handles_callback(self, data, context, user_id):
        return data.startswith("bilgi__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        pool = random.sample(SUALLAR, min(TURLAR, len(SUALLAR)))
        context.user_data["game_state"] = {
            "pool": pool, "tur": 0, "xal": 0,
            "pas": PAS_HAKKI, "ipucu_gosterildi": False,
        }
        await self._sual_goster(query, context, edit=True)

    async def _sual_goster(self, q, context, edit=False):
        st  = context.user_data["game_state"]
        idx = st["tur"]
        s   = st["pool"][idx]
        dogru = s["c"]
        ipucu_line = f"💡 İlk hərf: *{dogru[0]}*" if st["ipucu_gosterildi"] else \
                     f"💡 İpucu: {dashes(dogru)}"
        text = (
            f"🧠 *Bilik Oyunu* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
            f"❓ {s['s']}\n\n"
            f"{ipucu_line}\n\n"
            "✍️ Cavabı yazın:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💡 İpucu",  callback_data="bilgi__ipucu"),
             InlineKeyboardButton("⏭ Pas",     callback_data="bilgi__pas")],
            [InlineKeyboardButton("🔴 Bitir",  callback_data="bilgi__bitir")],
        ])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user

        if data == "bilgi__ipucu":
            if st.get("ipucu_gosterildi"):
                await query.answer("İpucu artıq göstərilib!")
                return
            st["ipucu_gosterildi"] = True
            context.user_data["game_state"] = st
            await self._sual_goster(query, context, edit=True)

        elif data == "bilgi__pas":
            if st.get("pas", 0) <= 0:
                await query.answer("Pas hakkınız qalmayıb!", show_alert=True)
                return
            dogru = st["pool"][st["tur"]]["c"]
            st["pas"] -= 1
            st["tur"] += 1
            st["ipucu_gosterildi"] = False
            await query.answer(f"Pas! Cavab: {dogru}")
            if st["tur"] >= TURLAR:
                await self._oyun_bitdi(query, context, st, user)
            else:
                context.user_data["game_state"] = st
                await self._sual_goster(query, context, edit=True)

        elif data == "bilgi__bitir":
            await self._oyun_bitdi(query, context, st, user)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st    = context.user_data.get("game_state", {})
        user  = update.effective_user
        cavab = update.message.text.strip()
        dogru = st["pool"][st["tur"]]["c"]

        if cavab.lower() == dogru.lower():
            st["xal"] += 10
            await update.message.reply_text(
                f"✅ *Düzgün!* *{dogru}* +10 xal!", parse_mode="Markdown")
        else:
            await update.message.reply_text(
                f"❌ *Yanlış!* Düzgün cavab: *{dogru}*", parse_mode="Markdown")

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
            f"🏁 *Bilik Oyunu Bitdi!*\n\n"
            f"👤 {user.first_name}\n"
            f"⭐ Xal: *{st['xal']}* / {TURLAR*10}\n\n"
            f"🏆 Ümumi xal: *{context.bot_data.get('scores',{}).get(user.full_name,0)}*"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_bilgi")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        if q:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        elif msg:
            await msg.reply_text(text, parse_mode="Markdown", reply_markup=kb)
