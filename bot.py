import asyncio

from aiogram import Dispatcher, Bot
from config_data.config import load_config


async def main():
    config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())