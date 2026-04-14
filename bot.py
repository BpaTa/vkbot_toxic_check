import asyncio
import json
import os
from dataclasses import field, fields
from pprint import pprint

from dotenv import load_dotenv
from sqlalchemy.testing.config import ident
from vkbottle import API, Bot
from vkbottle.bot import Message
from vkbottle_types.codegen.objects import UsersFields

from database.models import User
from database.models.message import get_user_toxic_level
from ml_model import toxicity_classifier
from ml_model.toxicity_classifier import ToxicityClassifier

load_dotenv()
# api = API(token=os.environ.get('VK_BOT_TOKEN'))
bot = Bot(token=os.environ.get('VK_BOT_TOKEN'))
toxicity_classifier = ToxicityClassifier()

@bot.on.message()
async def handle_message(message: Message):
    user_info = await bot.api.users.get(user_ids=message.from_id)
    # if (user_info):
    #     is_created_user = User.create_user(first_name=user_info[0].first_name, last_name=user_info[0].last_name, vk_user_id=user_info[0].id)
    #     if not is_created_user:
    #         print(f"Пользователь {user_info[0].first_name} {user_info[0].last_name} ({user_info[0].id}) уже добавлен в систему")

    result = toxicity_classifier.predict(message.text)
    print(f"""datetime: {message.date}
           user_id: {message.from_id}
           text: {message.text}
           user_info: {user_info}
            message: {message}
            result: {result}""")

    await message.answer(f"Привет, {user_info[0].first_name} {user_info[0].last_name}. Твой уровень токсичности - {get_user_toxic_level(message.from_id)}")


if __name__ == '__main__':
    print("Starting bot...")
    bot.run_forever()
