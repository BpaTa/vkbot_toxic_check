import os

from dotenv import load_dotenv
from vkbottle import API
from vkbottle.framework.labeler import BotLabeler

from ml_model.toxicity_classifier import ToxicityClassifier

load_dotenv()
api = API(token=os.environ.get('VK_BOT_TOKEN'))
labeler = BotLabeler()
toxic_classifier = ToxicityClassifier()

TOXIC_SCORE_THRESHOLD = 0.75