from vkbottle.framework.labeler import BotLabeler

from config import api
from vkbottle.bot import Message

from database.models import User
from database.models.message import get_top_toxic_users

command_labeler = BotLabeler()

@command_labeler.chat_message(text="/stats")
async def handle_commands(message: Message):
    user_info = await api.users.get(user_ids=message.from_id)
    if user_info:
        is_created_user = User.create_user(first_name=user_info[0].first_name, last_name=user_info[0].last_name,
                                           vk_user_id=user_info[0].id)
        if not is_created_user:
            print(f"Пользователь {user_info[0].first_name} {user_info[0].last_name} ({user_info[0].id}) уже добавлен в систему")

    result = get_top_toxic_users(message.peer_id)
    medal_icons = ["🥇", "🥈", "🥉"]
    answer = "Самые токсичные пользователи:\n"
    if result:
        for i, row in enumerate(result):
            answer += f"{medal_icons[i]} {row[0]} {row[1]} | {row[2]:>4} | {round(row[3], 2):>4} | {round(row[4], 2):>4}\n"
    answer += "__________________________________________________________________________________________"
    await message.answer(answer)
