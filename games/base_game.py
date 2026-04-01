from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

MENU_KB = InlineKeyboardMarkup([[
    InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")
]])


class BaseGame:
    def __init__(self, key: str, name: str):
        self.key  = key
        self.name = name

    def handles_callback(self, data: str, context, user_id: int) -> bool:
        return data.startswith(f"{self.key}__")

    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        raise NotImplementedError

    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def handle_message(self, update, context: ContextTypes.DEFAULT_TYPE):
        pass

    def add_score(self, context, user_name: str, pts: int):
        context.bot_data.setdefault("scores", {})
        context.bot_data["scores"][user_name] = (
            context.bot_data["scores"].get(user_name, 0) + pts
        )

    def set_active(self, context):
        context.user_data["active_game"] = self.key

    def clear_active(self, context):
        context.user_data.pop("active_game", None)
        context.user_data.pop("game_state", None)

    @staticmethod
    def back_kb(extra: list = None):
        rows = extra or []
        rows.append([InlineKeyboardButton("🔙 Oyun Menyusu", callback_data="ana_menu")])
        return InlineKeyboardMarkup(rows)
