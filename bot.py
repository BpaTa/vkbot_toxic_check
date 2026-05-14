from vkbottle import Bot
from vkbottle.bot import Message

from ml_model.toxicity_classifier import check_message

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("VK_BOT_TOKEN")
bot = Bot(TOKEN)


@bot.on.message()
async def echo(message:Message):
    result = check_message(message.text)
    await message.answer(f"{message.text} - {result}")

print("Бот запущен")
bot.run_forever()


