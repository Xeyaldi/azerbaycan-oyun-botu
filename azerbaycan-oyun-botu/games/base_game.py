from abc import ABC, abstractmethod
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

class BaseGame(ABC):
    def __init__(self, game_key: str, game_name: str):
        self.game_key = game_key
        self.game_name = game_name

    @abstractmethod
    async def start_game(self, query, context: ContextTypes.DEFAULT_TYPE):
        pass

    @abstractmethod
    async def handle_callback(self, query, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    def handles_callback(self, data: str, context, user_id: int) -> bool:
        active = context.user_data.get("active_game")
        return active == self.game_key and data.startswith(self.game_key)

    def add_score(self, context, user_name: str, points: int):
        if "scores" not in context.bot_data:
            context.bot_data["scores"] = {}
        context.bot_data["scores"][user_name] = (
            context.bot_data["scores"].get(user_name, 0) + points
        )

    def back_button(self):
        return [[InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]]

    def back_and_retry_buttons(self, retry_data: str):
        return [
            [InlineKeyboardButton("🔄 Yenidən", callback_data=retry_data)],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="ana_menu")]
        ]
