import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, CommandHandler
from games.base_game import BaseGame
from pymongo import MongoClient

# MongoDB Bağlantısı (Öz linkini bura qoymağı unutma)
MONGO_URL = "mongodb+srv://cabbarovxeyal32_db_user:Xeyal032aze@cluster0.f3gogmg.mongodb.net/?appName=Cluster0" 
client = MongoClient(MONGO_URL)
db = client['cro_bot_db']
words_col = db['words']
scores_col = db['scores']

OWNER_ID = 8371395083

# 150+ FƏRQLİ SÖZDƏN İBARƏT BAZA
CRO_SOZLER = [
    "Alma", "Armud", "Nar", "Banan", "Gilas", "Çiyələk", "Qarpız", "Yovşan", "Bənövşə", "Lalə",
    "Şir", "Pələng", "Ayı", "Dovşan", "Pişik", "İt", "At", "İnək", "Qoyun", "Keçi",
    "Bakı", "Gəncə", "Sumqayıt", "Şəki", "Lənkəran", "Quba", "Şuşa", "Ağdam", "Füzuli", "Kəlbəcər",
    "Məktəb", "Universitet", "Xəstəxana", "Polis", "Əsgər", "Həkim", "Müəllim", "Mühəndis", "Sürücü", "Aşpaz",
    "Futbol", "Şahmat", "Güləş", "Boks", "Tennis", "Voleybol", "Basketbol", "Üzgüçülük", "Qaçış", "Oxatma",
    "Dəniz", "Çay", "Göl", "Okean", "Şəlalə", "Dağ", "Meşə", "Səhra", "Ada", "Vadi",
    "Günəş", "Ay", "Ulduz", "Bulud", "Yağış", "Qar", "Külək", "Şimşək", "Göyqurşağı", "Duman",
    "Çörək", "Pendir", "Yumurta", "Balıq", "Ət", "Düyü", "Kartof", "Soğan", "Pomidor", "Xiyar",
    "Mavi", "Qırmızı", "Yaşıl", "Sarı", "Qara", "Ağ", "Bənövşəyi", "Narıncı", "Qəhvəyi", "Boz",
    "Körpü", "Bina", "Qapı", "Pəncərə", "Yol", "Park", "Muzey", "Teatr", "Kino", "Kitabxana",
    "Güzgü", "Daraq", "Sabun", "Dəsmal", "Yataq", "Masa", "Stul", "Şkaf", "Xalça", "Pərdə",
    "Qazan", "Tava", "Qaşıq", "Çəngəl", "Bıçaq", "Boşqab", "Fincan", "Çaydan", "Soba", "Soyuducu",
    "Lüğət", "Xəritə", "Bayraq", "Pul", "Cüzdan", "Çanta", "Çətir", "Açar", "Qıfıl", "Zəng",
    "Təbaşir", "Lövhə", "Dəftər", "Qələmdan", "Pozan", "Xətkeş", "Pərgar", "Boyaq", "Fırça", "Kağız",
    "Təyyarə", "Vertolyot", "Raket", "Kosmos", "Planet", "Teleskop", "Ulduz", "Kometa", "Kürə", "Xətt",
    "Gitar", "Tar", "Kamança", "Saz", "Piano", "Nafira", "Zurna", "Qaval", "Nağara", "Daf",
    "Zeytun", "Sarımsaq", "Bibər", "Badımcan", "Kabaçki", "Mərci", "Noxud", "Lobya", "Qarğıdalı", "Buğda",
    "Arı", "Kəpənək", "Milçək", "Ağcaqanad", "Hörümçək", "Qarışqa", "Böyrtkən", "Moruq", "Heyva", "Ərik",
    "Şalvar", "Köynək", "Paltar", "Ayaqqabı", "Papaq", "Əlcək", "Şərf", "Corab", "Kəmər", "Düymə",
    "Sabah", "Axşam", "Gecə", "Gündüz", "Həftə", "Ay", "İl", "Əsr", "Saat", "Dəqiqə"
]

class CroGame(BaseGame):
    def __init__(self):
        super().__init__("cro", "Cro (Krokodil)")
        # Bazada söz yoxdursa, yuxarıdakı 150+ sözü MongoDB-yə yükləyirik
        if words_col.count_documents({}) == 0:
            words_col.insert_many([{"word": w.lower()} for w in CRO_SOZLER])

    def handles_callback(self, data, context, user_id):
        return data.startswith("cro__")

    async def start_game(self, update_or_query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        
        all_words = list(words_col.find({}))
        chosen_word = random.choice(all_words)['word']

        context.user_data["game_state"] = {
            "soz": chosen_word,
            "aparici_id": None,
            "aparici_ad": None
        }
        
        text = (
            "🐊 *Cro (Krokodil) Başladı!* \n\n"
            "👇 Kim izah etmək istəyir? Butona basın."
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎤 Sözü İzah Et", callback_data="cro__aparici_ol")],
            [InlineKeyboardButton("🔴 Oyunu Bitir", callback_data="cro__bitir")]
        ])
        
        if isinstance(update_or_query, Update):
            await update_or_query.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await context.bot.send_message(
                chat_id=update_or_query.message.chat_id,
                text=text,
                parse_mode="Markdown",
                reply_markup=kb
            )

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st = context.user_data.get("game_state", {})
        user = query.from_user

        if data == "cro__aparici_ol":
            if st.get("aparici_id") is not None:
                if st["aparici_id"] == user.id:
                    await query.answer(f"Sənin sözün: {st['soz'].upper()}", show_alert=True)
                else:
                    await query.answer(f"Artıq aparıcı var: {st['aparici_ad']}", show_alert=True)
                return

            st["aparici_id"] = user.id
            st["aparici_ad"] = user.first_name
            await query.answer(f"Sənin sözün: {st['soz'].upper()}\n\nİzah etməyə başla!", show_alert=True)
            
            text = (
                f"🎤 *Aparıcı:* {user.mention_markdown()}\n"
                f"📢 Sözü izah edir... Tapın görək! \n\n"
                f"💡 Sözü unutmusansa, aşağıdakı butona bas."
            )
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("❓ Sözü Yenidən Gör", callback_data="cro__aparici_ol")],
                [InlineKeyboardButton("🚫 Aparıcılıqdan İmtina Et", callback_data="cro__imtina")],
                [InlineKeyboardButton("🔴 Oyunu Bitir", callback_data="cro__bitir")]
            ])
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

        elif data == "cro__imtina":
            if st.get("aparici_id") == user.id:
                await self.start_game(query, context)
            else:
                await query.answer("Sən aparıcı deyilsən!", show_alert=True)

        elif data == "cro__bitir":
            self.clear_active(context)
            await query.edit_message_text("🏁 *Oyun dayandırıldı.*")

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st = context.user_data.get("game_state", {})
        if not st or st.get("aparici_id") is None: return

        user = update.effective_user
        cavab = update.message.text.strip().lower()
        dogru_soz = st["soz"].lower()

        if user.id == st["aparici_id"]:
            if cavab == dogru_soz:
                await update.message.reply_text("🚫 Aparıcı cavabı özü yazmaz!")
            return

        if cavab == dogru_soz:
            scores_col.update_one(
                {"user_id": user.id},
                {"$inc": {"score": 10}, "$set": {"name": user.first_name}},
                upsert=True
            )
            
            await update.message.reply_text(
                f"🔥 Halaldır! *{user.first_name}* düzgün tapdı! \n"
                f"✅ Söz: *{dogru_soz.upper()}* \n"
                f"🏆 +10 xal qazandın!"
            , parse_mode="Markdown")
            await self.start_game(update, context)

    # --- OWNER & RANKING ---
    async def add_word(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != OWNER_ID: return
        
        words_input = " ".join(context.args).lower()
        if not words_input:
            await update.message.reply_text("İstifadə: `/sozelaveet soz1, soz2`")
            return
        
        new_words = [w.strip() for w in words_input.split(',')]
        added_count = 0
        for w in new_words:
            if not words_col.find_one({"word": w}):
                words_col.insert_one({"word": w})
                added_count += 1
        await update.message.reply_text(f"✅ {added_count} söz əlavə edildi. Toplam: {words_col.count_documents({})}")

    async def show_ranking(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        top_users = scores_col.find().sort("score", -1).limit(10)
        text = "🏆 *Cro Oyunu Top 10:* \n\n"
        for i, user in enumerate(top_users, 1):
            text += f"{i}. {user['name']} — *{user['score']} xal*\n"
        await update.message.reply_text(text, parse_mode="Markdown")
