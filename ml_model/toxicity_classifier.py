import os
import torch
import logging
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Union, List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ToxicityClassifier:
    """
    Класс для классификации токсичности с поддержкой кэширования модели.
    Модель скачивается один раз и сохраняется в указанный каталог.
    """

    DEFAULT_CACHE_DIR = Path.home() / ".cache" / "toxicity_models" / "russian_toxicity_classifier"

    def __init__(
            self,
            model_name: str = "s-nlp/russian_toxicity_classifier",
            cache_dir: Optional[Union[str, Path]] = None,
            device: Optional[str] = None,
            batch_size: int = 32,
            threshold: float = 0.5,
            max_length: int = 512,
            force_download: bool = False
    ):
        self.model_name = model_name
        self.cache_dir = Path(cache_dir) if cache_dir else self.DEFAULT_CACHE_DIR
        self.batch_size = batch_size
        self.threshold = threshold
        self.max_length = max_length
        self.device = torch.device(device if device else ("cuda" if torch.cuda.is_available() else "cpu"))
        self.force_download = force_download

        # Создаём директорию кэша, если не существует
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Cache directory: {self.cache_dir}")
        self._load_model()

    def _is_model_cached(self) -> bool:
        """Проверяет, есть ли уже скачанные файлы модели в кэше."""
        required_files = [
            "config.json",
            "pytorch_model.bin",  # или "model.safetensors" для новых моделей
            "tokenizer.json",
            "vocab.json",
            "merges.txt"
        ]
        return all((self.cache_dir / fname).exists() for fname in required_files)

    def _load_model(self) -> None:
        """Загрузка модели с проверкой кэша."""
        # Определяем параметры загрузки
        from_pretrained_kwargs = {
            "cache_dir": str(self.cache_dir),
            "local_files_only": not self.force_download and self._is_model_cached(),
        }

        if self.force_download:
            logger.info("⬇️  Force downloading model (ignoring cache)...")
            from_pretrained_kwargs["local_files_only"] = False
        elif self._is_model_cached():
            logger.info("✅ Model found in cache, loading locally...")
        else:
            logger.info(f"⬇️  Model not found in cache, downloading to {self.cache_dir}...")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                **from_pretrained_kwargs
            )
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                **from_pretrained_kwargs
            )
        except OSError as e:
            if "local_files_only" in str(e):
                logger.warning("⚠️  Cache corrupted or incomplete, re-downloading...")
                # Повторная загрузка без local_files_only
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=str(self.cache_dir))
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name,
                                                                                cache_dir=str(self.cache_dir))
            else:
                raise

        self.model.to(self.device)
        self.model.eval()
        self.id2label = getattr(self.model.config, "id2label", {0: "not toxic", 1: "toxic"})
        logger.info("✅ Model loaded successfully")

    def _process_batch(self, texts: List[str], threshold: float) -> List[Dict[str, Any]]:
        """Пакетная обработка текстов."""
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
        """Предсказание токсичности."""
        if threshold is None:
            threshold = self.threshold

        is_single = isinstance(texts, str)
        input_texts = [texts] if is_single else texts

        if not input_texts or all(t.strip() == "" for t in input_texts):
            default = {"is_toxic": False, "toxic_score": 0.0, "label": "not toxic"}
            return default if is_single else [default] * len(input_texts)

        results = self._process_batch([t.strip() for t in input_texts], threshold)
        return results[0] if is_single else results

    def __call__(self, texts: Union[str, List[str]], threshold: Optional[float] = None):
        """Вызов экземпляра как функции."""
        return self.predict(texts, threshold)