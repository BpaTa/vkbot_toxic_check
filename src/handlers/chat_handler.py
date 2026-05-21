from vkbottle.bot import BotLabeler, Message
from services import is_toxic_message
from database.models import User, UserScore
from vkbottle.modules import logger as log

from config import API


chat_labeler = BotLabeler()

@chat_labeler.chat_message()
async def handle_message(message: Message):
    chat_id = message.peer_id
    user_id = message.from_id

    vk_users = await API.users.get(users_ids=[user_id,], fields=['first_name_nom', 'last_name_nom', 'nickname',])
    if vk_users:
        first_name = vk_users[0].first_name
        last_name = vk_users[0].last_name
    else:
        first_name = None
        last_name = None
    
    user = await User.get_user_by_id(user_id)
    if not user:
        await User.create_user(user_id, first_name, last_name)

    
    toxic_message_count, all_message_count = await UserScore.get_messages_count(user_id, chat_id)
    is_toxic = is_toxic_message(message.text)

    if is_toxic:
        toxic_message_count += 1
    
    all_message_count += 1
    toxic_rating = pow(toxic_message_count, 2) / all_message_count
    
    await UserScore.upsert_user_score(user_id, chat_id, toxic_rating, toxic_message_count, all_message_count)
    log.debug(f"Рейтинг токсичности для пользователя {first_name} {last_name} - {toxic_rating}. Количеcтво токсичных сообщений - {toxic_message_count} из {all_message_count}")
    await message.answer(f'{first_name} {last_name} - {toxic_rating}')