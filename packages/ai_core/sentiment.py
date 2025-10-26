"""
AUREX.AI - FinBERT Sentiment Analysis.

This module provides sentiment analysis for financial text using the FinBERT model.
"""

import asyncio
from typing import Any

import torch
from loguru import logger
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from packages.shared.config import config


class SentimentAnalyzer:
    """FinBERT-based sentiment analyzer for financial text."""

    def __init__(self) -> None:
        """Initialize the sentiment analyzer."""
        self.model_name = config.FINBERT_MODEL_NAME
        self.device = "cuda" if torch.cuda.is_available() and config.DEVICE == "gpu" else "cpu"
        self.batch_size = config.INFERENCE_BATCH_SIZE
        self.model = None
        self.tokenizer = None
        self.labels = ["negative", "neutral", "positive"]
        logger.info(f"SentimentAnalyzer initialized (device: {self.device})")

    async def load_model(self) -> None:
        """Load the FinBERT model and tokenizer."""
        if self.model is not None:
            return  # Already loaded

        try:
            logger.info(f"Loading FinBERT model: {self.model_name}")

            # Load in executor to avoid blocking
            loop = asyncio.get_event_loop()

            self.tokenizer = await loop.run_in_executor(
                None,
                lambda: AutoTokenizer.from_pretrained(self.model_name),
            )

            self.model = await loop.run_in_executor(
                None,
                lambda: AutoModelForSequenceClassification.from_pretrained(self.model_name),
            )

            self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode

            logger.info(f"✅ FinBERT model loaded on {self.device}")

        except Exception as e:
            logger.error(f"❌ Failed to load FinBERT model: {e}")
            raise

    async def analyze_text(self, text: str) -> dict[str, Any]:
        """
        Analyze sentiment of a single text.

        Args:
            text: Text to analyze

        Returns:
            dict: {"label": str, "score": float, "probabilities": dict}
        """
        if self.model is None:
            await self.load_model()

        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(self.device)

            # Run inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # Get results
            probabilities = predictions[0].cpu().numpy()
            predicted_class = probabilities.argmax()
            confidence = float(probabilities[predicted_class])

            result = {
                "label": self.labels[predicted_class],
                "score": confidence,
                "probabilities": {
                    label: float(prob)
                    for label, prob in zip(self.labels, probabilities)
                },
            }

            return result

        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            return {"label": "neutral", "score": 0.33, "probabilities": {}}

    async def analyze_batch(self, texts: list[str]) -> list[dict[str, Any]]:
        """
        Analyze sentiment of multiple texts in batch.

        Args:
            texts: List of texts to analyze

        Returns:
            list: List of sentiment results
        """
        if self.model is None:
            await self.load_model()

        if not texts:
            return []

        try:
            logger.info(f"Analyzing batch of {len(texts)} texts")

            # Tokenize all texts
            inputs = self.tokenizer(
                texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(self.device)

            # Run inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # Process results
            results = []
            probabilities_np = predictions.cpu().numpy()

            for probs in probabilities_np:
                predicted_class = probs.argmax()
                confidence = float(probs[predicted_class])

                result = {
                    "label": self.labels[predicted_class],
                    "score": confidence,
                    "probabilities": {
                        label: float(prob) for label, prob in zip(self.labels, probs)
                    },
                }
                results.append(result)

            logger.info(f"✅ Batch analysis complete: {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Error in batch analysis: {e}")
            # Return neutral sentiment for all on error
            return [{"label": "neutral", "score": 0.33, "probabilities": {}} for _ in texts]

    def get_model_info(self) -> dict[str, Any]:
        """Get information about the loaded model."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "batch_size": self.batch_size,
            "loaded": self.model is not None,
            "labels": self.labels,
        }


# Global sentiment analyzer instance
_sentiment_analyzer = None


async def get_sentiment_analyzer() -> SentimentAnalyzer:
    """
    Get or create the global sentiment analyzer instance.

    Returns:
        SentimentAnalyzer: Global analyzer instance
    """
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
        await _sentiment_analyzer.load_model()
    return _sentiment_analyzer


async def analyze_sentiment(text: str) -> dict[str, Any]:
    """
    Analyze sentiment of a single text (convenience function).

    Args:
        text: Text to analyze

    Returns:
        dict: Sentiment result
    """
    analyzer = await get_sentiment_analyzer()
    return await analyzer.analyze_text(text)


async def analyze_sentiments_batch(texts: list[str]) -> list[dict[str, Any]]:
    """
    Analyze sentiments of multiple texts (convenience function).

    Args:
        texts: List of texts to analyze

    Returns:
        list: List of sentiment results
    """
    analyzer = await get_sentiment_analyzer()
    return await analyzer.analyze_batch(texts)


async def main() -> None:
    """Main entry point for testing."""
    from packages.shared.logging_config import setup_logging

    setup_logging("sentiment-analyzer", log_level="INFO")

    logger.info("Testing FinBERT Sentiment Analyzer...")

    # Test sentences
    test_sentences = [
        "Gold prices surge to record highs amid economic uncertainty",
        "Federal Reserve announces unexpected rate cut",
        "Market remains stable with minimal volatility",
        "Gold futures plummet as dollar strengthens",
        "Investors cautiously optimistic about gold outlook",
    ]

    # Analyze each sentence
    analyzer = SentimentAnalyzer()
    await analyzer.load_model()

    logger.info("\n" + "=" * 60)
    logger.info("Individual Sentiment Analysis")
    logger.info("=" * 60)

    for text in test_sentences:
        result = await analyzer.analyze_text(text)
        logger.info(f"\nText: {text}")
        logger.info(f"Sentiment: {result['label']} (confidence: {result['score']:.2%})")
        logger.info(f"Probabilities: {result['probabilities']}")

    # Batch analysis
    logger.info("\n" + "=" * 60)
    logger.info("Batch Sentiment Analysis")
    logger.info("=" * 60)

    results = await analyzer.analyze_batch(test_sentences)
    for text, result in zip(test_sentences, results):
        logger.info(f"{result['label']:8} ({result['score']:.2%}) | {text[:50]}...")

    logger.info(f"\n✅ Testing complete!")
    logger.info(f"Model info: {analyzer.get_model_info()}")


if __name__ == "__main__":
    asyncio.run(main())

