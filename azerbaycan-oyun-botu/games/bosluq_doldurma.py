import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

CUMLELER = [
    {"cumle": "Azərbaycanın paytaxtı ___ şəhəridir.", "cavab": "Bakı", "variantlar": ["Bakı", "Gəncə", "Sumqayıt", "Lənkəran"]},
    {"cumle": "Günəş ___ istiqamətdən doğur.", "cavab": "Şərq", "variantlar": ["Şərq", "Qərb", "Şimal", "Cənub"]},
    {"cumle": "İnsan bədəninin ən böyük orqanı ___-dır.", "cavab": "Dəri", "variantlar": ["Dəri", "Qaraciyər", "Ürək", "Beyin"]},
    {"cumle": "Su ___ dərəcədə qaynayır.", "cavab": "100", "variantlar": ["100", "90", "80", "120"]},
    {"cumle": "Bir ildə ___ ay var.", "cavab": "12", "variantlar": ["12", "10", "11", "13"]},
    {"cumle": "Dünya günəşin ətrafında ___ ildə bir dövr edir.", "cavab": "1", "variantlar": ["1", "2", "365", "12"]},
    {"cumle": "Ən böyük okean ___ okeanıdır.", "cavab": "Sakit", "variantlar": ["Sakit", "Atlantik", "Hind", "Arktik"]},
    {"cumle": "Azərbaycan dili ___ qrupuna aiddir.", "cavab": "Türk", "variantlar": ["Türk", "Slavyan", "Ərəb", "Fars"]},
    {"cumle": "İnsan bədənində ___ sümük var.", "cavab": "206", "variantlar": ["206", "196", "186", "216"]},
    {"cumle": "Xəzər dənizi dünyanın ən böyük ___ gölüdür.", "cavab": "qapalı", "variantlar": ["qapalı", "açıq", "şirin", "dağ"]},
    {"cumle": "Hava ___ dərəcə olduqda su donur.", "cavab": "0", "variantlar": ["0", "-10", "4", "-5"]},
    {"cumle": "Azərbaycanda ___ rayonu var.", "cavab": "66", "variantlar": ["66", "60", "70", "75"]},
    {"cumle": "Işığın sürəti saniyədə ___ km-dir.", "cavab": "300.000", "variantlar": ["300.000", "150.000", "500.000", "100.000"]},
    {"cumle": "Yer kürəsinin ən hündür nöqtəsi ___ dağıdır.", "cavab": "Everest", "variantlar": ["Everest", "Elbrus", "Kazbek", "Qazbeq"]},
    {"cumle": "Bir həftədə ___ gün var.", "cavab": "7", "variantlar": ["7", "5", "6", "8"]},
]

class BosluqDoldurma(BaseGame):
    def __init__(self):
        super().__init__("bosluq", "Boşluq Doldurma")

    def handles_callback(self, data: str, context, user_id: int) -> bool:
        active = context.user_data.get("active_game")
        return active == self.game_key and data.startswith("bosluq_")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["active_game"] = self.game_key
        sual = random.choice(CUMLELER)
        variantlar = sual["variantlar"][:]
        random.shuffle(variantlar)
        context.user_data["game_state"] = {
            "cavab": sual["cavab"],
            "cumle": sual["cumle"]
        }
        text = (
            "📝 *Boşluq Doldurma*\n\n"
            f"🔤 {sual['cumle']}\n\n"
            "Düzgün variantı seçin:"
        )
        keyboard = []
        row = []
        for i, v in enumerate(variantlar):
            row.append(InlineKeyboardButton(v, callback_data=f"bosluq_cavab_{v}"))
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
        state = context.user_data.get("game_state", {})
        user = query.from_user

        if data.startswith("bosluq_cavab_"):
            secim = data.replace("bosluq_cavab_", "")
            dogru = state.get("cavab", "")
            cumle = state.get("cumle", "")
            keyboard = [
                [InlineKeyboardButton("🔄 Yenidən Oyna", callback_data="oyun_bosluq")],
                [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
            ]
            if secim == dogru:
                self.add_score(context, user.full_name, 10)
                result_text = (
                    f"✅ *Düzgün!*\n\n"
                    f"🔤 {cumle.replace('___', f'**{dogru}**')}\n\n"
                    f"⭐ +10 xal!"
                )
            else:
                result_text = (
                    f"❌ *Yanlış!*\n\n"
                    f"🔤 Düzgün cavab: *{dogru}*\n"
                    f"🔤 {cumle.replace('___', f'**{dogru}**')}"
                )
            context.user_data.pop("active_game", None)
            context.user_data.pop("game_state", None)
            await query.edit_message_text(
                result_text, parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
