import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from games.base_game import BaseGame

class XOX(BaseGame):
    def __init__(self):
        super().__init__("xox", "XOX")

    def handles_callback(self, data: str, context, user_id: int) -> bool:
        return data.startswith("xox_")

    def _create_board_keyboard(self, board):
        icons = {" ": "⬜", "X": "❌", "O": "⭕"}
        keyboard = []
        for r in range(3):
            row = []
            for c in range(3):
                idx = r * 3 + c
                cell = board[idx]
                row.append(InlineKeyboardButton(
                    icons[cell],
                    callback_data=f"xox_move_{idx}" if cell == " " else f"xox_noop_{idx}"
                ))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")])
        return InlineKeyboardMarkup(keyboard)

    def _check_winner(self, board):
        wins = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for combo in wins:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
                return board[combo[0]]
        if " " not in board:
            return "berabere"
        return None

    def _bot_move(self, board):
        # Try to win
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                if self._check_winner(board) == "O":
                    return i
                board[i] = " "
        # Block player
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                if self._check_winner(board) == "X":
                    board[i] = " "
                    return i
                board[i] = " "
        # Center
        if board[4] == " ":
            return 4
        # Corner
        for i in [0, 2, 6, 8]:
            if board[i] == " ":
                return i
        # Any
        empty = [i for i, v in enumerate(board) if v == " "]
        return random.choice(empty) if empty else -1

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        board = [" "] * 9
        context.user_data["active_game"] = self.game_key
        context.user_data["game_state"] = {"board": board, "turn": "X"}
        text = "⭕ *XOX Oyunu*\n\nSiz ❌, Bot ⭕\nSıra sizdədir!"
        await query.edit_message_text(
            text, parse_mode="Markdown",
            reply_markup=self._create_board_keyboard(board)
        )

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        data = query.data
        if data.startswith("xox_noop"):
            await query.answer("Bu xana doludur!", show_alert=False)
            return
        if data == "xox_yeniden":
            await self.start_game(query, context)
            return

        if not data.startswith("xox_move_"):
            return

        state = context.user_data.get("game_state", {})
        board = state.get("board", [" "] * 9)
        user = query.from_user
        idx = int(data.replace("xox_move_", ""))

        if board[idx] != " ":
            await query.answer("Bu xana doludur!", show_alert=True)
            return

        board[idx] = "X"
        winner = self._check_winner(board)

        if winner:
            await self._end_game(query, context, board, winner, user)
            return

        bot_idx = self._bot_move(board)
        if bot_idx >= 0:
            board[bot_idx] = "O"

        winner = self._check_winner(board)
        state["board"] = board
        context.user_data["game_state"] = state

        if winner:
            await self._end_game(query, context, board, winner, user)
        else:
            await query.edit_message_text(
                "⭕ *XOX Oyunu*\n\nSıra sizdədir! ❌",
                parse_mode="Markdown",
                reply_markup=self._create_board_keyboard(board)
            )

    async def _end_game(self, query, context, board, winner, user):
        context.user_data.pop("active_game", None)
        context.user_data.pop("game_state", None)
        keyboard = [
            [InlineKeyboardButton("🔄 Yenidən Oyna", callback_data="xox_yeniden")],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
        ]
        if winner == "X":
            self.add_score(context, user.full_name, 20)
            text = "🎉 *Siz Qazandınız!* ❌\n\n⭐ +20 xal!"
        elif winner == "O":
            text = "😔 *Bot Qazandı!* ⭕\n\nYenidən cəhd edin!"
        else:
            self.add_score(context, user.full_name, 5)
            text = "🤝 *Bərabər!*\n\n⭐ +5 xal!"

        icons = {" ": "⬜", "X": "❌", "O": "⭕"}
        board_display = ""
        for r in range(3):
            board_display += "".join(icons[board[r*3+c]] for c in range(3)) + "\n"

        await query.edit_message_text(
            f"{text}\n\n{board_display}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
