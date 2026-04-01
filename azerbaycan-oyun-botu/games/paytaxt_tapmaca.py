import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

OLKELER = [
    {"olke": "Azərbaycan", "paytaxt": "Bakı", "variantlar": ["Bakı", "Gəncə", "Tbilisi", "Yerevan"]},
    {"olke": "Türkiyə", "paytaxt": "Ankara", "variantlar": ["Ankara", "İstanbul", "İzmir", "Bursa"]},
    {"olke": "Rusiya", "paytaxt": "Moskva", "variantlar": ["Moskva", "Sankt-Peterburq", "Novosibirsk", "Kazan"]},
    {"olke": "Almaniya", "paytaxt": "Berlin", "variantlar": ["Berlin", "Münhen", "Hamburq", "Köln"]},
    {"olke": "Fransa", "paytaxt": "Paris", "variantlar": ["Paris", "Lion", "Marsel", "Bordo"]},
    {"olke": "ABŞ", "paytaxt": "Vaşinqton", "variantlar": ["Vaşinqton", "Nyu-York", "Los-Anceles", "Çikaqo"]},
    {"olke": "Britaniya", "paytaxt": "London", "variantlar": ["London", "Mançester", "Birminqem", "Edinburq"]},
    {"olke": "Yaponiya", "paytaxt": "Tokio", "variantlar": ["Tokio", "Osaka", "Kioto", "Yokohama"]},
    {"olke": "Çin", "paytaxt": "Pekin", "variantlar": ["Pekin", "Şanxay", "Quanqçou", "Şenzen"]},
    {"olke": "Braziliya", "paytaxt": "Braziliya", "variantlar": ["Braziliya", "Rio-de-Janeyro", "San-Paulo", "Salvador"]},
    {"olke": "Hindistan", "paytaxt": "Nyu-Delhi", "variantlar": ["Nyu-Delhi", "Mumbay", "Kalkuta", "Çennay"]},
    {"olke": "Kanada", "paytaxt": "Ottava", "variantlar": ["Ottava", "Toronto", "Vankuver", "Montreal"]},
    {"olke": "Avstraliya", "paytaxt": "Kanberra", "variantlar": ["Kanberra", "Sidney", "Melburn", "Brizbern"]},
    {"olke": "Gürcüstan", "paytaxt": "Tbilisi", "variantlar": ["Tbilisi", "Batumi", "Kutaisi", "Rustavi"]},
    {"olke": "Ukrayna", "paytaxt": "Kiyev", "variantlar": ["Kiyev", "Xarkov", "Odessa", "Dnipro"]},
    {"olke": "Qazaxıstan", "paytaxt": "Astana", "variantlar": ["Astana", "Almatı", "Şımkent", "Karaganda"]},
    {"olke": "İtaliya", "paytaxt": "Roma", "variantlar": ["Roma", "Milan", "Napoli", "Florensiya"]},
    {"olke": "İspaniya", "paytaxt": "Madrid", "variantlar": ["Madrid", "Barselona", "Valensiya", "Sevilla"]},
    {"olke": "Polşa", "paytaxt": "Varşava", "variantlar": ["Varşava", "Krakov", "Vroslav", "Lodz"]},
    {"olke": "Niderland", "paytaxt": "Amsterdam", "variantlar": ["Amsterdam", "Rotterdam", "Haaqa", "Utreçt"]},
    {"olke": "Portuqaliya", "paytaxt": "Lissabon", "variantlar": ["Lissabon", "Porto", "Braga", "Koimbra"]},
    {"olke": "İsveç", "paytaxt": "Stokholm", "variantlar": ["Stokholm", "Qeteborg", "Malmö", "Uppsala"]},
    {"olke": "Norveç", "paytaxt": "Oslo", "variantlar": ["Oslo", "Bergen", "Trondheym", "Stavanger"]},
    {"olke": "Meksika", "paytaxt": "Mexiko", "variantlar": ["Mexiko", "Quadalaxara", "Monterrey", "Puebla"]},
    {"olke": "Argentina", "paytaxt": "Buenos-Aires", "variantlar": ["Buenos-Aires", "Kordoba", "Rosario", "Mendosa"]},
    {"olke": "Mısır", "paytaxt": "Qahirə", "variantlar": ["Qahirə", "İskəndəriyyə", "Giza", "Suez"]},
    {"olke": "Cənubi Afrika", "paytaxt": "Pretoriya", "variantlar": ["Pretoriya", "Keyp Town", "Johannesburq", "Durban"]},
    {"olke": "Pakistan", "paytaxt": "İslamabad", "variantlar": ["İslamabad", "Karaçi", "Lahor", "Peşəvər"]},
    {"olke": "Səudiyyə Ərəbistanı", "paytaxt": "Riyad", "variantlar": ["Riyad", "Ciddə", "Məkkə", "Dammam"]},
    {"olke": "İran", "paytaxt": "Tehran", "variantlar": ["Tehran", "Məşhəd", "İsfahan", "Şiraz"]},
]

class PaytaxtTapmaca(BaseGame):
    def __init__(self):
        super().__init__("paytaxt", "Paytaxt Tapmaca")

    def handles_callback(self, data: str, context, user_id: int) -> bool:
        return data.startswith("paytaxt_")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["active_game"] = self.game_key
        sual = random.choice(OLKELER)
        variantlar = sual["variantlar"][:]
        random.shuffle(variantlar)
        context.user_data["game_state"] = {
            "cavab": sual["paytaxt"],
            "olke": sual["olke"]
        }
        text = (
            "🏛 *Paytaxt Tapmaca*\n\n"
            f"🌍 *{sual['olke']}* ölkəsinin paytaxtı hansdır?\n\n"
            "Düzgün variantı seçin:"
        )
        keyboard = []
        row = []
        for i, v in enumerate(variantlar):
            row.append(InlineKeyboardButton(v, callback_data=f"paytaxt_cavab_{v}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")])
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        if not data.startswith("paytaxt_cavab_"):
            return

        state = context.user_data.get("game_state", {})
        user = query.from_user
        secim = data.replace("paytaxt_cavab_", "")
        dogru = state.get("cavab", "")
        olke = state.get("olke", "")

        keyboard = [
            [InlineKeyboardButton("🔄 Yenidən Oyna", callback_data="oyun_paytaxt")],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
        ]

        if secim == dogru:
            self.add_score(context, user.full_name, 10)
            result = f"✅ *Düzgün!*\n\n🌍 *{olke}* ölkəsinin paytaxtı *{dogru}*-dur!\n\n⭐ +10 xal!"
        else:
            result = f"❌ *Yanlış!*\n\n🌍 *{olke}* ölkəsinin paytaxtı *{dogru}*-dur!"

        context.user_data.pop("active_game", None)
        context.user_data.pop("game_state", None)
        await query.edit_message_text(
            result, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
