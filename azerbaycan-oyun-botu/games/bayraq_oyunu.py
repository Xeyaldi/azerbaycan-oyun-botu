import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

BAYRAQLАР = [
    {"emoji": "🇦🇿", "olke": "Azərbaycan", "variantlar": ["Azərbaycan", "Türkiyə", "Qazaxıstan", "Özbəkistan"]},
    {"emoji": "🇹🇷", "olke": "Türkiyə", "variantlar": ["Türkiyə", "Azərbaycan", "İran", "Yunanıstan"]},
    {"emoji": "🇷🇺", "olke": "Rusiya", "variantlar": ["Rusiya", "Polşa", "Niderland", "Fransa"]},
    {"emoji": "🇩🇪", "olke": "Almaniya", "variantlar": ["Almaniya", "Belçika", "Avstriya", "İsveçrə"]},
    {"emoji": "🇫🇷", "olke": "Fransa", "variantlar": ["Fransa", "İtaliya", "İspaniya", "Portuqaliya"]},
    {"emoji": "🇺🇸", "olke": "ABŞ", "variantlar": ["ABŞ", "Britaniya", "Avstraliya", "Kanada"]},
    {"emoji": "🇬🇧", "olke": "Britaniya", "variantlar": ["Britaniya", "ABŞ", "İrlandiya", "Yeni Zelandiya"]},
    {"emoji": "🇯🇵", "olke": "Yaponiya", "variantlar": ["Yaponiya", "Çin", "Koreya", "Vyetnam"]},
    {"emoji": "🇨🇳", "olke": "Çin", "variantlar": ["Çin", "Yaponiya", "Koreya", "Tayvan"]},
    {"emoji": "🇮🇹", "olke": "İtaliya", "variantlar": ["İtaliya", "Fransa", "İspaniya", "Rumıniya"]},
    {"emoji": "🇧🇷", "olke": "Braziliya", "variantlar": ["Braziliya", "Argentina", "Meksika", "Kolombia"]},
    {"emoji": "🇮🇳", "olke": "Hindistan", "variantlar": ["Hindistan", "Banqladeş", "Pakistan", "Nepal"]},
    {"emoji": "🇸🇦", "olke": "Səudiyyə Ərəbistanı", "variantlar": ["Səudiyyə Ərəbistanı", "İraq", "İran", "İordaniya"]},
    {"emoji": "🇰🇿", "olke": "Qazaxıstan", "variantlar": ["Qazaxıstan", "Azərbaycan", "Özbəkistan", "Qırğızıstan"]},
    {"emoji": "🇬🇪", "olke": "Gürcüstan", "variantlar": ["Gürcüstan", "Ermənistan", "Ukrayna", "Belarus"]},
    {"emoji": "🇦🇲", "olke": "Ermənistan", "variantlar": ["Ermənistan", "Gürcüstan", "Suriya", "Livan"]},
    {"emoji": "🇺🇦", "olke": "Ukrayna", "variantlar": ["Ukrayna", "Rusiya", "Belarus", "Moldova"]},
    {"emoji": "🇪🇸", "olke": "İspaniya", "variantlar": ["İspaniya", "Portuqaliya", "Meksika", "Argentina"]},
    {"emoji": "🇵🇰", "olke": "Pakistan", "variantlar": ["Pakistan", "Hindistan", "Banqladeş", "Əfqanıstan"]},
    {"emoji": "🇳🇱", "olke": "Niderland", "variantlar": ["Niderland", "Almaniya", "Belçika", "Danimarka"]},
]

class BayraqOyunu(BaseGame):
    def __init__(self):
        super().__init__("bayraq", "Bayraq Oyunu")

    def handles_callback(self, data: str, context, user_id: int) -> bool:
        return data.startswith("bayraq_")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["active_game"] = self.game_key
        sual = random.choice(BAYRAQLАР)
        variantlar = sual["variantlar"][:]
        random.shuffle(variantlar)
        context.user_data["game_state"] = {
            "cavab": sual["olke"],
            "emoji": sual["emoji"]
        }
        text = (
            "🚩 *Bayraq Oyunu*\n\n"
            f"Bu bayraq hansı ölkəyə aiddir?\n\n"
            f"{sual['emoji']}\n\n"
            "Düzgün variantı seçin:"
        )
        keyboard = []
        for v in variantlar:
            keyboard.append([InlineKeyboardButton(v, callback_data=f"bayraq_cavab_{v}")])
        keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")])
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        if not data.startswith("bayraq_cavab_"):
            return

        state = context.user_data.get("game_state", {})
        user = query.from_user
        secim = data.replace("bayraq_cavab_", "")
        dogru = state.get("cavab", "")
        emoji = state.get("emoji", "🏳")

        keyboard = [
            [InlineKeyboardButton("🔄 Yenidən Oyna", callback_data="oyun_bayraq")],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
        ]

        if secim == dogru:
            self.add_score(context, user.full_name, 10)
            result = f"✅ *Düzgün!* {emoji} = *{dogru}*\n\n⭐ +10 xal!"
        else:
            result = f"❌ *Yanlış!*\n\n{emoji} = *{dogru}*"

        context.user_data.pop("active_game", None)
        context.user_data.pop("game_state", None)
        await query.edit_message_text(
            result, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
