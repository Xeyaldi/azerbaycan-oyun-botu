import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

LUGAT = {
    "alma","araba","adam","ağac","ağıl","alov","at","ay","bağ","bala",
    "balıq","bayraq","bilik","bulud","çay","çiçək","dad","dağ","dəmir",
    "dəniz","diş","duz","ev","əl","əsas","fil","gəmi","gün","günəş",
    "həyat","heyvan","hiss","hava","işıq","it","kənd","kitab","körpü",
    "küçə","lalə","limon","məktəb","meşə","musiqi","nağıl","neft",
    "od","paltar","pambıq","pişik","qaz","qala","qar","qapı","qazan",
    "qızıl","rəng","saat","sabun","səs","söz","su","süd","şam","şəhər",
    "taxıl","torpaq","top","ulduz","üzüm","vətən","yağış","yol","zəng",
    "daş","divar","ocaq","öküz","pəncərə","tikan","xalq","yuxu",
    "zəhmət","abi","acı","ağ","arı","göz","ilk","körpə","mavi","pəri",
    "rəvan","toz","xoş","zil","pul","qanad","çörək","alma","abır",
}
BASLANĞICLAR = ["alma","araba","ev","it","at","top","pul","qapı","dağ",
                "dəniz","çay","gün","ay","yol","ağac","bağ","qar","yağış"]


class SozZenciri(BaseGame):
    def __init__(self):
        super().__init__("soz_zenciri", "Söz Zənciri")

    def handles_callback(self, data, context, user_id):
        return data.startswith("soz_zenciri__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        bas = random.choice(BASLANĞICLAR)
        context.user_data["game_state"] = {
            "son_soz": bas, "istifade": [bas], "say": 0
        }
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("ℹ️ Qaydalar", callback_data="soz_zenciri__qaydalar")],
            [InlineKeyboardButton("⏹ Bitir",     callback_data="soz_zenciri__bitir")],
        ])
        await query.edit_message_text(
            f"🔗 *Söz Zənciri*\n\n"
            f"🟢 Başlanğıc söz: *{bas.upper()}*\n\n"
            f"Son hərf: *{bas[-1].upper()}*\n\n"
            f"*{bas[-1].upper()}* hərfi ilə başlayan söz yazın:",
            parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        if data == "soz_zenciri__qaydalar":
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri", callback_data="oyun_soz_zenciri")]])
            await query.edit_message_text(
                "🔗 *Söz Zənciri — Qaydalar*\n\n"
                "1️⃣ Hər söz əvvəlki sözün *son hərfi* ilə başlamalıdır\n"
                "2️⃣ Eyni söz iki dəfə istifadə edilə bilməz\n"
                "3️⃣ Hər düzgün söz üçün *+5 xal*\n\n"
                "Nə qədər çox söz — bir o qədər çox xal! 🏆",
                parse_mode="Markdown", reply_markup=kb)
        elif data == "soz_zenciri__bitir":
            st  = context.user_data.get("game_state", {})
            say = st.get("say", 0)
            user = query.from_user
            self.add_score(context, user.full_name, say * 5)
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_soz_zenciri")],
                [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
            ])
            await query.edit_message_text(
                f"⏹ *Oyun Bitdi!*\n\n🔗 {say} söz dediniz!\n"
                f"⭐ Qazanılan xal: *{say * 5}*\n\n"
                f"🏆 Ümumi: *{context.bot_data.get('scores',{}).get(user.full_name,0)}*",
                parse_mode="Markdown", reply_markup=kb)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st   = context.user_data.get("game_state", {})
        user = update.effective_user
        yeni = update.message.text.strip().lower()
        son  = st.get("son_soz", "")
        istifade = st.get("istifade", [])

        if not yeni.isalpha():
            await update.message.reply_text("❌ Yalnız hərf istifadə edin!"); return
        if yeni[0] != son[-1]:
            await update.message.reply_text(
                f"❌ Söz *{son[-1].upper()}* hərfi ilə başlamalıdır!",
                parse_mode="Markdown"); return
        if yeni in istifade:
            await update.message.reply_text(
                f"❌ *{yeni.upper()}* artıq istifadə edilib!",
                parse_mode="Markdown"); return
        if yeni not in LUGAT:
            await update.message.reply_text(
                f"❓ *{yeni.upper()}* lüğətdə tapılmadı. Başqa söz cəhd edin.",
                parse_mode="Markdown"); return

        self.add_score(context, user.full_name, 5)
        istifade.append(yeni)
        st.update({"son_soz": yeni, "istifade": istifade, "say": st.get("say", 0) + 1})
        context.user_data["game_state"] = st
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⏹ Bitir", callback_data="soz_zenciri__bitir")]])
        await update.message.reply_text(
            f"✅ *{yeni.upper()}* — Düzgün! ⭐ +5 xal\n\n"
            f"🔗 Zəncir: {st['say']} söz\n\n"
            f"*{yeni[-1].upper()}* hərfi ilə söz yazın:",
            parse_mode="Markdown", reply_markup=kb)
