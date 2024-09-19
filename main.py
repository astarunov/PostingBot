import asyncio
from aiogram import Bot, Dispatcher
from Handlers import bot_messages, user_commands

async def main():
    bot = Bot("7232023894:AAFLWTVGE6AMFq942K0SMoEVMT2elPTWdiw")
    dp = Dispatcher()
    user_commands.scheduler.start()
    dp.include_routers(
        user_commands.router,
    )


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())
