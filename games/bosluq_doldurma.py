import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

CUMLELER = [
    {"c": "Azərbaycanın paytaxtı ___ şəhəridir.",            "d": "Bakı"},
    {"c": "Günəş ___ istiqamətdən doğur.",                   "d": "Şərq"},
    {"c": "İnsan bədəninin ən böyük orqanı ___-dır.",        "d": "Dəri"},
    {"c": "Su ___ dərəcədə qaynayır.",                       "d": "100"},
    {"c": "Bir ildə ___ ay var.",                            "d": "12"},
    {"c": "Ən böyük okean ___ okeanıdır.",                   "d": "Sakit"},
    {"c": "Azərbaycan dili ___ qrupuna aiddir.",             "d": "Türk"},
    {"c": "İnsan bədənində ___ sümük var.",                  "d": "206"},
    {"c": "Xəzər dünyanın ən böyük ___ gölüdür.",           "d": "qapalı"},
    {"c": "Hava ___ dərəcə olduqda su donur.",               "d": "0"},
    {"c": "Azərbaycanda ___ rayon var.",                     "d": "66"},
    {"c": "Bir həftədə ___ gün var.",                        "d": "7"},
    {"c": "Yer kürəsinin ən hündür nöqtəsi ___ dağıdır.",   "d": "Everest"},
    {"c": "İşığın sürəti saniyədə ___ km-dir.",             "d": "300000"},
    {"c": "Dünya günəşin ətrafında ___ ildə bir dövr edir.", "d": "1"},
    {"c": "Okeanlar Yer kürəsinin ___%-ni örtür.",           "d": "71"},
    {"c": "İnsanın normal bədən temperaturu ___ dərəcədir.", "d": "36.6"},
    {"c": "Mis elementi ___ simvolu ilə göstərilir.",        "d": "Cu"},
    {"c": "Günəş sistemindəki planetlərin sayı ___-dir.",    "d": "8"},
    {"c": "Azərbaycan ___ ildə müstəqilliyini elan etdi.",   "d": "1991"},
    {"c": "Avropanın ən uzun çayı ___ çayıdır.",             "d": "Volqa"},
    {"c": "İnsan bədəninin ən böyük sümüyü ___ sümüyüdür.", "d": "bud"},
    {"c": "Dünyanın ən böyük ölkəsi ___-dır.",               "d": "Rusiya"},
    {"c": "Bakı ___ dənizinin sahilindədir.",                "d": "Xəzər"},
    {"c": "Azərbaycan valyutası ___-dır.",                   "d": "Manat"},
]

TURLAR    = 10
PAS_HAKKI = 2


def dashes(word):
    return " _ " * len(word)


class BosluqDoldurma(BaseGame):
    def __init__(self):
        super().__init__("bosluq", "Boşluq Doldurma")

    def handles_callback(self, data, context, user_id):
        return data.startswith("bosluq__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        pool = random.sample(CUMLELER, min(TURLAR, len(CUMLELER)))
        context.user_data["game_state"] = {
            "pool": pool, "tur": 0, "xal": 0,
            "pas": PAS_HAKKI, "ipucu_gosterildi": False,
        }
        await self._sual_goster(query, context, edit=True)

    async def _sual_goster(self, q, context, edit=False):
        st  = context.user_data["game_state"]
        idx = st["tur"]
        s   = st["pool"][idx]
        dogru = s["d"]
        ipucu_line = f"💡 İlk hərf: *{dogru[0]}*" if st["ipucu_gosterildi"] else \
                     f"💡 İpucu: {dashes(dogru)}"
        text = (
            f"📝 *Boşluq Doldurma* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
            f"🔤 {s['c']}\n\n"
            f"{ipucu_line}\n\n"
            "✍️ Boşluğu doldurun:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💡 İpucu",  callback_data="bosluq__ipucu"),
             InlineKeyboardButton("⏭ Pas",     callback_data="bosluq__pas")],
            [InlineKeyboardButton("🔴 Bitir",  callback_data="bosluq__bitir")],
        ])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user

        if data == "bosluq__ipucu":
            if st.get("ipucu_gosterildi"):
                await query.answer("İpucu artıq göstərilib!"); return
            st["ipucu_gosterildi"] = True
            context.user_data["game_state"] = st
            await self._sual_goster(query, context, edit=True)

        elif data == "bosluq__pas":
            if st.get("pas", 0) <= 0:
                await query.answer("Pas hakkınız qalmayıb!", show_alert=True); return
            dogru = st["pool"][st["tur"]]["d"]
            st["pas"] -= 1; st["tur"] += 1; st["ipucu_gosterildi"] = False
            await query.answer(f"Pas! Cavab: {dogru}")
            if st["tur"] >= TURLAR:
                await self._oyun_bitdi(query, context, st, user)
            else:
                context.user_data["game_state"] = st
                await self._sual_goster(query, context, edit=True)

        elif data == "bosluq__bitir":
            await self._oyun_bitdi(query, context, st, user)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st    = context.user_data.get("game_state", {})
        user  = update.effective_user
        cavab = update.message.text.strip()
        dogru = st["pool"][st["tur"]]["d"]

        if cavab.lower() == dogru.lower():
            st["xal"] += 10
            filled = st["pool"][st["tur"]]["c"].replace("___", f"*{dogru}*")
            await update.message.reply_text(
                f"✅ *Düzgün!* +10 xal!\n\n{filled}", parse_mode="Markdown")
        else:
            filled = st["pool"][st["tur"]]["c"].replace("___", f"*{dogru}*")
            await update.message.reply_text(
                f"❌ *Yanlış!* Düzgün: *{dogru}*\n\n{filled}", parse_mode="Markdown")

        st["tur"] += 1; st["ipucu_gosterildi"] = False
        if st["tur"] >= TURLAR:
            await self._oyun_bitdi(None, context, st, user, msg=update.message)
        else:
            context.user_data["game_state"] = st
            await self._sual_goster(update, context, edit=False)

    async def _oyun_bitdi(self, q, context, st, user, msg=None):
        self.add_score(context, user.full_name, st["xal"])
        self.clear_active(context)
        text = (
            f"🏁 *Boşluq Doldurma Bitdi!*\n\n"
            f"👤 {user.first_name}\n"
            f"⭐ Xal: *{st['xal']}* / {TURLAR*10}\n\n"
            f"🏆 Ümumi xal: *{context.bot_data.get('scores',{}).get(user.full_name,0)}*"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_bosluq")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        if q:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        elif msg:
            await msg.reply_text(text, parse_mode="Markdown", reply_markup=kb)
