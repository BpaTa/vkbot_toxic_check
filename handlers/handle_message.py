from logging import log

from vkbottle.framework.labeler import BotLabeler

from config import toxic_classifier, api, TOXIC_SCORE_THRESHOLD
from vkbottle.bot import Message

from database.models import User
from database.models.message import save_message
from database.models.user import calc_toxic_rating, update_user_toxic_rating

chat_labeler = BotLabeler()

@chat_labeler.chat_message()
async def handle_message(message: Message):

    user_info = await api.users.get(user_ids=message.from_id)

    # Создаем пользователя в таблице users, если он еще не был добавлен
    if user_info:
        is_created_user = User.create_user(first_name=user_info[0].first_name, last_name=user_info[0].last_name,
                                           vk_user_id=user_info[0].id)
        if not is_created_user:
            print(
                f"Пользователь {user_info[0].first_name} {user_info[0].last_name} ({user_info[0].id}) уже добавлен в систему")

    # Считаем уровень токсичности сообщения
    toxic_score = float(toxic_classifier.predict(message.text).get("toxic_score"))
    is_toxic = toxic_score > TOXIC_SCORE_THRESHOLD

    # Сохраняем сообщение в БД
    save_message(date=message.date.utcnow(), from_id=message.from_id, text=message.text, chat_id=message.peer_id,
                 toxic_score=toxic_score, is_toxic=is_toxic)
    log(f"Сообщение от {message.from_id} было сохранено в БД")

    # Обновляем рейтинг токсичности пользователя
    user_toxic_rating = calc_toxic_rating(user_id=message.from_id)
    update_user_toxic_rating(user_id=message.from_id, toxic_rating=user_toxic_rating)
    log(f"Рейтинг токсичности пользователя {message.from_id} равен {user_toxic_rating}")

