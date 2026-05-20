from vkbottle.bot import BotLabeler, Message
from services import is_toxic_message

chat_labeler = BotLabeler()

@chat_labeler.chat_message()
async def handle_message(message: Message):
    is_toxic = is_toxic_message(message.text)
    await message.answer(f'{message.text} - {is_toxic}')