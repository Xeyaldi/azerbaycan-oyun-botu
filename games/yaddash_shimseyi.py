import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

POOL = ["🍎","🍌","🍇","🍓","🍊","🍋","🍉","🍑","🥝","🍒","🥭","🍍"]


class YaddasShimseyi(BaseGame):
    def __init__(self):
        super().__init__("yaddash", "Yaddaş Şimşəyi")

    def handles_callback(self, data, context, user_id):
        return data.startswith("yaddash__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        self.set_active(context)
        await self._next(query, context, level=1, xal=0, edit=True)

    async def _next(self, q, context, level, xal, edit=False):
        n   = level + 2
        seq = [random.choice(POOL) for _ in range(n)]
        context.user_data["game_state"] = {"seq": seq, "level": level, "xal": xal}
        text = (
            f"⚡ *Yaddaş Şimşəyi* — Səviyyə {level}\n\n"
            f"⭐ Xal: {xal}\n\n"
            f"Yadda saxlayın ({n} emoji):\n\n"
            f"{' '.join(seq)}\n\n"
            "Hazır olduqda 'Başla' düyməsinə basın:"
        )
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Başla", callback_data=f"yaddash__basla_{level}_{xal}")],
            [InlineKeyboardButton("🔴 Bitir", callback_data="yaddash__bitir")],
        ])
        if edit:
            await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)
        else:
            await q.message.reply_text(text, parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data  = query.data
        st    = context.user_data.get("game_state", {})
        user  = query.from_user

        if data == "yaddash__bitir":
            xal = st.get("xal", 0)
            self.add_score(context, user.full_name, xal)
            self.clear_active(context)
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_yaddash")],
                [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
            ])
            await query.edit_message_text(
                f"⏹ *Oyun Bitdi!*\n\n⭐ Ümumi xal: *{xal}*",
                parse_mode="Markdown", reply_markup=kb)
            return

        if data.startswith("yaddash__basla_"):
            parts = data.split("_")
            level, xal = int(parts[-2]), int(parts[-1])
            seq   = st.get("seq", [])
            first = seq[0] if seq else "🍎"
            opts  = {first}
            while len(opts) < 4:
                opts.add(random.choice(POOL))
            opts = list(opts); random.shuffle(opts)
            kb = []
            row = []
            for o in opts:
                row.append(InlineKeyboardButton(o, callback_data=f"yaddash__c_{o}_{level}_{xal}"))
                if len(row) == 2:
                    kb.append(row); row = []
            if row: kb.append(row)
            kb.append([InlineKeyboardButton("🔴 Bitir", callback_data="yaddash__bitir")])
            await query.edit_message_text(
                f"⚡ *Yaddaş Şimşəyi* — Səviyyə {level}\n\n"
                "Ardıcıllığın *BİRİNCİ* emojisi nə idi?",
                parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

        elif data.startswith("yaddash__c_"):
            parts = data.split("_")
            secim = parts[2]; level = int(parts[3]); xal = int(parts[4])
            seq   = st.get("seq", [])
            dogru = seq[0] if seq else ""
            if secim == dogru:
                kazanilan = level * 10
                xal += kazanilan
                self.add_score(context, user.full_name, kazanilan)
                await query.answer(f"✅ Düzgün! +{kazanilan} xal")
                await self._next(query, context, level=level+1, xal=xal, edit=True)
            else:
                self.clear_active(context)
                kb = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_yaddash")],
                    [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
                ])
                await query.edit_message_text(
                    f"❌ *Yanlış!* Düzgün: *{dogru}*\n\n"
                    f"⭐ Ümumi xal: *{xal}*\n🔥 Səviyyə {level}-də bitdi!",
                    parse_mode="Markdown", reply_markup=kb)
