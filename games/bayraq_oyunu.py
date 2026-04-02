import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

BAYRAQLАР = [
    {"olke":"Azərbaycan",   "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Flag_of_Azerbaijan.svg/1280px-Flag_of_Azerbaijan.svg.png",    "ipucu":"A","herf":10},
    {"olke":"Türkiyə",      "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Flag_of_Turkey.svg/1280px-Flag_of_Turkey.svg.png",            "ipucu":"T","herf":8},
    {"olke":"Rusiya",       "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Russia.svg/1280px-Flag_of_Russia.svg.png",            "ipucu":"R","herf":6},
    {"olke":"Almaniya",     "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Flag_of_Germany.svg/1280px-Flag_of_Germany.svg.png",          "ipucu":"A","herf":8},
    {"olke":"Fransa",       "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Flag_of_France.svg/1280px-Flag_of_France.svg.png",            "ipucu":"F","herf":6},
    {"olke":"İtaliya",      "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Flag_of_Italy.svg/1280px-Flag_of_Italy.svg.png",              "ipucu":"İ","herf":7},
    {"olke":"İspaniya",     "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Flag_of_Spain.svg/1280px-Flag_of_Spain.svg.png",              "ipucu":"İ","herf":8},
    {"olke":"Britaniya",    "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Flag_of_the_United_Kingdom.svg/1280px-Flag_of_the_United_Kingdom.svg.png","ipucu":"B","herf":9},
    {"olke":"ABŞ",          "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Flag_of_the_United_States.svg/1280px-Flag_of_the_United_States.svg.png","ipucu":"A","herf":3},
    {"olke":"Yaponiya",     "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Flag_of_Japan.svg/1280px-Flag_of_Japan.svg.png",              "ipucu":"Y","herf":8},
    {"olke":"Çin",          "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/1280px-Flag_of_the_People%27s_Republic_of_China.svg.png","ipucu":"Ç","herf":3},
    {"olke":"Braziliya",    "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/1280px-Flag_of_Brazil.svg.png",            "ipucu":"B","herf":9},
    {"olke":"Hindistan",    "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_India.svg/1280px-Flag_of_India.svg.png",              "ipucu":"H","herf":8},
    {"olke":"Kanada",       "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_Canada_%28Pantone%29.svg/1280px-Flag_of_Canada_%28Pantone%29.svg.png","ipucu":"K","herf":6},
    {"olke":"Avstraliya",   "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Flag_of_Australia_%28converted%29.svg/1280px-Flag_of_Australia_%28converted%29.svg.png","ipucu":"A","herf":9},
    {"olke":"Gürcüstan",    "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Flag_of_Georgia.svg/1280px-Flag_of_Georgia.svg.png",          "ipucu":"G","herf":8},
    {"olke":"Ukrayna",      "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Ukraine.svg/1280px-Flag_of_Ukraine.svg.png",          "ipucu":"U","herf":7},
    {"olke":"Qazaxıstan",   "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Flag_of_Kazakhstan.svg/1280px-Flag_of_Kazakhstan.svg.png",    "ipucu":"Q","herf":10},
    {"olke":"İsveç",        "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Flag_of_Sweden.svg/1280px-Flag_of_Sweden.svg.png",            "ipucu":"İ","herf":5},
    {"olke":"Norveç",       "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Flag_of_Norway.svg/1280px-Flag_of_Norway.svg.png",            "ipucu":"N","herf":6},
    {"olke":"Polşa",        "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Flag_of_Poland.svg/1280px-Flag_of_Poland.svg.png",            "ipucu":"P","herf":5},
    {"olke":"Niderland",    "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Flag_of_the_Netherlands.svg/1280px-Flag_of_the_Netherlands.svg.png","ipucu":"N","herf":9},
    {"olke":"Portuqaliya",  "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_Portugal.svg/1280px-Flag_of_Portugal.svg.png",        "ipucu":"P","herf":11},
    {"olke":"Meksika",      "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Flag_of_Mexico.svg/1280px-Flag_of_Mexico.svg.png",            "ipucu":"M","herf":7},
    {"olke":"Argentina",    "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Flag_of_Argentina.svg/1280px-Flag_of_Argentina.svg.png",      "ipucu":"A","herf":9},
    {"olke":"Cənubi Koreya","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/1280px-Flag_of_South_Korea.svg.png",  "ipucu":"C","herf":13},
    {"olke":"Mısır",        "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Flag_of_Egypt.svg/1280px-Flag_of_Egypt.svg.png",              "ipucu":"M","herf":5},
    {"olke":"Cənubi Afrika","url":"https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Flag_of_South_Africa.svg/1280px-Flag_of_South_Africa.svg.png","ipucu":"C","herf":13},
    {"olke":"Pakistan",     "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Flag_of_Pakistan.svg/1280px-Flag_of_Pakistan.svg.png",        "ipucu":"P","herf":8},
    {"olke":"İran",         "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Flag_of_Iran.svg/1280px-Flag_of_Iran.svg.png",                "ipucu":"İ","herf":4},
    {"olke":"Yunanıstan",   "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Flag_of_Greece.svg/1280px-Flag_of_Greece.svg.png",            "ipucu":"Y","herf":10},
    {"olke":"İsveçrə",      "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Switzerland.svg/800px-Flag_of_Switzerland.svg.png",   "ipucu":"İ","herf":8},
    {"olke":"Belçika",      "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Flag_of_Belgium.svg/1280px-Flag_of_Belgium.svg.png",          "ipucu":"B","herf":7},
    {"olke":"Avstriya",     "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Flag_of_Austria.svg/1280px-Flag_of_Austria.svg.png",          "ipucu":"A","herf":8},
    {"olke":"Ermənistan",   "url":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Flag_of_Armenia.svg/1280px-Flag_of_Armenia.svg.png",          "ipucu":"E","herf":9},
]

TURLAR        = 10
PAS_HAKKI     = 3
XAL_IPUCUSUZ  = 15   # ipucu almadan düzgün cavab
XAL_IPUCULU   = 8    # ipucu alandan sonra düzgün cavab


def dashes(n):
    return "＿ " * n


class BayraqOyunu(BaseGame):
    def __init__(self):
        super().__init__("bayraq", "Bayraq Oyunu")

    def handles_callback(self, data, context, user_id):
        return data.startswith("bayraq__")

    # ── Oyunu başlat ──────────────────────────────────────────────────────────
    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        pool = random.sample(BAYRAQLАР, min(TURLAR, len(BAYRAQLАР)))
        context.user_data["game_state"] = {
            "pool": pool, "tur": 0, "xal": 0,
            "pas": PAS_HAKKI, "ipucu_gosterildi": False,
        }
        # Köhnə menyunu sil, bayraq foto göndər
        try:
            await query.message.delete()
        except Exception:
            pass
        await self._foto_gonder(query.message.chat_id, context)

    # ── Bayraq fotosunu göndər ────────────────────────────────────────────────
    async def _foto_gonder(self, chat_id, context):
        st  = context.user_data["game_state"]
        idx = st["tur"]
        s   = st["pool"][idx]

        ipucu_line = (
            f"💡 İlk hərf: *{s['ipucu']}*\n"
            f"🔤 {dashes(s['herf'])}"
            if st["ipucu_gosterildi"]
            else f"🔤 {dashes(s['herf'])}"
        )
        caption = (
            f"🚩 *Bayraq Oyunu* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
            f"❓ Bu bayraq hansı ölkəyə aiddir?\n\n"
            f"{ipucu_line}\n\n"
            "✍️ Ölkə adını yazın:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💡 İpucu",  callback_data="bayraq__ipucu"),
             InlineKeyboardButton("⏭ Pas",     callback_data="bayraq__pas")],
            [InlineKeyboardButton("🔴 Bitir",  callback_data="bayraq__bitir")],
        ])
        msg = await context.bot.send_photo(
            chat_id=chat_id,
            photo=s["url"],
            caption=caption,
            parse_mode="Markdown",
            reply_markup=kb,
        )
        # Son mesaj ID-sini saxla (caption yeniləmək üçün)
        context.user_data["game_state"]["last_msg_id"] = msg.message_id

    # ── Callback ──────────────────────────────────────────────────────────────
    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user

        if data == "bayraq__ipucu":
            if st.get("ipucu_gosterildi"):
                await query.answer("💡 İpucu artıq göstərilib!")
                return
            st["ipucu_gosterildi"] = True
            context.user_data["game_state"] = st
            # Caption-u yenilə
            s   = st["pool"][st["tur"]]
            idx = st["tur"]
            caption = (
                f"🚩 *Bayraq Oyunu* | Tur {idx+1}/{TURLAR}\n"
                f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
                f"❓ Bu bayraq hansı ölkəyə aiddir?\n\n"
                f"💡 İlk hərf: *{s['ipucu']}*\n"
                f"🔤 {dashes(s['herf'])}\n\n"
                "✍️ Ölkə adını yazın:"
            )
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("💡 İpucu (göstərilib)", callback_data="bayraq__noop"),
                 InlineKeyboardButton("⏭ Pas",                 callback_data="bayraq__pas")],
                [InlineKeyboardButton("🔴 Bitir",              callback_data="bayraq__bitir")],
            ])
            try:
                await query.edit_message_caption(
                    caption=caption, parse_mode="Markdown", reply_markup=kb
                )
            except Exception:
                await query.answer(f"💡 İlk hərf: {s['ipucu']}")

        elif data == "bayraq__noop":
            await query.answer("💡 İpucu artıq göstərilib!")

        elif data == "bayraq__pas":
            if st.get("pas", 0) <= 0:
                await query.answer("⚠️ Pas hakkınız qalmayıb!", show_alert=True)
                return
            dogru = st["pool"][st["tur"]]["olke"]
            st["pas"] -= 1
            st["tur"] += 1
            st["ipucu_gosterildi"] = False
            await query.answer(f"⏭ Pas! Cavab: {dogru}")
            # Köhnə fotonu sil
            try:
                await query.message.delete()
            except Exception:
                pass
            if st["tur"] >= TURLAR:
                context.user_data["game_state"] = st
                await self._bitir_mesaj(query.message.chat_id, context, st, user)
            else:
                context.user_data["game_state"] = st
                await self._foto_gonder(query.message.chat_id, context)

        elif data == "bayraq__bitir":
            try:
                await query.message.delete()
            except Exception:
                pass
            await self._bitir_mesaj(query.message.chat_id, context, st, user)

    # ── Mesaj (cavab) ─────────────────────────────────────────────────────────
    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st   = context.user_data.get("game_state", {})
        if not st:
            return
        user  = update.effective_user
        cavab = update.message.text.strip()
        s     = st["pool"][st["tur"]]
        dogru = s["olke"]

        if cavab.lower() == dogru.lower():
            xal = XAL_IPUCUSUZ if not st["ipucu_gosterildi"] else XAL_IPUCULU
            st["xal"] += xal
            await update.message.reply_text(
                f"✅ *Düzgün!* 🎉\n\n"
                f"🚩 Bu *{dogru}* bayrağı idi!\n"
                f"⭐ +{xal} xal!",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"❌ *Yanlış!*\n\n"
                f"🚩 Bu *{dogru}* bayrağı idi.\n"
                f"💪 Növbəti bayrağa hazır olun!",
                parse_mode="Markdown"
            )

        st["tur"] += 1
        st["ipucu_gosterildi"] = False

        # Köhnə bayraq şəklini sil
        last_id = st.get("last_msg_id")
        if last_id:
            try:
                await context.bot.delete_message(
                    chat_id=update.effective_chat.id,
                    message_id=last_id
                )
            except Exception:
                pass

        if st["tur"] >= TURLAR:
            context.user_data["game_state"] = st
            await self._bitir_mesaj(update.effective_chat.id, context, st, user)
        else:
            context.user_data["game_state"] = st
            await self._foto_gonder(update.effective_chat.id, context)

    # ── Oyun bitdi ────────────────────────────────────────────────────────────
    async def _bitir_mesaj(self, chat_id, context, st, user):
        self.add_score(context, user.full_name, st["xal"])
        self.clear_active(context)

        umumi   = context.bot_data.get("scores", {}).get(user.full_name, 0)
        max_xal = TURLAR * XAL_IPUCUSUZ
        faiz    = (st["xal"] / max_xal * 100) if max_xal > 0 else 0

        if faiz == 100:   medal = "🏆 Mükəmməl! Siz bayraq ustasısınız!"
        elif faiz >= 80:  medal = "🥇 Əla nəticə!"
        elif faiz >= 60:  medal = "🥈 Yaxşı nəticə!"
        elif faiz >= 40:  medal = "🥉 Pis deyil!"
        else:             medal = "💪 Daha çox məşq edin!"

        text = (
            f"🏁 *Bayraq Oyunu Bitdi!*\n\n"
            f"👤 Oyunçu: *{user.first_name}*\n"
            f"⭐ Xal: *{st['xal']}* / {max_xal}\n"
            f"{medal}\n\n"
            f"🏆 Ümumi xal: *{umumi}*"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən Oyna",  callback_data="oyun_bayraq")],
            [InlineKeyboardButton("🔙 Oyun Menyusu",  callback_data="ana_menu")],
        ])
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="Markdown",
            reply_markup=kb,
        )
