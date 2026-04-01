from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

ICONS = {None: "⬜", "X": "❌", "O": "⭕"}
WINS  = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]


def check_winner(board):
    for c in WINS:
        v = board[c[0]]
        if v and v == board[c[1]] == board[c[2]]:
            return v
    return "draw" if all(x is not None for x in board) else None


def board_kb(board):
    kb = []
    for r in range(3):
        row = []
        for c in range(3):
            i  = r*3+c
            cb = f"xox__move_{i}" if board[i] is None else "xox__noop"
            row.append(InlineKeyboardButton(ICONS[board[i]], callback_data=cb))
        kb.append(row)
    kb.append([InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")])
    return InlineKeyboardMarkup(kb)


class XOX(BaseGame):
    def __init__(self):
        super().__init__("xox", "XOX")

    def handles_callback(self, data, context, user_id):
        return data.startswith("xox__")

    def _get(self, ctx, cid): return ctx.bot_data.get(f"xox_{cid}")
    def _set(self, ctx, cid, s): ctx.bot_data[f"xox_{cid}"] = s
    def _del(self, ctx, cid): ctx.bot_data.pop(f"xox_{cid}", None)

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        cid  = query.message.chat_id
        user = query.from_user
        if self._get(context, cid) and self._get(context, cid).get("active"):
            await query.answer("❌ Artıq oyun gedir! /dur yazın.", show_alert=True); return
        self._set(context, cid, {
            "board": [None]*9, "px": {"id": user.id, "name": user.first_name},
            "po": None, "turn": "X", "active": False, "waiting": True,
        })
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ Oyuna Qoşul (⭕)", callback_data="xox__join")],
            [InlineKeyboardButton("❌ Ləğv Et",          callback_data="xox__cancel")],
        ])
        await query.edit_message_text(
            f"⭕ *XOX — 2 Nəfərlik Oyun*\n\n"
            f"❌ Oyunçu 1: *{user.first_name}*\n"
            "⭕ Oyunçu 2: _Gözlənilir..._\n\n"
            "Qoşulmaq üçün aşağıdakı düyməyə basın:",
            parse_mode="Markdown", reply_markup=kb)

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        cid  = query.message.chat_id
        user = query.from_user
        st   = self._get(context, cid)

        if data == "xox__noop":
            await query.answer(); return

        if data == "xox__cancel":
            if st and st["px"]["id"] == user.id:
                self._del(context, cid)
                kb = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_xox")],
                    [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
                ])
                await query.edit_message_text("❌ *Oyun ləğv edildi.*",
                                              parse_mode="Markdown", reply_markup=kb)
            else:
                await query.answer("Yalnız başladan ləğv edə bilər!", show_alert=True)
            return

        if data == "xox__join":
            if not st or not st.get("waiting"):
                await query.answer("Oyun artıq başlayıb!", show_alert=True); return
            if st["px"]["id"] == user.id:
                await query.answer("Öz oyununuza qoşula bilməzsiniz!", show_alert=True); return
            st.update({"po": {"id": user.id, "name": user.first_name}, "active": True, "waiting": False})
            self._set(context, cid, st)
            await query.edit_message_text(
                f"❌ {st['px']['name']}  vs  ⭕ {st['po']['name']}\n\n"
                f"🎯 Sıra: ❌ *{st['px']['name']}*",
                parse_mode="Markdown", reply_markup=board_kb(st["board"]))
            return

        if data.startswith("xox__move_"):
            if not st or not st.get("active"):
                await query.answer("Oyun aktiv deyil!", show_alert=True); return
            turn = st["turn"]
            cur  = st["px"] if turn == "X" else st["po"]
            if user.id != cur["id"]:
                await query.answer(f"Sıra {cur['name']}-dədir!", show_alert=True); return
            idx = int(data.split("_")[-1])
            if st["board"][idx] is not None:
                await query.answer("Bu xana doludur!", show_alert=True); return
            st["board"][idx] = turn
            winner = check_winner(st["board"])
            if winner:
                self._del(context, cid)
                bd = ""
                for r in range(3):
                    bd += "".join(ICONS[st["board"][r*3+c]] for c in range(3)) + "\n"
                kb = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Yenidən", callback_data="oyun_xox")],
                    [InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")],
                ])
                if winner == "draw":
                    for p in [st["px"], st["po"]]:
                        self.add_score(context, p["name"], 5)
                    txt = f"🤝 *Bərabər!*\n\n{bd}\n⭐ Hər oyunçuya +5 xal!"
                else:
                    wp = st["px"] if winner == "X" else st["po"]
                    wi = "❌" if winner == "X" else "⭕"
                    self.add_score(context, wp["name"], 25)
                    txt = f"🎉 {wi} *{wp['name']} Qazandı!*\n\n{bd}\n⭐ +25 xal!"
                await query.edit_message_text(txt, parse_mode="Markdown", reply_markup=kb)
            else:
                st["turn"] = "O" if turn == "X" else "X"
                nxt = st["po"] if st["turn"] == "O" else st["px"]
                ni  = "⭕" if st["turn"] == "O" else "❌"
                self._set(context, cid, st)
                await query.edit_message_text(
                    f"❌ {st['px']['name']}  vs  ⭕ {st['po']['name']}\n\n"
                    f"🎯 Sıra: {ni} *{nxt['name']}*",
                    parse_mode="Markdown", reply_markup=board_kb(st["board"]))
