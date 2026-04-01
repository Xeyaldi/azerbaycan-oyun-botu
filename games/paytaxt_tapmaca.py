import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

DATA = [
    ("Azərbaycan","Bakı"),("Türkiyə","Ankara"),("Rusiya","Moskva"),
    ("Almaniya","Berlin"),("Fransa","Paris"),("ABŞ","Vaşinqton"),
    ("Britaniya","London"),("Yaponiya","Tokio"),("Çin","Pekin"),
    ("Braziliya","Braziliya şəhəri"),("Hindistan","Nyu-Delhi"),
    ("Kanada","Ottava"),("Avstraliya","Kanberra"),("Gürcüstan","Tbilisi"),
    ("Ukrayna","Kiyev"),("Qazaxıstan","Astana"),("İtaliya","Roma"),
    ("İspaniya","Madrid"),("Niderland","Amsterdam"),("Portuqaliya","Lissabon"),
    ("İsveç","Stokholm"),("Norveç","Oslo"),("Meksika","Mexiko"),
    ("Argentina","Buenos-Aires"),("Mısır","Qahirə"),("Pakistan","İslamabad"),
    ("Cənubi Koreya","Seul"),("Polşa","Varşava"),("İran","Tehran"),
    ("Yunanıstan","Afina"),("İsveçrə","Bern"),("Belçika","Brüssel"),
    ("Avstriya","Vyana"),("Cənubi Afrika","Pretoriya"),("Macarıstan","Budapeşt"),
]

TURLAR    = 10
PAS_HAKKI = 2


def dashes(word):
    return " _ " * len(word)


class PaytaxtTapmaca(BaseGame):
    def __init__(self):
        super().__init__("paytaxt", "Paytaxt Tapmaca")

    def handles_callback(self, data, context, user_id):
        return data.startswith("paytaxt__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        """Mod seçim ekranı"""
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌍 Ölkədən Paytaxt",  callback_data="paytaxt__mod_olke"),
             InlineKeyboardButton("🏛 Paytaxtdan Ölkə",  callback_data="paytaxt__mod_paytaxt")],
            [InlineKeyboardButton("❌ İptal",             callback_data="ana_menu")],
        ])
        await query.edit_message_text(
            "🏛 *Paytaxt Tapmaca*\n\nOyun modunu seçin:",
            parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user

        if data in ("paytaxt__mod_olke", "paytaxt__mod_paytaxt"):
            mod  = "olke" if data == "paytaxt__mod_olke" else "paytaxt"
            pool = random.sample(DATA, min(TURLAR, len(DATA)))
            self.set_active(context)
            context.user_data["game_state"] = {
                "pool": pool, "tur": 0, "xal": 0,
                "mod": mod, "pas": PAS_HAKKI, "ipucu_gosterildi": False,
            }
            await self._sual_goster(query, context, edit=True)

        elif data == "paytaxt__ipucu":
            if st.get("ipucu_gosterildi"):
                await query.answer("İpucu artıq göstərilib!")
                return
            st["ipucu_gosterildi"] = True
            context.user_data["game_state"] = st
            await self._sual_goster(query, context, edit=True)

        elif data == "paytaxt__pas":
            if st.get("pas", 0) <= 0:
                await query.answer("Pas hakkınız qalmayıb!", show_alert=True)
                return
            pair  = st["pool"][st["tur"]]
            dogru = pair[1] if st["mod"] == "olke" else pair[0]
            st["pas"] -= 1
            st["tur"] += 1
            st["ipucu_gosterildi"] = False
            await query.answer(f"Pas! Cavab: {dogru}")
            if st["tur"] >= TURLAR:
                await self._oyun_bitdi(query, context, st, user)
            else:
                context.user_data["game_state"] = st
                await self._sual_goster(query, context, edit=True)

        elif data == "paytaxt__bitir":
            await self._oyun_bitdi(query, context, st, user)

    async def _sual_goster(self, q, context, edit=False):
        st   = context.user_data["game_state"]
        idx  = st["tur"]
        pair = st["pool"][idx]
        mod  = st["mod"]

        if mod == "olke":
            sual  = f"🌍 *{pair[0]}* ölkəsinin paytaxtı hansıdır?"
            dogru = pair[1]
        else:
            sual  = f"🏛 *{pair[1]}* hansı ölkənin paytaxtıdır?"
            dogru = pair[0]

        ipucu_line = f"💡 İpucu: *{dogru[0]}*" if st["ipucu_gosterildi"] else \
                     f"💡 İpucu: {dashes(dogru)}"

        text = (
            f"🏛 *Paytaxt Tapmaca* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
            f"{sual}\n\n"
            f"{ipucu_line}\n\n"
            "✍️ Cavabı yazın:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💡 İpucu",  callback_data="paytaxt__ipucu"),
             InlineKeyboardButton("⏭ Pas",     callback_data="paytaxt__pas")],
            [InlineKeyboardButton("🔴 Bitir",  callback_data="paytaxt__bitir")],
        ])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st    = context.user_data.get("game_state", {})
        user  = update.effective_user
        cavab = update.message.text.strip()
        pair  = st["pool"][st["tur"]]
        mod   = st["mod"]
        dogru = pair[1] if mod == "olke" else pair[0]

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
            f"🏁 *Paytaxt Tapmaca Bitdi!*\n\n"
            f"👤 {user.first_name}\n"
            f"⭐ Xal: *{st['xal']}* / {TURLAR*10}\n\n"
            f"🏆 Ümumi xal: *{context.bot_data.get('scores',{}).get(user.full_name,0)}*"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_paytaxt")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        if q:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        elif msg:
            await msg.reply_text(text, parse_mode="Markdown", reply_markup=kb)
