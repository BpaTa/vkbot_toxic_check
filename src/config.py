from envparse import env
from vkbottle import API

env.read_envfile('.env')

# VK
BOT_TOKEN = env.str('BOT_TOKEN')
API = API(token=BOT_TOKEN)

# Database
POSTGRES_HOST = env.str('POSTGRES_HOST', default='localhost')
POSTGRES_PORT = env.str('POSTGRES_PORT', default=5432)
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_DB = env.str('POSTGRES_DB')
SQLALCHEMY_DATABASE_URI = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'  # noqa
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ML 
ML_MODEL = env.str('ML_MODEL', default='s-nlp/russian_toxicity_classifier')
ML_MODEL_CACHE_DIR = env.str('ML_MODEL_CACHE_DIR', default='./ml_model')
TOXIC_LEVEL_THRESHOLD = env.float('TOXIC_LEVEL_THRESHOLD', default=0.75)

