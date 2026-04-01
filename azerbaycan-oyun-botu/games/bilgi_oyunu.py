import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

SUALLAR = [
    {"sual": "Azərbaycanın milli rəmzi hansıdır?", "cavab": "Üç rəngli bayraq", "variantlar": ["Üç rəngli bayraq", "Qartal", "Nar", "At"]},
    {"sual": "Bakı şəhəri hansı dənizin sahilindədir?", "cavab": "Xəzər", "variantlar": ["Xəzər", "Qara", "Aral", "Aralıq"]},
    {"sual": "Azərbaycanın müstəqillik günü nə vaxtdır?", "cavab": "18 Oktyabr", "variantlar": ["18 Oktyabr", "28 May", "15 Sentyabr", "1 Yanvar"]},
    {"sual": "Heydar Əliyev kimdir?", "cavab": "Azərbaycanın ulu öndəri", "variantlar": ["Azərbaycanın ulu öndəri", "Türkiyə prezidenti", "Rus rəhbəri", "Gürcüstan prezidenti"]},
    {"sual": "Dünyada ən çox danışılan dil hansıdır?", "cavab": "Mandarin (Çin)", "variantlar": ["Mandarin (Çin)", "İngilis", "İspan", "Ərəb"]},
    {"sual": "Yer kürəsinin ən dərin nöqtəsi haradadır?", "cavab": "Mariana çuxuru", "variantlar": ["Mariana çuxuru", "Atlantik okean", "Sakit okean", "Hind okeanı"]},
    {"sual": "Kompüterin beyin hissəsi nə adlanır?", "cavab": "Prosessor (CPU)", "variantlar": ["Prosessor (CPU)", "Monitor", "RAM", "Klaviatura"]},
    {"sual": "Fotosintez prosesi nədir?", "cavab": "Bitkilərin işıqdan qida alması", "variantlar": ["Bitkilərin işıqdan qida alması", "Heyvanların nəfəs alması", "Suyun buxarlanması", "Torpağın islanması"]},
    {"sual": "Ən böyük planet hansıdır?", "cavab": "Yupiter", "variantlar": ["Yupiter", "Saturn", "Uran", "Neptun"]},
    {"sual": "DNA-nın tam açılışı nədir?", "cavab": "Deoksiribonuklein turşusu", "variantlar": ["Deoksiribonuklein turşusu", "Dəmir turşusu", "Dihidrogen turşusu", "Azot turşusu"]},
    {"sual": "Azərbaycanın ən uzun çayı hansıdır?", "cavab": "Kür", "variantlar": ["Kür", "Araz", "Samur", "Alazan"]},
    {"sual": "İlk kompüter nə vaxt icad edilib?", "cavab": "1940-cı illər", "variantlar": ["1940-cı illər", "1920-ci illər", "1960-cı illər", "1800-cü illər"]},
    {"sual": "Günəş sistemindəki planetlərin sayı neçədir?", "cavab": "8", "variantlar": ["8", "9", "7", "10"]},
    {"sual": "Azərbaycanda hansı dil rəsmi dil sayılır?", "cavab": "Azərbaycan dili", "variantlar": ["Azərbaycan dili", "Rus dili", "Türk dili", "İngilis dili"]},
    {"sual": "İnsanın normal bədən temperaturu neçə dərəcədir?", "cavab": "36.6", "variantlar": ["36.6", "37.5", "35.0", "38.0"]},
    {"sual": "Ən kiçik planet hansıdır?", "cavab": "Merkuri", "variantlar": ["Merkuri", "Mars", "Venera", "Yer"]},
    {"sual": "Azərbaycan neçənci ildə müstəqilliyini elan etdi?", "cavab": "1991", "variantlar": ["1991", "1990", "1992", "1989"]},
    {"sual": "Mis elementi hansı simvolla göstərilir?", "cavab": "Cu", "variantlar": ["Cu", "Mi", "Mg", "Co"]},
    {"sual": "Bakı metrosunun ilk xətti nə vaxt açılıb?", "cavab": "1967", "variantlar": ["1967", "1970", "1960", "1975"]},
    {"sual": "Hansı heyvan dünyanın ən sürətli quşudur?", "cavab": "Şahin", "variantlar": ["Şahin", "Qartal", "Turac", "Qaz"]},
]

class BilgiOyunu(BaseGame):
    def __init__(self):
        super().__init__("bilgi", "Bilik Oyunu")

    def handles_callback(self, data: str, context, user_id: int) -> bool:
        active = context.user_data.get("active_game")
        return active == self.game_key and data.startswith("bilgi_")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["active_game"] = self.game_key
        asked = context.user_data.get("bilgi_asked", [])
        remaining = [s for s in SUALLAR if s["sual"] not in asked]
        if not remaining:
            context.user_data["bilgi_asked"] = []
            remaining = SUALLAR[:]

        sual = random.choice(remaining)
        asked.append(sual["sual"])
        context.user_data["bilgi_asked"] = asked

        variantlar = sual["variantlar"][:]
        random.shuffle(variantlar)
        context.user_data["game_state"] = {
            "cavab": sual["cavab"],
            "sual": sual["sual"],
            "seriya": context.user_data.get("bilgi_seriya", 0)
        }

        seriya = context.user_data.get("bilgi_seriya", 0)
        text = (
            "🧠 *Bilik Oyunu*\n\n"
            f"❓ {sual['sual']}\n\n"
            f"🔥 Seriya: {seriya}"
        )
        keyboard = []
        for v in variantlar:
            keyboard.append([InlineKeyboardButton(v, callback_data=f"bilgi_cavab_{v}")])
        keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")])
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        if not data.startswith("bilgi_cavab_"):
            return

        state = context.user_data.get("game_state", {})
        user = query.from_user
        secim = data.replace("bilgi_cavab_", "")
        dogru = state.get("cavab", "")

        if secim == dogru:
            seriya = context.user_data.get("bilgi_seriya", 0) + 1
            context.user_data["bilgi_seriya"] = seriya
            xal = 10 + (seriya - 1) * 5
            self.add_score(context, user.full_name, xal)
            result = (
                f"✅ *Düzgün!*\n\n"
                f"⭐ +{xal} xal!\n"
                f"🔥 Seriya: {seriya}\n\n"
                "Növbəti sual üçün davam edin:"
            )
            keyboard = [
                [InlineKeyboardButton("➡️ Növbəti Sual", callback_data="oyun_bilgi")],
                [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
            ]
        else:
            context.user_data["bilgi_seriya"] = 0
            result = (
                f"❌ *Yanlış!*\n\n"
                f"✅ Düzgün cavab: *{dogru}*\n"
                f"🔥 Seriya sıfırlandı!"
            )
            keyboard = [
                [InlineKeyboardButton("🔄 Yenidən Oyna", callback_data="oyun_bilgi")],
                [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
            ]

        context.user_data.pop("active_game", None)
        context.user_data.pop("game_state", None)
        await query.edit_message_text(
            result, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
