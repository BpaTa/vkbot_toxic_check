from vkbottle import Bot
from vkbottle.bot import Message
import asyncio
import logging
from database.base import engine, Base, init_db
import os
from config import BOT_TOKEN
from handlers import chat_labeler


log = logging.getLogger(__name__)


bot = Bot(token=BOT_TOKEN)

# Инициализация БД перед запуском бота
bot.loop_wrapper.on_startup.append(init_db())

# Добавление labeler 
bot.labeler.load(chat_labeler)

log.info("Бот запущен..")
bot.run_forever()
    






