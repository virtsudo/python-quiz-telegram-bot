from asyncio import run
from logging import basicConfig, INFO
from os import environ
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import BotCommand
from app.handler import common, game

BOT_TOKEN = environ['BOT_TOKEN']


async def main():
    basicConfig(level=INFO, format="%(asctime)s\n\t- %(levelname)s - %(name)s - %(message)s")
    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)
    bot = Bot(token=BOT_TOKEN)

    dp.include_router(common.router)
    dp.include_router(game.router)

    await set_commands(bot)
    # await bot.delete_my_commands()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description="Start"),
        BotCommand(command='cancel', description="Cancel")
    ]
    await bot.set_my_commands(commands)


if __name__ == '__main__':
    run(main())
