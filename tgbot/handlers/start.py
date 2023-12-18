from time import sleep
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.keyboards import main_menu

router: Router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f'Hello, {message.from_user.username}!', reply_markup=main_menu.keyboard)
    sleep(1)
