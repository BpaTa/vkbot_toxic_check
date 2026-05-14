from vkbottle import Bot
from vkbottle.bot import Message

from ml_model.toxicity_classifier import check_message

 
TOKEN = 'vk1.a.8gwJ-lmoIacQSOK4zMXBWu183EOu8Ni_YefxZi2zS9n-n4pFCVTojbrShVvckxtG8k68onOt2JlziZU6dXjHZDAhy5rtu_OWGm2YMqXjRvOZn0iwAmOSZuX8NYLFUNULKsE4uNxPZtO6CA7-fqtLrgTZlqPpqiZtPAay2OTDiOsQsTljhzm1Jqib3TMIUeYSzpFNALQN0OZER0rNOb7m-w'
bot = Bot(TOKEN)


@bot.on.message()
async def echo(message:Message):
    result = check_message(message.text)
    await message.answer(f"{message.text} - {result}")

print("Бот запущен")
bot.run_forever()


