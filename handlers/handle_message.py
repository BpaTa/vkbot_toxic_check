from vkbottle.framework.labeler import BotLabeler

from config import toxic_classifier, api
from vkbottle.bot import Message

from database.models import User
from database.models.message import save_message

chat_labeler = BotLabeler()

@chat_labeler.chat_message()
async def handle_message(message: Message):
    user_info = await api.users.get(user_ids=message.from_id)
    if user_info:
        is_created_user = User.create_user(first_name=user_info[0].first_name, last_name=user_info[0].last_name,
                                           vk_user_id=user_info[0].id)
        if not is_created_user:
            print(
                f"Пользователь {user_info[0].first_name} {user_info[0].last_name} ({user_info[0].id}) уже добавлен в систему")

    toxic_score = float(toxic_classifier.predict(message.text).get("toxic_score"))

    save_message(date=message.date.utcnow(), toxic_level=toxic_score, text=message.text, chat_id=message.peer_id,
                 from_id=message.from_id)
    print(f"Сообщение от {message.from_id} было сохранено в БД")
    if toxic_score > 0.6:
        await message.answer(
            f"{user_info[0].first_name} {user_info[0].last_name}. Твой уровень токсичности - {toxic_score}")
