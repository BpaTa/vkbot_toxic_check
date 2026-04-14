from vkbottle import Bot, bot

from config import api
from database.base import Base, engine
from vkbottle import Bot

from config import api, labeler
from database.base import Base, engine
from handlers import command_labeler
from handlers import chat_labeler

labeler.load(command_labeler)
labeler.load(chat_labeler)

bot = Bot(api=api, labeler=labeler)

Base.metadata.create_all(engine)

print("Бот запущен...")
bot.run_forever()
