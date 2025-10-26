"""
AUREX.AI - Sentiment Analysis Tests.
"""

import pytest

from packages.ai_core.sentiment import SentimentAnalyzer


@pytest.mark.asyncio
class TestSentimentAnalyzer:
    """Test FinBERT sentiment analyzer."""

    @pytest.mark.skip(reason="Requires FinBERT model download")
    async def test_sentiment_analyzer_init(self):
        """Test sentiment analyzer initialization."""
        analyzer = SentimentAnalyzer()
        assert analyzer.model_name == "ProsusAI/finbert"
        assert analyzer.labels == ["negative", "neutral", "positive"]

    @pytest.mark.skip(reason="Requires FinBERT model download")
    async def test_analyze_positive_text(self):
        """Test analyzing positive sentiment."""
        analyzer = SentimentAnalyzer()
        await analyzer.load_model()

        text = "Gold prices surge to record highs as investors rush to safe havens"
        result = await analyzer.analyze_text(text)

        assert result["label"] in ["positive", "neutral", "negative"]
        assert 0 <= result["score"] <= 1
        assert "probabilities" in result

    @pytest.mark.skip(reason="Requires FinBERT model download")
    async def test_analyze_negative_text(self):
        """Test analyzing negative sentiment."""
        analyzer = SentimentAnalyzer()
        await analyzer.load_model()

        text = "Gold prices plummet as economic outlook improves"
        result = await analyzer.analyze_text(text)

        assert result["label"] in ["positive", "neutral", "negative"]
        assert 0 <= result["score"] <= 1

    @pytest.mark.skip(reason="Requires FinBERT model download")
    async def test_analyze_batch(self):
        """Test batch sentiment analysis."""
        analyzer = SentimentAnalyzer()
        await analyzer.load_model()

        texts = [
            "Gold prices surge dramatically",
            "Market remains stable today",
            "Gold prices fall sharply",
        ]

        results = await analyzer.analyze_batch(texts)

        assert len(results) == 3
        for result in results:
            assert result["label"] in ["positive", "neutral", "negative"]
            assert 0 <= result["score"] <= 1

    async def test_sentiment_error_handling(self):
        """Test sentiment analyzer error handling."""
        analyzer = SentimentAnalyzer()

        # Should return neutral sentiment on error
        result = await analyzer.analyze_text("")

        assert result["label"] == "neutral"
        assert result["score"] == 0.33

    @pytest.mark.skip(reason="Requires FinBERT model download")
    async def test_get_model_info(self):
        """Test getting model info."""
        analyzer = SentimentAnalyzer()

        info = analyzer.get_model_info()

        assert info["model_name"] == "ProsusAI/finbert"
        assert info["device"] in ["cpu", "cuda"]
        assert "labels" in info

