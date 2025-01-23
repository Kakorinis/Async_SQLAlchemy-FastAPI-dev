from typing import List

from aiogram import Bot

from src.logger import AppLogger


class TelegramBot:
    """
    Телеграм бот в объеме функционала, необходимого для только лишь отправки ботами сообщений в чаты.
    """
    def __init__(self, token):
        self.bot = Bot(token=token)

    async def send_message(self, chat_id: str, message: str) -> None:
        await self.bot.send_message(chat_id=chat_id, text=message)

    async def send_mass_messages(self, chat_ids: List[str], message: str) -> None:
        for chat_id in chat_ids:
            await self.bot.send_message(chat_id=chat_id, text=message)
            AppLogger.info(f"В телегам чат c id: {chat_id} отправлено сообщение:\n'{message}'")