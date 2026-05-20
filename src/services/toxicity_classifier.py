import torch
import torch.nn.functional as F
from transformers import BertTokenizer, pipeline, BertForSequenceClassification
import logging

from config import ML_MODEL, ML_MODEL_CACHE_DIR, TOXIC_LEVEL_THRESHOLD

log = logging.getLogger(__name__)

try:
    tokenizer = BertTokenizer.from_pretrained(ML_MODEL, cache_dir=ML_MODEL_CACHE_DIR)
    model = BertForSequenceClassification.from_pretrained(ML_MODEL, cache_dir=ML_MODEL_CACHE_DIR)
    log.info(f"Модель {ML_MODEL} загружен из кэша")
except:
    tokenizer = BertTokenizer.from_pretrained(ML_MODEL)
    tokenizer.save_pretrained(ML_MODEL_CACHE_DIR)

    model = BertForSequenceClassification.from_pretrained(ML_MODEL)
    model.save_pretrained(ML_MODEL_CACHE_DIR)
    log.info(f"Модель {ML_MODEL} сохранена в кэш")

    
def is_toxic_message(text: str) -> bool:
    input = tokenizer(text, return_tensors='pt')
    log.debug(f"Вычисление уровня токсичности для сообщения {text}")
    with torch.no_grad():
        logits = model(**input).logits

    toxic_score = round(F.softmax(logits, dim=1)[0,1].item(), 3)
    log.debug(f"Уровень токсчиности для сообщения {text} - {toxic_score}")
    
    return  toxic_score >= TOXIC_LEVEL_THRESHOLD
