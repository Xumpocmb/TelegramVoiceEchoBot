import os
import subprocess

import speech_recognition as sr
from aiogram import Bot
from aiogram import Router, F
from aiogram.types import Message

from tgbot.config import Config, load_config
from tgbot.keyboards import main_menu

router: Router = Router()
config: Config = load_config()
bot: Bot = Bot(token=config.tg_bot.token)


@router.message(F.voice)
async def voice_handler(message: Message):
    # Получаем файл голосового сообщения
    if message.content_type == F.ContentType.VOICE:
        voice_id = message.voice.file_id
    elif message.content_type == F.ContentType.AUDIO:
        voice_id = message.audio.file_id
    elif message.content_type == F.ContentType.DOCUMENT:
        voice_id = message.document.file_id
    else:
        await message.reply("Формат документа не поддерживается")
        return

    # Проверяем наличие директории для сохранения файлов голосовых сообщений
    if not os.path.exists("voice"):
        os.makedirs("voice")
    file = await bot.get_file(voice_id)
    file_path = file.file_path
    voice_path = f"voice/voice_{message.from_user.id}.oga"
    await bot.download_file(file_path, voice_path)
    await message.reply("Аудио получено")

    # Преобразуем формат файла в WAV (SpeechRecognition поддерживает WAV)
    subprocess.run(['bin/ffmpeg', '-i', voice_path, voice_path[:-4] + '.wav'])
    voice_path = voice_path[:-4] + '.wav'

    # Распознаем текст с использованием SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(voice_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            await message.reply(f"Текст из голосового сообщения: {text}", reply_markup=main_menu.keyboard)
        except sr.UnknownValueError:
            await message.reply("Не удалось распознать голосовое сообщение.", reply_markup=main_menu.keyboard)
        except sr.RequestError as e:
            await message.reply(f"Ошибка запроса к API распознавания: {e}", reply_markup=main_menu.keyboard)

    # Удаляем временные файлы
    os.remove(voice_path)
    os.remove(voice_path[:-4] + '.oga')
    print('Done!')
