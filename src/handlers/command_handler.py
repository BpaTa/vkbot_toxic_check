from vkbottle.bot import BotLabeler, Message
from vkbottle.modules import logger as log


command_labeler = BotLabeler()

@command_labeler.chat_message(command=("help", 0))
async def help(message: Message):
    await message.answer(f"""
        Список доступных команд:
                         /help - текущаая подсказка
                         /top - Топ самых токсчиных участников
                         /my_stat - статистика
                         """)
    
@command_labeler.chat_message(command=("stat", 0))
async def top(message: Message):
    pass

@command_labeler.chat_message(command=("my_stat", 0))
async def my_stat(message: Message):
    pass