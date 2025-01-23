from dotenv import load_dotenv
from db.models import async_main
from bot import logging  # после выхода в прод надо выключить
import os
import asyncio
from bot import dp, bot

from aiogram.types import BotCommand, BotCommandScopeDefault

from router.user_router import user
from router.admin_router import admin
from router.content import content



async def set_commands() -> None:
    commands = [BotCommand(command="start", description="Старт")]

    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def start_bot():
    await set_commands()


async def stop_bot():
    pass


async def main():
    await async_main()
    load_dotenv()

    dp.include_routers(admin, content, user)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as error:
        print("Somthing went wrong...", error)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
