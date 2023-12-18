import asyncio
import logging

from aiogram import Bot, Dispatcher

from tgbot.config import Config, load_config
from tgbot.handlers import (
    start,
    voice_handler,
)
from tgbot.utils.send_admin_notify import send_notify
from tgbot.utils.set_commands import set_main_menu

logger = logging.getLogger(__name__)


# Запуск бота
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    dp.include_routers(
        start.router,
        voice_handler.router,
    )

    # Пропускаем накопившиеся апдейты и запускаем polling
    # start:
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await send_notify(bot)
        dp.startup.register(set_main_menu)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
