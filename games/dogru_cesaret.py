import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

DOGRULAR = [
    "Ən utandığınız anınızı söyləyin.",
    "Son yalan nə vaxt söylediniz?",
    "Gizli bir hobiniz varmı?",
    "Ən böyük qorxunuz nədir?",
    "Ən pis qiymət aldığınız fənn nədir?",
    "Ən böyük xülyanız nədir?",
    "Bu qrupda ən çox kimə etibar edirsiniz?",
    "Həyatınızda ən böyük səhviniz nədir?",
    "İlk sevgilinizin adı nədir?",
    "Bu qrupda ən çox kimə oxşamaq istərdiniz?",
    "Ən axmaq nə iş etdiniz?",
    "Son 24 saatda nə yemişsiniz?",
    "Ən çox kimə paxıllıq edirsiniz?",
    "Heç uşaqkən bir şey oğurlamısınızmı?",
    "İndi necə hiss edirsiniz?",
]

CESARETLER = [
    "10 saniyə sol ayağınızın üstündə durun.",
    "Özünüzə 3 kompliment deyin.",
    "Azərbaycanca bir şeir yazın.",
    "Özünüzü 3 sözlə təsvir edin.",
    "5 ölkənin paytaxtını ardıcıl yazın.",
    "Bu qrupda birinin adını söyləyin.",
    "30 saniyəyə 10-dan geriyə sayın.",
    "Bir dəqiqəyə 5 Azərbaycan şəhərinin adını yazın.",
    "Ən sevdiyiniz film haqqında 2 cümlə yazın.",
    "Özünüz haqqında maraqlı bir fakt deyin.",
    "Ən sevdiyiniz mahnının adını yazın.",
    "Danışdığınız dilləri sıralayın.",
    "Bu gecə nə edəcəksiniz?",
    "Ən sevdiyiniz yemək adını hərflərə bölün.",
    "Gülünc bir emoji ilə özünüzü ifadə edin.",
]


class DogruCesaret(BaseGame):
    def __init__(self):
        super().__init__("dogru_cesaret", "Doğru/Cəsarət")

    def handles_callback(self, data, context, user_id):
        return data.startswith("dogru_cesaret__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔍 Doğru",   callback_data="dogru_cesaret__dogru"),
             InlineKeyboardButton("⚡ Cəsarət",  callback_data="dogru_cesaret__cesaret")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        await query.edit_message_text(
            "🎭 *Doğru/Cəsarət*\n\nSeçin — doğru söyləyəcəksiniz, yoxsa cəsarət göstərəcəksiniz?",
            parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_dogru_cesaret")],
            [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
        ])
        self.clear_active(context)
        if data == "dogru_cesaret__dogru":
            await query.edit_message_text(
                f"🔍 *Doğru:*\n\n{random.choice(DOGRULAR)}",
                parse_mode="Markdown", reply_markup=kb)
        elif data == "dogru_cesaret__cesaret":
            await query.edit_message_text(
                f"⚡ *Cəsarət:*\n\n{random.choice(CESARETLER)}",
                parse_mode="Markdown", reply_markup=kb)
