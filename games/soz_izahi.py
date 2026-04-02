import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from games.base_game import BaseGame

# BÜTÜN SÖZ BAZASI (KODUN İÇİNDƏ)
INITIAL_DATA = [
    # QARIŞIQ (40 ədəd)
    {"word": "alma", "cat": "qarisiq"}, {"word": "şir", "cat": "qarisiq"}, {"word": "masa", "cat": "qarisiq"}, {"word": "kitab", "cat": "qarisiq"}, {"word": "qələm", "cat": "qarisiq"},
    {"word": "telefon", "cat": "qarisiq"}, {"word": "pəncərə", "cat": "qarisiq"}, {"word": "qapı", "cat": "qarisiq"}, {"word": "eynək", "cat": "qarisiq"}, {"word": "saat", "cat": "qarisiq"},
    {"word": "dəftər", "cat": "qarisiq"}, {"word": "çanta", "cat": "qarisiq"}, {"word": "maşın", "cat": "qarisiq"}, {"word": "təyyarə", "cat": "qarisiq"}, {"word": "gəmi", "cat": "qarisiq"},
    {"word": "velosiped", "cat": "qarisiq"}, {"word": "günəş", "cat": "qarisiq"}, {"word": "bulud", "cat": "qarisiq"}, {"word": "yağış", "cat": "qarisiq"}, {"word": "qar", "cat": "qarisiq"},
    {"word": "küçə", "cat": "qarisiq"}, {"word": "park", "cat": "qarisiq"}, {"word": "məktəb", "cat": "qarisiq"}, {"word": "universitet", "cat": "qarisiq"}, {"word": "çörək", "cat": "qarisiq"},
    {"word": "su", "cat": "qarisiq"}, {"word": "çay", "cat": "qarisiq"}, {"word": "kofe", "cat": "qarisiq"}, {"word": "şəkər", "cat": "qarisiq"}, {"word": "duz", "cat": "qarisiq"},
    {"word": "yumurta", "cat": "qarisiq"}, {"word": "pendir", "cat": "qarisiq"}, {"word": "balıq", "cat": "qarisiq"}, {"word": "toyuq", "cat": "qarisiq"}, {"word": "kartof", "cat": "qarisiq"},
    {"word": "soğan", "cat": "qarisiq"}, {"word": "pomidor", "cat": "qarisiq"}, {"word": "xiyar", "cat": "qarisiq"}, {"word": "üzüm", "cat": "qarisiq"}, {"word": "heyva", "cat": "qarisiq"},

    # TARİX (40 ədəd)
    {"word": "şah ismayıl", "cat": "tarix"}, {"word": "atabəylər", "cat": "tarix"}, {"word": "babək", "cat": "tarix"}, {"word": "cavanşir", "cat": "tarix"}, {"word": "tomris", "cat": "tarix"},
    {"word": "nadir şah", "cat": "tarix"}, {"word": "uzun həsən", "cat": "tarix"}, {"word": "fətəli xan", "cat": "tarix"}, {"word": "məmməd əmin rəsulzadə", "cat": "tarix"}, {"word": "heydər əliyev", "cat": "tarix"},
    {"word": "nizami gəncəvi", "cat": "tarix"}, {"word": "nəsimi", "cat": "tarix"}, {"word": "füzuli", "cat": "tarix"}, {"word": "vaqif", "cat": "tarix"}, {"word": "axundov", "cat": "tarix"},
    {"word": "zərdabi", "cat": "tarix"}, {"word": "hacı zeynalabdin tağıyev", "cat": "tarix"}, {"word": "murtuza muxtarov", "cat": "tarix"}, {"word": "atropatena", "cat": "tarix"}, {"word": "albaniya", "cat": "tarix"},
    {"word": "manat", "cat": "tarix"}, {"word": "midiya", "cat": "tarix"}, {"word": "sümer", "cat": "tarix"}, {"word": "mısır", "cat": "tarix"}, {"word": "roma", "cat": "tarix"},
    {"word": "yunanıstan", "cat": "tarix"}, {"word": "piramida", "cat": "tarix"}, {"word": "firon", "cat": "tarix"}, {"word": "sezar", "cat": "tarix"}, {"word": "isgəndər", "cat": "tarix"},
    {"word": "atilla", "cat": "tarix"}, {"word": "çingiz xan", "cat": "tarix"}, {"word": "əmir teymur", "cat": "tarix"}, {"word": "ataturk", "cat": "tarix"}, {"word": "napoleon", "cat": "tarix"},
    {"word": "hitler", "cat": "tarix"}, {"word": "stalin", "cat": "tarix"}, {"word": "kolumb", "cat": "tarix"}, {"word": "nyuton", "cat": "tarix"}, {"word": "eynşteyn", "cat": "tarix"},

    # COĞRAFİYA (40 ədəd)
    {"word": "everest", "cat": "cografiya"}, {"word": "xəzər", "cat": "cografiya"}, {"word": "amazon", "cat": "cografiya"}, {"word": "nil", "cat": "cografiya"}, {"word": "kür", "cat": "cografiya"},
    {"word": "araz", "cat": "cografiya"}, {"word": "böyük səhra", "cat": "cografiya"}, {"word": "alplar", "cat": "cografiya"}, {"word": "qafqaz", "cat": "cografiya"}, {"word": "ural", "cat": "cografiya"},
    {"word": "himalay", "cat": "cografiya"}, {"word": "vulkan", "cat": "cografiya"}, {"word": "zəlzələ", "cat": "cografiya"}, {"word": "sunami", "cat": "cografiya"}, {"word": "ekvator", "cat": "cografiya"},
    {"word": "antarktida", "cat": "cografiya"}, {"word": "avstraliya", "cat": "cografiya"}, {"word": "avropa", "cat": "cografiya"}, {"word": "asya", "cat": "cografiya"}, {"word": "afrika", "cat": "cografiya"},
    {"word": "sakit okean", "cat": "cografiya"}, {"word": "qara dəniz", "cat": "cografiya"}, {"word": "aralıq dənizi", "cat": "cografiya"}, {"word": "göy göl", "cat": "cografiya"}, {"word": "şahdağ", "cat": "cografiya"},
    {"word": "bakı", "cat": "cografiya"}, {"word": "gence", "cat": "cografiya"}, {"word": "sumqayit", "cat": "cografiya"}, {"word": "naxçıvan", "cat": "cografiya"}, {"word": "şuşa", "cat": "cografiya"},
    {"word": "ankara", "cat": "cografiya"}, {"word": "istanbul", "cat": "cografiya"}, {"word": "moskva", "cat": "cografiya"}, {"word": "london", "cat": "cografiya"}, {"word": "parij", "cat": "cografiya"},
    {"word": "ada", "cat": "cografiya"}, {"word": "yarımada", "cat": "cografiya"}, {"word": "körfəz", "cat": "cografiya"}, {"word": "şəlalə", "cat": "cografiya"}, {"word": "iqlim", "cat": "cografiya"},

    # İNSAN ADLARI (40 ədəd)
    {"word": "vaqif", "cat": "insan"}, {"word": "leyla", "cat": "insan"}, {"word": "əli", "cat": "insan"}, {"word": "həsən", "cat": "insan"}, {"word": "hüseyn", "cat": "insan"},
    {"word": "məmməd", "cat": "insan"}, {"word": "əhməd", "cat": "insan"}, {"word": "fatima", "cat": "insan"}, {"word": "zəhra", "cat": "insan"}, {"word": "nərmin", "cat": "insan"},
    {"word": "aygün", "cat": "insan"}, {"word": "günel", "cat": "insan"}, {"word": "vüsal", "cat": "insan"}, {"word": "vüqar", "cat": "insan"}, {"word": "rəşad", "cat": "insan"},
    {"word": "elvin", "cat": "insan"}, {"word": "tural", "cat": "insan"}, {"word": "anar", "cat": "insan"}, {"word": "elnur", "cat": "insan"}, {"word": "samir", "cat": "insan"},
    {"word": "fərid", "cat": "insan"}, {"word": "nicat", "cat": "insan"}, {"word": "murad", "cat": "insan"}, {"word": "fuad", "cat": "insan"}, {"word": "ismayıl", "cat": "insan"},
    {"word": "ibrahim", "cat": "insan"}, {"word": "yusif", "cat": "insan"}, {"word": "məryəm", "cat": "insan"}, {"word": "ayşə", "cat": "insan"}, {"word": "xədicə", "cat": "insan"},
    {"word": "zeynəb", "cat": "insan"}, {"word": "sevinc", "cat": "insan"}, {"word": "könül", "cat": "insan"}, {"word": "lalə", "cat": "insan"}, {"word": "nərgiz", "cat": "insan"},
    {"word": "fidan", "cat": "insan"}, {"word": "aynur", "cat": "insan"}, {"word": "aysel", "cat": "insan"}, {"word": "arzu", "cat": "insan"}, {"word": "xəyal", "cat": "insan"}
]

class SozIzahi(BaseGame):
    def __init__(self):
        super().__init__("cro", "HT-Cro")
        self.temp_scores = {}

    def handles_callback(self, data, context, user_id):
        return data.startswith("cro__")

    async def start_game(self, update_or_query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        
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
        st = context.chat_data.get("game_state", {})
        user = query.from_user

        # MOD SEÇİMİ
        if data.startswith("cro__mod_"):
            mod = data.split("_")[-1]
            all_words = [i['word'] for i in INITIAL_DATA if i['cat'] == mod]
            if not all_words:
                await query.answer("Bu kateqoriyada söz yoxdur!", show_alert=True)
                return
            
            chosen = random.choice(all_words)
            context.chat_data["game_state"] = {
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
            await query.answer() # Buton donmasın deyə
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

        elif data == "cro__back_to_mods":
            await query.answer()
            await self.start_game(query, context)

        elif data == "cro__aparici_ol":
            if st.get("aparici_id") is not None and st["aparici_id"] != user.id:
                await query.answer(f"Artıq aparıcı var: {st['aparici_ad']}", show_alert=True)
                return

            st["aparici_id"] = user.id
            st["aparici_ad"] = user.first_name
            
            await query.answer(f"Sözün: {st['soz'].upper()}", show_alert=True)
            
            text = (
                f"👤 *Aparıcı:* {user.mention_markdown()}\n"
                f"📂 *Mod:* {st['mod'].capitalize()}\n"
                f"📢 Sözü izah edir... Tapın görək!"
            )
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔍 Sözə Baxmaq", callback_data="cro_soze_bax")],
                [InlineKeyboardButton("❌ Fikrimi Dəyişdim", callback_data="cro_imtina")],
                [InlineKeyboardButton("♻️ Növbəti Söz", callback_data="cro_novbeti")]
            ])
            await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)

        elif data == "cro__soze_bax":
            st = context.chat_data.get("game_state", {})
            aparici_id = st.get("aparici_id")
            
            if user.id == aparici_id:
                # Aparıcıya sözü popup olaraq göstəririk
                await query.answer(f"Sənin sözün: {st['soz'].upper()}", show_alert=True)
            else:
                # Başqası bassa xəbərdarlıq edirik
                await query.answer("⚠️ Sən aparıcı deyilsən! Sözü yalnız izah edən görə bilər.", show_alert=True)

        elif data == "cro__novbeti":
            st = context.chat_data.get("game_state", {})
            aparici_id = st.get("aparici_id")
            
            if user.id == aparici_id:
                mod = st.get('mod', 'qarisiq')
                all_words = [i['word'] for i in INITIAL_DATA if i['cat'] == mod]
                new_word = random.choice(all_words)
                
                # Yeni sözü yaddaşa yazırıq
                st['soz'] = new_word
                context.chat_data["game_state"] = st
                
                # Aparıcıya yeni sözü alert ilə göndəririk
                await query.answer(f"🔄 Söz dəyişdirildi!\nYeni sözün: {new_word.upper()}", show_alert=True)
            else:
                await query.answer("❌ Yalnız aparıcı sözü dəyişə bilər!", show_alert=True)
                     
        elif data == "cro__imtina":
            if st.get("aparici_id") == user.id:
                st["aparici_id"] = None
                st["aparici_ad"] = None
                await query.answer("Aparıcılıqdan imtina edildi")
                
                text = f"❌ {user.mention_markdown()} aparıcılıqdan imtina etdi.\n\n👇 Kim izah etmək istəyir? Butona basın."
                kb = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎤 Aparıcı Olmaq İstəyirəm", callback_data="cro__aparici_ol")],
                    [InlineKeyboardButton("🔙 Modu Dəyiş", callback_data="cro__back_to_mods")],
                    [InlineKeyboardButton("🔴 Oyunu Bitir", callback_data="cro__bitir")]
                ])
                await query.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
            else:
                await query.answer("Sən aparıcı deyilsən!", show_alert=True)

        elif data == "cro__bitir":
            await query.answer("Oyun bitirilir...")
            self.clear_active(context)
            await query.edit_message_text("**🏁 HT-Cro dayandırıldı.**")
            
    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        st = context.chat_data.get("game_state", {})
        if not st or st.get("aparici_id") is None: return

        user = update.effective_user
        cavab = update.message.text.strip().lower()
        dogru_soz = st["soz"].lower()

        if user.id == st["aparici_id"]:
            if cavab == dogru_soz:
                await update.message.reply_text("🚫 Aparıcı cavabı özü yazmaz!")
            return

        if cavab == dogru_soz:
            self.temp_scores[user.id] = self.temp_scores.get(user.id, 0) + 10
            
            await update.message.reply_text(
                f"🥳 *{user.first_name}* düzgün tapdı! \n"
                f"✅ Söz: *{dogru_soz.upper()}* \n"
                f"🏆 +10 xal qazandın! Yeni raund başlayır..."
            , parse_mode="Markdown")
            
            mod = st['mod']
            all_words = [i['word'] for i in INITIAL_DATA if i['cat'] == mod]
            st['soz'] = random.choice(all_words)
            st['aparici_id'] = None
            st['aparici_ad'] = None
            context.chat_data["game_state"] = st
            
            await self.start_game(update, context)
