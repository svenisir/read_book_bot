import asyncio
import logging.config

from aiogram import Dispatcher, Bot
from config_data.config import load_config
from handlers import user_handlers
from keyboards.set_menu import set_main_menu
from logging_settings.logging_dict import logging_config


async def main():
    config = load_config()

    logging.config.dictConfig(logging_config)

    logging.debug('Starting bot')

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
