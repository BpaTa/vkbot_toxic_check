import torch
import torch.nn.functional as F
from transformers import BertTokenizer, pipeline, BertForSequenceClassification
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
LOG = logging.getLogger(__name__)

#MODEL = "s-nlp/russian_toxicity_classifier"
MODEL = "apanc/russian-inappropriate-messages"

try:
    tokenizer = BertTokenizer.from_pretrained(MODEL, cache_dir="./ml_model")
    model = BertForSequenceClassification.from_pretrained(MODEL, cache_dir="./ml_model")
    LOG.info(f"Модель {MODEL} загружен из кэша")
except:
    tokenizer = BertTokenizer.from_pretrained(MODEL)
    tokenizer.save_pretrained("./ml_model")

    model = BertForSequenceClassification.from_pretrained(MODEL)
    model.save_pretrained("./ml_model")
    LOG.info(f"Модель {MODEL} сохранена в кэш")

    
def check_message(text: str):
    input = tokenizer(text, return_tensors='pt')
    LOG.debug(f"Вычисление уровня токсичности для сообщения {text}")
    with torch.no_grad():
        logits = model(**input).logits
    
    return round(F.softmax(logits, dim=1)[0,1].item()*100, 3) 
