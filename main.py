import asyncio
from aiogram import Bot, Dispatcher
from Handlers import bot_messages, user_commands

async def main():
    bot = Bot("|", parse_mode="markdown")
    dp = Dispatcher()
    dp.include_routers(

    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())
