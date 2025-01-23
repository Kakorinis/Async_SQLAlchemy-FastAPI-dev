from .telegram_bot import TelegramBot


async def get_telegram_bot(token: str) -> TelegramBot:
    """
    Зависимость для получения экземпляра aiogram бота.
    """
    return TelegramBot(token=token)
