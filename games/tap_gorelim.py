import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

FAKTLAR = [
    ("Xəzər dənizi dünyanın ən böyük gölüdür.", True),
    ("Bakı Avropanın ən böyük şəhəridir.", False),
    ("Günəş bir ulduzdur.", True),
    ("İnsan bədənində 300-dən çox sümük var.", False),
    ("Azərbaycanda 66 rayon var.", True),
    ("Su H₂O formuluna malikdir.", True),
    ("Yer kürəsi Günəşin ən yaxın planetidir.", False),
    ("Azərbaycan 1991-ci ildə müstəqilliyini elan etdi.", True),
    ("Zürafə dünyanın ən ağır heyvanıdır.", False),
    ("Okeanlar Yer kürəsinin 71%-ini örtür.", True),
    ("Avstraliyanın paytaxtı Sidney şəhəridir.", False),
    ("Almazlar karbondan ibarətdir.", True),
    ("Bütün quşlar uça bilir.", False),
    ("Bakı Xəzər dənizinin sahilindədir.", True),
    ("Çin dünyanın ən kiçik ölkəsidir.", False),
    ("Balıqlar suda tənəffüs edir.", True),
    ("Şimşək çaxması zamanı işıq səsdən əvvəl görünür.", True),
    ("Ay Yer kürəsindən böyükdür.", False),
    ("DNA irsiyyət məlumatını daşıyır.", True),
    ("İnsan ömründə ortalama 100 il yaşayır.", False),
]

TURLAR = 10


class TapGorelim(BaseGame):
    def __init__(self):
        super().__init__("tap_gorelim", "Tap Görəlim")

    def handles_callback(self, data, context, user_id):
        return data.startswith("tap_gorelim__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        pool = random.sample(FAKTLAR, min(TURLAR, len(FAKTLAR)))
        context.user_data["game_state"] = {"pool": pool, "tur": 0, "xal": 0}
        await self._sual_goster(query, context, edit=True)

    async def _sual_goster(self, q, context, edit=False):
        st  = context.user_data["game_state"]
        idx = st["tur"]
        f   = st["pool"][idx]
        text = (
            f"❓ *Tap Görəlim — Doğru/Yanlış* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}\n\n"
            f"📌 {f[0]}\n\n"
            "Bu iddia doğrudurmu?"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Doğrudur",   callback_data="tap_gorelim__dogru"),
             InlineKeyboardButton("❌ Yanlışdır",  callback_data="tap_gorelim__yanlish")],
            [InlineKeyboardButton("🔴 Bitir",      callback_data="tap_gorelim__bitir")],
        ])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user

        if data == "tap_gorelim__bitir":
            await self._oyun_bitdi(query, context, st, user)
            return

        if data not in ("tap_gorelim__dogru", "tap_gorelim__yanlish"):
            return

        f     = st["pool"][st["tur"]]
        secim = (data == "tap_gorelim__dogru")
        if secim == f[1]:
            st["xal"] += 10
            await query.answer("✅ Düzgün! +10 xal")
        else:
            cavab_txt = "Doğrudur ✅" if f[1] else "Yanlışdır ❌"
            await query.answer(f"❌ Yanlış! Düzgün: {cavab_txt}")

        st["tur"] += 1
        if st["tur"] >= TURLAR:
            await self._oyun_bitdi(query, context, st, user)
        else:
            context.user_data["game_state"] = st
            await self._sual_goster(query, context, edit=True)

    async def _oyun_bitdi(self, q, context, st, user):
        self.add_score(context, user.full_name, st["xal"])
        self.clear_active(context)
        text = (f"🏁 *Tap Görəlim Bitdi!*\n\n👤 {user.first_name}\n"
                f"⭐ Xal: *{st['xal']}* / {TURLAR*10}\n\n"
                f"🏆 Ümumi: *{context.bot_data.get('scores',{}).get(user.full_name,0)}*")
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_tap_gorelim")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
