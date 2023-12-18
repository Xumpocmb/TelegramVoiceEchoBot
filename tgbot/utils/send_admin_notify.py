import logging
from tgbot.config import Config, load_config


async def send_notify(bot):
    config: Config = load_config()
    for admin in config.tg_bot.admin_ids:
        try:
            await bot.send_message(admin, 'Бот Запущен')
        except Exception as err:
            logging.exception(err)
