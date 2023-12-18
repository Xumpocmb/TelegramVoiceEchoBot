from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

# Создаем объекты кнопок
button_1: KeyboardButton = KeyboardButton(text='/start')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            button_1,
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие..'
    # one_time_keyboard=True - свернет клавиатуру после использования
)
