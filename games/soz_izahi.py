import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

SOZLER = [
    {"soz": "Alma",      "izah": "Qırmızı və ya yaşıl rəngdə ağacda bitən meyvə",          "ipucu": "A"},
    {"soz": "Kitab",     "izah": "Oxumaq üçün olan, səhifələrdən ibarət əşya",              "ipucu": "K"},
    {"soz": "Günəş",     "izah": "Göydə parlayan, istilik və işıq verən nəhəng ulduz",      "ipucu": "G"},
    {"soz": "Bulud",     "izah": "Göydə üzən, yağış gətirən ağ və ya boz kütlə",           "ipucu": "B"},
    {"soz": "Dəniz",     "izah": "Böyük duzlu su kütləsi, sahilləri var",                   "ipucu": "D"},
    {"soz": "Dağ",       "izah": "Hündür torpaq və daş kütləsi, zirvəsi olur",              "ipucu": "D"},
    {"soz": "Kompüter",  "izah": "Elektron hesablama və məlumat işləmə cihazı",             "ipucu": "K"},
    {"soz": "Telefon",   "izah": "Danışmaq və mesaj göndərmək üçün kiçik cihaz",            "ipucu": "T"},
    {"soz": "Çörək",     "izah": "Undan hazırlanan, sobada bişən əsas qida",                "ipucu": "Ç"},
    {"soz": "Pişik",     "izah": "Miyoldayan, siçan tutan ev heyvanı",                      "ipucu": "P"},
    {"soz": "Ağac",      "izah": "Gövdəsi möhkəm olan, meşədə böyüyən bitki",              "ipucu": "A"},
    {"soz": "Müəllim",   "izah": "Məktəbdə dərs keçən, bilik öyrədən insan",               "ipucu": "M"},
    {"soz": "Həkim",     "izah": "Xəstələri müayinə edib müalicə edən mütəxəssis",         "ipucu": "H"},
    {"soz": "Bayraq",    "izah": "Ölkəni təmsil edən rəngli parça, dirəyə qaldırılır",      "ipucu": "B"},
    {"soz": "Torpaq",    "izah": "Bitkilərin böyüdüyü, ayağımızın altındakı qat",           "ipucu": "T"},
    {"soz": "Körpü",     "izah": "Çay və ya dərə üzərindən keçmək üçün tikili",             "ipucu": "K"},
    {"soz": "Saat",      "izah": "Vaxtı göstərən cihaz, əl biləyinə taxılır",              "ipucu": "S"},
    {"soz": "Uçuş",      "izah": "Havada hərəkət etmə, quşların etdiyi iş",                "ipucu": "U"},
    {"soz": "Xəzinə",    "izah": "Gizlədilmiş qiymətli əşyalar toplusu",                   "ipucu": "X"},
    {"soz": "Zəng",      "izah": "Səs çıxaran metal əşya, məktəbdə dərs başlayanda çalınır","ipucu": "Z"},
    {"soz": "Neft",      "izah": "Yer altından çıxan, yanacaq kimi istifadə edilən maddə", "ipucu": "N"},
    {"soz": "Şəlalə",    "izah": "Yüksəkdən aşağı düşən güclü su axını",                   "ipucu": "Ş"},
    {"soz": "Kənd",      "izah": "Şəhərdən kiçik, insanların yaşadığı yaşayış məntəqəsi",  "ipucu": "K"},
    {"soz": "Üzüm",      "izah": "Salxımlarla bitən, şərabda istifadə edilən meyvə",        "ipucu": "Ü"},
    {"soz": "Çiçək",     "izah": "Gözəl görünüşü və ətri olan bitkinin hissəsi",            "ipucu": "Ç"},
]

TURLAR = 10
PAS_HAKKI = 2


def dashes(word):
    return " _ " * len(word)


class SozIzahi(BaseGame):
    def __init__(self):
        super().__init__("soz_izahi", "Söz İzahı")

    def handles_callback(self, data, context, user_id):
        return data.startswith("soz_izahi__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        pool = random.sample(SOZLER, min(TURLAR, len(SOZLER)))
        context.user_data["game_state"] = {
            "pool": pool, "tur": 0, "xal": 0,
            "pas": PAS_HAKKI, "ipucu_gosterildi": False,
        }
        await self._sual_goster(query, context, edit=True)

    async def _sual_goster(self, q, context, edit=False):
        st   = context.user_data["game_state"]
        idx  = st["tur"]
        s    = st["pool"][idx]
        ipucu_hint = f"İlk hərf: *{s['ipucu']}*" if st["ipucu_gosterildi"] else dashes(s["soz"])
        text = (
            f"🎯 *Söz İzahı* | Tur {idx+1}/{TURLAR}\n"
            f"💰 Xal: {st['xal']}  •  ⏭ Pas: {st['pas']}\n\n"
            f"📖 *İzah:* {s['izah']}\n\n"
            f"🔤 {ipucu_hint}\n\n"
            "✍️ Cavabı yazın:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("💡 İpucu",    callback_data="soz_izahi__ipucu"),
             InlineKeyboardButton("⏭ Pas",       callback_data="soz_izahi__pas")],
            [InlineKeyboardButton("🔴 Bitir",    callback_data="soz_izahi__bitir")],
        ])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st   = context.user_data.get("game_state", {})
        user = query.from_user

        if data == "soz_izahi__ipucu":
            if st.get("ipucu_gosterildi"):
                await query.answer("İpucu artıq göstərilib!", show_alert=False)
                return
            st["ipucu_gosterildi"] = True
            context.user_data["game_state"] = st
            await self._sual_goster(query, context, edit=True)

        elif data == "soz_izahi__pas":
            if st.get("pas", 0) <= 0:
                await query.answer("Pas hakkınız qalmayıb!", show_alert=True)
                return
            st["pas"] -= 1
            dogru = st["pool"][st["tur"]]["soz"]
            st["tur"] += 1
            st["ipucu_gosterildi"] = False
            if st["tur"] >= TURLAR:
                await self._oyun_bitdi(query, context, st, user)
            else:
                context.user_data["game_state"] = st
                await query.answer(f"Pas! Cavab: {dogru}")
                await self._sual_goster(query, context, edit=True)

        elif data == "soz_izahi__bitir":
            await self._oyun_bitdi(query, context, st, user)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st   = context.user_data.get("game_state", {})
        user = update.effective_user
        cavab = update.message.text.strip()
        dogru = st["pool"][st["tur"]]["soz"]

        if cavab.lower() == dogru.lower():
            st["xal"] += 10
            await update.message.reply_text(f"✅ *Düzgün!* +10 xal 🎉", parse_mode="Markdown")
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
            f"🏁 *Söz İzahı Bitdi!*\n\n"
            f"👤 {user.first_name}\n"
            f"⭐ Xal: *{st['xal']}* / {TURLAR*10}\n\n"
            f"🏆 Ümumi xal: *{context.bot_data.get('scores',{}).get(user.full_name,0)}*"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_soz_izahi")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        if q:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        elif msg:
            await msg.reply_text(text, parse_mode="Markdown", reply_markup=kb)
