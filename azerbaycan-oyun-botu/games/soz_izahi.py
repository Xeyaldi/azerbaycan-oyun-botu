import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

SOZLER = [
    {"soz": "Alma", "izah": "Qırmızı və ya yaşıl rəngdə olan meyvə", "ipucu": "Ağacda bitir"},
    {"soz": "Kitab", "izah": "Oxumaq üçün istifadə edilən, səhifələrdən ibarət olan əşya", "ipucu": "Kitabxanada olur"},
    {"soz": "Günəş", "izah": "Göydə parlayan, bizə istilik və işıq verən ulduz", "ipucu": "Hər gün doğur"},
    {"soz": "Su", "izah": "İçdiyimiz, şəffaf maye", "ipucu": "H2O"},
    {"soz": "Ev", "izah": "İnsanların yaşadığı bina", "ipucu": "Orada yatırıq"},
    {"soz": "At", "izah": "Minilən heyvan, dörd ayaqlı", "ipucu": "Çox sürətli qaçır"},
    {"soz": "Dəniz", "izah": "Böyük su kütləsi, sahilləri var", "ipucu": "Azərbaycanda Xəzər var"},
    {"soz": "Dağ", "izah": "Hündür torpaq və daş kütləsi, zirvəsi qar ilə örtülü olur", "ipucu": "Alpinistlər çıxır"},
    {"soz": "Uçurmaq", "izah": "Bir şeyi havaya qaldırmaq", "ipucu": "Quşlar edir"},
    {"soz": "Kompüter", "izah": "Elektron hesablama cihazı", "ipucu": "Ekranı var"},
    {"soz": "Telefon", "izah": "Danışmaq və mesaj göndərmək üçün cihaz", "ipucu": "Cibinizde"},
    {"soz": "Çörək", "izah": "Undan hazırlanan əsas qida məhsulu", "ipucu": "Sobada bişir"},
    {"soz": "Pişik", "izah": "Ev heyvanı, miyoldayır", "ipucu": "Siçan tutur"},
    {"soz": "İt", "izah": "İnsanın ən yaxın heyvan dostu", "ipucu": "Hürür"},
    {"soz": "Ağac", "izah": "Möhkəm gövdəsi olan bitki", "ipucu": "Meşədə olur"},
    {"soz": "Bulud", "izah": "Göydə ağ kütlə, yağış gətirir", "ipucu": "Göydə üzür"},
    {"soz": "Yağış", "izah": "Göydən düşən su damcıları", "ipucu": "Çətirlə gedirik"},
    {"soz": "Qar", "izah": "Qışda yağan ağ, yumşaq yağıntı", "ipucu": "Soyuqdur"},
    {"soz": "Müəllim", "izah": "Məktəbdə dərs keçən insan", "ipucu": "Taxtaya yazır"},
    {"soz": "Həkim", "izah": "Xəstələri müalicə edən mütəxəssis", "ipucu": "Xəstəxanada işləyir"},
    {"soz": "Aşpaz", "izah": "Yemək bişirən peşəkar insan", "ipucu": "Restoranda işləyir"},
    {"soz": "Pilot", "izah": "Təyyarə idarə edən şəxs", "ipucu": "Göydə işləyir"},
    {"soz": "Futbol", "izah": "Top ilə oynanan idman oyunu", "ipucu": "11 oyunçu"],
    {"soz": "Musiqi", "izah": "Notlardan ibarət sənət növü", "ipucu": "Qulaqla dinlənilir"},
    {"soz": "Rəng", "izah": "Qırmızı, mavi, sarı kimi görüntü xüsusiyyəti", "ipucu": "Gözdə görünür"},
]

class SozIzahi(BaseGame):
    def __init__(self):
        super().__init__("soz_izahi", "Söz İzahı")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["active_game"] = self.game_key
        soz_data = random.choice(SOZLER)
        context.user_data["game_state"] = {
            "soz": soz_data["soz"],
            "izah": soz_data["izah"],
            "ipucu": soz_data["ipucu"],
            "canlar": 3,
            "ipucu_istendi": False
        }
        text = (
            "🎯 *Söz İzahı Oyunu*\n\n"
            f"📖 *İzah:* {soz_data['izah']}\n\n"
            f"💡 Cavabı yazın! ({'_' * len(soz_data['soz'])})\n"
            f"❤️ Canlar: 3"
        )
        keyboard = [
            [InlineKeyboardButton("💡 İpucu Al (-1 can)", callback_data="soz_izahi_ipucu")],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
        ]
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        state = context.user_data.get("game_state", {})

        if data == "soz_izahi_ipucu":
            if state.get("canlar", 0) <= 1:
                await query.answer("❌ Kifayət qədər canınız yoxdur!", show_alert=True)
                return
            state["canlar"] -= 1
            state["ipucu_istendi"] = True
            context.user_data["game_state"] = state
            text = (
                "🎯 *Söz İzahı Oyunu*\n\n"
                f"📖 *İzah:* {state['izah']}\n"
                f"💡 *İpucu:* {state['ipucu']}\n\n"
                f"❤️ Canlar: {state['canlar']}"
            )
            keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]]
            await query.edit_message_text(
                text, parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        elif data == "soz_izahi_yeniden":
            await self.start_game(query, context)

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        state = context.user_data.get("game_state", {})
        user_answer = update.message.text.strip()
        correct = state.get("soz", "")
        user = update.effective_user

        if user_answer.lower() == correct.lower():
            xal = state.get("canlar", 1) * 10
            self.add_score(context, user.full_name, xal)
            context.user_data.pop("active_game", None)
            context.user_data.pop("game_state", None)
            keyboard = [
                [InlineKeyboardButton("🔄 Yenidən Oyna", callback_data="oyun_soz_izahi")],
                [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
            ]
            await update.message.reply_text(
                f"✅ *Düzgün cavab!* Söz: *{correct}*\n\n"
                f"⭐ +{xal} xal qazandınız!\n"
                f"🏆 Ümumi xal: {context.bot_data.get('scores', {}).get(user.full_name, 0)}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            state["canlar"] -= 1
            context.user_data["game_state"] = state
            if state["canlar"] <= 0:
                context.user_data.pop("active_game", None)
                context.user_data.pop("game_state", None)
                keyboard = [
                    [InlineKeyboardButton("🔄 Yenidən Oyna", callback_data="oyun_soz_izahi")],
                    [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
                ]
                await update.message.reply_text(
                    f"❌ *Canlarınız bitti!*\nDüzgün cavab: *{correct}*",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            else:
                await update.message.reply_text(
                    f"❌ Yanlış! ❤️ {state['canlar']} can qaldı. Yenidən cəhd edin:"
                )
