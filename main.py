import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN is not set in environment variables")

    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
