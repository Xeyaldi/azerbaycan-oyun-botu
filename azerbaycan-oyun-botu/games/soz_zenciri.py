import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

# Seed words to start the chain
BASLANĞIC_SOZLER = [
    "alma", "araba", "ev", "it", "at", "top", "pul",
    "qapı", "dağ", "dəniz", "çay", "gün", "ay", "yol",
    "ağac", "bağ", "qar", "yağış", "od", "su"
]

# Words that are valid (known dictionary - simplified for demo)
SOZLER_LUGETI = set([
    "alma","araba","adam","abır","axır","ağac","ağıl","alov",
    "at","ay","az","aç","bağ","bala","bax","bəd","bəy","bilik",
    "boyun","bulud","çay","çiçək","çox","dad","dağ","dəmir",
    "dəniz","diş","döş","duz","ev","əkin","əl","əsas","fil",
    "gəmi","gözəl","gün","günəş","həyat","heyvan","hiss",
    "hava","inci","işıq","it","iplik","kənd","kitab","körpü",
    "küçə","lalə","limon","məktəb","meşə","musiqi","nağıl",
    "neft","od","ov","paltar","pambıq","pişik","qaz","qala",
    "qar","qapı","qazan","qızıl","rəng","rüzgar","saat",
    "sabun","sarı","səs","söz","su","süd","şam","şəhər",
    "taxıl","torpaq","top","turac","uçuş","ulduz","üzüm",
    "vətən","yağış","yol","zəng","zövq","çiyin","balıq",
    "bayraq","bəzək","cücə","daş","dəri","divar","döyüş",
    "əhd","fikirli","quru","həsr","inad","iştirak","kəpənək",
    "kök","limon","meyvə","müəllim","nəfəs","ocaq","öküz",
    "pəncərə","qoşun","rəhbər","süngü","tikan","uzaq","var",
    "xalq","yuxu","zəhmət","abi","acı","adəm","ağ","arı",
    "bərabər","cins","çatı","dəqiq","dünya","elə","fəxr",
    "göz","hüquq","ilk","işarə","körpə","lalə","mavi",
    "nadir","olar","pəri","qırmızı","rəvan","sübut","toz",
    "ucuz","varlı","xoş","yadda","zil","pul","başlıq","qanad"
])

class SozZenciri(BaseGame):
    def __init__(self):
        super().__init__("soz_zenciri", "Söz Zənciri")

    def handles_callback(self, data: str, context, user_id: int) -> bool:
        active = context.user_data.get("active_game")
        return active == self.game_key and data.startswith("soz_zenciri_")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["active_game"] = self.game_key
        baslanğic = random.choice(BASLANĞIC_SOZLER)
        context.user_data["game_state"] = {
            "son_soz": baslanğic,
            "istifade_edilmis": [baslanğic],
            "sira": 0
        }
        text = (
            "🔗 *Söz Zənciri*\n\n"
            "📌 *Qayda:* Mən bir söz deyirəm, siz onun son hərfi ilə başlayan yeni söz deyin!\n\n"
            f"🟢 Başlanğıc söz: *{baslanğic.upper()}*\n\n"
            f"Son hərf: *{baslanğic[-1].upper()}*\n\n"
            f"Yazın: _{baslanğic[-1].upper()}_... ilə başlayan söz"
        )
        keyboard = [
            [InlineKeyboardButton("❓ Qaydaları göstər", callback_data="soz_zenciri_qaydalar")],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
        ]
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        if data == "soz_zenciri_qaydalar":
            keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="oyun_soz_zenciri")]]
            await query.edit_message_text(
                "🔗 *Söz Zənciri - Qaydalar*\n\n"
                "1️⃣ Hər söz əvvəlki sözün son hərfi ilə başlamalıdır\n"
                "2️⃣ Eyni söz iki dəfə istifadə edilə bilməz\n"
                "3️⃣ Söz Azərbaycan dilindən olmalıdır\n"
                "4️⃣ Hər düzgün söz üçün +5 xal!\n\n"
                "Nə qədər çox söz deyə bilsəniz, bir o qədər çox xal!",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        state = context.user_data.get("game_state", {})
        user = update.effective_user
        yeni_soz = update.message.text.strip().lower()
        son_soz = state.get("son_soz", "")
        istifade = state.get("istifade_edilmis", [])

        # Validate
        if not yeni_soz.isalpha():
            await update.message.reply_text("❌ Yalnız hərflərdən ibarət söz yazın!")
            return

        if yeni_soz[0] != son_soz[-1]:
            await update.message.reply_text(
                f"❌ Söz *{son_soz[-1].upper()}* hərfi ilə başlamalıdır!\n"
                f"Son hərf: *{son_soz[-1].upper()}*",
                parse_mode="Markdown"
            )
            return

        if yeni_soz in istifade:
            await update.message.reply_text(
                f"❌ *{yeni_soz.upper()}* artıq istifadə edilib! Başqa söz deyin.",
                parse_mode="Markdown"
            )
            return

        if yeni_soz not in SOZLER_LUGETI:
            await update.message.reply_text(
                f"❓ *{yeni_soz.upper()}* sözü məlumat bazasında tapılmadı. Başqa söz cəhd edin.",
                parse_mode="Markdown"
            )
            return

        # Valid word
        self.add_score(context, user.full_name, 5)
        istifade.append(yeni_soz)
        state["son_soz"] = yeni_soz
        state["istifade_edilmis"] = istifade
        state["sira"] = state.get("sira", 0) + 1
        context.user_data["game_state"] = state

        sira = state["sira"]
        keyboard = [[InlineKeyboardButton("⏹ Oyunu Bitir", callback_data="soz_zenciri_bitir")]]

        await update.message.reply_text(
            f"✅ *{yeni_soz.upper()}* — Düzgün!\n\n"
            f"⭐ +5 xal | 🔗 Zəncir: {sira} söz\n\n"
            f"İndi *{yeni_soz[-1].upper()}* hərfi ilə söz deyin:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        if data == "soz_zenciri_bitir":
            state = context.user_data.get("game_state", {})
            sira = state.get("sira", 0)
            context.user_data.pop("active_game", None)
            context.user_data.pop("game_state", None)
            keyboard = [
                [InlineKeyboardButton("🔄 Yenidən Oyna", callback_data="oyun_soz_zenciri")],
                [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
            ]
            await query.edit_message_text(
                f"⏹ *Oyun Bitdi!*\n\n"
                f"🔗 {sira} söz dediniz!\n"
                f"⭐ Qazandığınız xal: {sira * 5}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif data == "soz_zenciri_qaydalar":
            keyboard = [[InlineKeyboardButton("🔙 Geri", callback_data="oyun_soz_zenciri")]]
            await query.edit_message_text(
                "🔗 *Söz Zənciri - Qaydalar*\n\n"
                "1️⃣ Hər söz əvvəlki sözün son hərfi ilə başlamalıdır\n"
                "2️⃣ Eyni söz iki dəfə istifadə edilə bilməz\n"
                "3️⃣ Söz Azərbaycan dilindən olmalıdır\n"
                "4️⃣ Hər düzgün söz üçün +5 xal!",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
