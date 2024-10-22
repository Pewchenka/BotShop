import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router

dp = Dispatcher()
bot = Bot(token=TOKEN)

async def main():
	dp.include_router(router)
	await dp.start_polling(bot)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG) #Use only for debug, because it's slow down the bot
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("Exit")
