from vkbottle import Bot
from vkbottle.bot import Message
import asyncio
import logging
from ml_model.toxicity_classifier import check_message
from database.base import engine, Base, create_db
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("VK_BOT_TOKEN")
bot = Bot(TOKEN)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG = logging.getLogger(__name__)


@bot.on.message()
async def echo(message:Message):
    result = check_message(message.text)
    LOG.debug(f"Получено сообщение: {message.text}. Уровень токсичности: {result}")
    await message.answer(f"{message.text} - {result}%")

       
if __name__ == "__main__":
    asyncio.run(create_db())
    
    LOG.info("Бот запущен..")
    bot.run_forever()






