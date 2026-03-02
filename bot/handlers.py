from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Я конвертирую MP3 в голосовые сообщения.\n\n"
        "Отправь мне .mp3 файл — я верну его как голосовое сообщение."
    )
