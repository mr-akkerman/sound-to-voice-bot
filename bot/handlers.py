import logging
import os
import uuid

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from bot.converter import ConversionError, convert_mp3_to_ogg

logger = logging.getLogger(__name__)

router = Router()

_TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tmp")


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Я конвертирую MP3 в голосовые сообщения.\n\n"
        "Отправь мне .mp3 файл — я верну его как голосовое сообщение."
    )


@router.message(F.audio | (F.document.mime_type == "audio/mpeg"))
async def handle_mp3(message: Message, bot: Bot) -> None:
    # Telegram sends MP3 either as audio (music player) or as document
    doc = message.audio or message.document
    file_id = str(uuid.uuid4())
    mp3_path = os.path.join(_TMP_DIR, f"{file_id}.mp3")
    ogg_path = os.path.join(_TMP_DIR, f"{file_id}.ogg")

    logger.info("Received MP3: %s (%s bytes)", doc.file_name, doc.file_size)

    try:
        await bot.download(doc, destination=mp3_path)
        convert_mp3_to_ogg(mp3_path, ogg_path)
        await message.answer_voice(FSInputFile(ogg_path))
        logger.info("Voice sent for file: %s", doc.file_name)
    except ConversionError as exc:
        logger.error("Conversion failed: %s", exc)
        await message.answer("Не удалось конвертировать файл. Убедись, что это корректный MP3.")
    except Exception as exc:
        logger.error("Unexpected error handling MP3: %s", exc)
        await message.answer("Произошла ошибка при обработке файла. Попробуй ещё раз.")
    finally:
        for path in (mp3_path, ogg_path):
            if os.path.exists(path):
                os.remove(path)


@router.message()
async def handle_other(message: Message) -> None:
    await message.answer("Отправь мне .mp3 файл — я верну его как голосовое сообщение.")
