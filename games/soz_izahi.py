import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from games.base_game import BaseGame
from pymongo import MongoClient

# MongoDB Bağlantısı
MONGO_URL = "mongodb+srv://cabbarovxeyal32_db_user:Xeyal032aze@cluster0.f3gogmg.mongodb.net/?appName=Cluster0" 
client = MongoClient(MONGO_URL)
db = client['cro_bot_db']
words_col = db['words']
scores_col = db['scores']

OWNER_ID = 8371395083

class SozIzahi(BaseGame):
    def __init__(self):
        super().__init__("cro", "HT-Cro") # Oyun adı HT-Cro olaraq dəyişdirildi
        self.init_db()

    def init_db(self):
        # Əgər baza boşdursa, ilkin sözləri kateqoriya ilə əlavə edirik
        if words_col.count_documents({}) == 0:
            initial_data = [
                {"word": "alma", "cat": "qarisiq"}, {"word": "şir", "cat": "qarisiq"},
                {"word": "şah ismayıl", "cat": "tarix"}, {"word": "atabəylər", "cat": "tarix"},
                {"word": "everest", "cat": "cografiya"}, {"word": "xəzər", "cat": "cografiya"},
                {"word": "vaqif", "cat": "insan"}, {"word": "leyla", "cat": "insan"}
            ]
            words_col.insert_many(initial_data)

    def handles_callback(self, data, context, user_id):
        return data.startswith("cro__")

    async def start_game(self, update_or_query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        
        # İlk addım: Mod seçimi (Şəkildəki kimi)
        text = "🎮 *HT-Cro* modunu seçin:"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌀 Qarışıq Sözlər", callback_data="cro__mod_qarisiq")],
            [InlineKeyboardButton("📜 Tarix", callback_data="cro__mod_tarix"), 
             InlineKeyboardButton("🌍 Coğrafiya", callback_data="cro__mod_cografiya")],
            [InlineKeyboardButton("👥 İnsan Adları", callback_data="cro__mod_insan")],
            [InlineKeyboardButton("🔴 Oyunu Bitir", callback_data="cro__bitir")]
        ])
        
        if isinstance(update_or_query, Update):
            await update_or_query.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await update_or_query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        st = context.user_data.get("game_state", {})
        user = query.from_user

        # MOD SEÇİMİ
        if data.startswith("cro__mod_"):
            mod = data.split("_")[-1]
            all_words = list(words_col.find({"cat": mod}))
            if not all_words:
                await query.answer("Bu kateqoriyada söz yoxdur!", show_alert=True)
                return
            
            chosen = random.choice(all_words)['word']
            context.user_data["game_state"] = {
                "soz": chosen,
                "mod": mod,
                "aparici_id": None,
                "aparici_ad": None
            }
            
            text = f"✅ *{mod.capitalize()}* modu seçildi!\n\n👇 Kim izah etmək istəyir? Butona basın."
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🎤 Sözü İzah Et", callback_data="cro__aparici_ol")],
                [InlineKeyboardButton("🔙 Modu Dəyiş", callback_data="cro__back_to_mods")],
                [InlineKeyboardButton("🔴 Oyunu Bitir", callback_data="cro__bitir")]
            ])
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

        elif data == "cro__back_to_mods":
            await self.start_game(query, context)

        elif data == "cro__aparici_ol":
            if st.get("aparici_id") is not None and st["aparici_id"] != user.id:
                await query.answer(f"Artıq aparıcı var: {st['aparici_ad']}", show_alert=True)
                return

            st["aparici_id"] = user.id
            st["aparici_ad"] = user.first_name
            
            # Sözə baxmaq üçün alert
            await query.answer(f"Sözün: {st['soz'].upper()}", show_alert=True)
            
            text = (
                f"👤 *Aparıcı:* {user.mention_markdown()}\n"
                f"📂 *Mod:* {st['mod'].capitalize()}\n"
                f"📢 Sözü izah edir... Tapın görək!"
            )
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔍 Sözə Baxmaq", callback_data="cro__soze_bax")],
                [InlineKeyboardButton("❌ Fikrimi Dəyişdim", callback_data="cro__imtina")],
                [InlineKeyboardButton("♻️ Növbəti Söz", callback_data="cro__novbeti")]
            ])
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

        elif data == "cro__soze_bax":
            if user.id == st.get("aparici_id"):
                await query.answer(f"Sənin sözün: {st['soz'].upper()}", show_alert=True)
            else:
                await query.answer("Sən aparıcı deyilsən!", show_alert=True)

        elif data == "cro__novbeti":
            if user.id == st.get("aparici_id"):
                mod = st['mod']
                new_word = random.choice(list(words_col.find({"cat": mod})))['word']
                st['soz'] = new_word
                await query.answer("Söz dəyişdirildi!", show_alert=True)
                await query.answer(f"Yeni sözün: {new_word.upper()}", show_alert=True)
            else:
                await query.answer("Yalnız aparıcı sözü dəyişə bilər!")

        elif data == "cro__imtina":
            if st.get("aparici_id") == user.id:
                await self.start_game(query, context)
            else:
                await query.answer("Sən aparıcı deyilsən!", show_alert=True)

        elif data == "cro__bitir":
            self.clear_active(context)
            await query.edit_message_text("🏁 *HT-Cro dayandırıldı.*")

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
                f"🥳 *{user.first_name}* düzgün tapdı! \n"
                f"✅ Söz: *{dogru_soz.upper()}* \n"
                f"🏆 +10 xal qazandın! Yeni raund başlayır..."
            , parse_mode="Markdown")
            
            # Yeni raund eyni modda başlasın
            mod = st['mod']
            new_word = random.choice(list(words_col.find({"cat": mod})))['word']
            st['soz'] = new_word
            st['aparici_id'] = None
            st['aparici_ad'] = None
            
            # Yenidən kim izah etsin mesajı
            await self.start_game(update, context)
