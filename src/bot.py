from vkbottle import Bot
from vkbottle.bot import Message
import logging
from database.base import init_db
from config import BOT_TOKEN
from handlers import chat_labeler
from vkbottle.modules import logger as log
from config import API

logging.getLogger("vkbottle").setLevel("DEBUG")


bot = Bot(api=API)

# Инициализация БД перед запуском бота
bot.loop_wrapper.on_startup.append(init_db())

# Добавление labeler 
bot.labeler.load(command_labeler)
bot.labeler.load(chat_labeler)


log.info("Бот запущен..")
bot.run_forever()
    






