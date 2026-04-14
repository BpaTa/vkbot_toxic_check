import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Union, List, Dict, Any, Optional


class ToxicityClassifier:
    """Класс для классификации текста на наличие нецензурной лексики/токсичности."""

    def __init__(
            self,
            model_name: str = "SkolkovoInstitute/russian_toxicity_classifier",
            device: Optional[str] = None,
            batch_size: int = 32,
            threshold: float = 0.5,
            max_length: int = 512
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self.threshold = threshold
        self.max_length = max_length
        self.device = torch.device(device if device else ("cuda" if torch.cuda.is_available() else "cpu"))
        self._load_model()

    def _load_model(self) -> None:
        """Загрузка токенизатора и модели в память."""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.model.to(self.device)
        self.model.eval()  # Режим инференса
        # Карта меток (обычно {0: "not toxic", 1: "toxic"})
        self.id2label = getattr(self.model.config, "id2label", {0: "not toxic", 1: "toxic"})

    def _process_batch(self, texts: List[str], threshold: float) -> List[Dict[str, Any]]:
        """Внутренний метод для пакетной обработки текстов."""
        results = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            inputs = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            ).to(self.device)

            with torch.no_grad():
                logits = self.model(**inputs).logits
                probs = torch.softmax(logits, dim=-1)
                toxic_scores = probs[:, 1].cpu().tolist()

            for score in toxic_scores:
                is_toxic = score > threshold
                results.append({
                    "is_toxic": is_toxic,
                    "toxic_score": round(score, 4),
                    "label": self.id2label.get(1 if is_toxic else 0, "unknown")
                })
        return results

    def predict(
            self,
            texts: Union[str, List[str]],
            threshold: Optional[float] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Предсказание токсичности для одного текста или списка.
        :param texts: str или List[str]
        :param threshold: Порог срабатывания (переопределяет self.threshold)
        :return: dict или list[dict]
        """
        if threshold is None:
            threshold = self.threshold

        is_single = isinstance(texts, str)
        input_texts = [texts] if is_single else texts

        # Быстрая обработка пустых входов
        if not input_texts or all(t.strip() == "" for t in input_texts):
            default = {"is_toxic": False, "toxic_score": 0.0, "label": "not toxic"}
            return default if is_single else [default] * len(input_texts)

        results = self._process_batch([t.strip() for t in input_texts], threshold)
        return results[0] if is_single else results

    def __call__(self, texts: Union[str, List[str]], threshold: Optional[float] = None):
        """Позволяет вызывать экземпляр как функцию."""
        return self.predict(texts, threshold)