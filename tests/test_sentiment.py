# tests/test_sentiment.py
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentiment.analyzer import SentimentAnalyzer, quick_analyze

class TestSentimentAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return SentimentAnalyzer()
    
    def test_textblob_analysis(self, analyzer):
        """Test TextBlob sentiment analysis"""
        positive_text = "I love this so much!"
        negative_text = "I hate everything"
        
        pos_result = analyzer.analyze_textblob(positive_text)
        neg_result = analyzer.analyze_textblob(negative_text)
        
        assert pos_result['polarity'] > 0
        assert neg_result['polarity'] < 0
        assert 0 <= pos_result['subjectivity'] <= 1
    
    def test_vader_analysis(self, analyzer):
        """Test VADER sentiment analysis"""
        positive_text = "This is absolutely amazing!"
        negative_text = "This is terrible"
        
        pos_result = analyzer.analyze_vader(positive_text)
        neg_result = analyzer.analyze_vader(negative_text)
        
        assert pos_result['compound'] > 0
        assert neg_result['compound'] < 0
        assert 'pos' in pos_result
        assert 'neg' in pos_result
    
    def test_mood_categorization(self, analyzer):
        """Test mood category assignment"""
        assert analyzer.get_mood_category(0.8) == 'very_positive'
        assert analyzer.get_mood_category(0.2) == 'positive'
        assert analyzer.get_mood_category(0.0) == 'neutral'
        assert analyzer.get_mood_category(-0.2) == 'negative'
        assert analyzer.get_mood_category(-0.8) == 'very_negative'
    
    def test_comprehensive_analysis(self, analyzer):
        """Test comprehensive analysis"""
        text = "I'm having a great day!"
        result = analyzer.analyze_comprehensive(text)
        
        required_keys = ['text', 'combined_score', 'mood_category', 'mood_emoji', 'mood_vibe']
        for key in required_keys:
            assert key in result
        
        assert result['text'] == text
        assert isinstance(result['combined_score'], float)
        assert result['mood_category'] in ['very_positive', 'positive', 'neutral', 'negative', 'very_negative']

# tests/test_sass_quotes.py
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sass_quotes.sass_gen import SassQuoteGenerator
from sentiment.analyzer import SentimentAnalyzer

class TestSassQuoteGenerator:
    @pytest.fixture
    def generator(self):
        return SassQuoteGenerator()
    
    @pytest.fixture
    def sample_sentiment(self):
        analyzer = SentimentAnalyzer()
        return analyzer.analyze_comprehensive("I'm feeling great today!")
    
    def test_fallback_quotes(self, generator):
        """Test fallback quote generation"""
        for mood in ['very_positive', 'positive', 'neutral', 'negative', 'very_negative']:
            quote = generator.get_fallback_quote(mood)
            assert isinstance(quote, str)
            assert len(quote) > 0
    
    def test_sass_quote_generation(self, generator, sample_sentiment):
        """Test sass quote generation"""
        result = generator.generate_sass_quote(sample_sentiment, use_gpt=False)
        
        required_keys = ['sass_quote', 'mood_category', 'mood_vibe', 'formatted_output']
        for key in required_keys:
            assert key in result
        
        assert isinstance(result['sass_quote'], str)
        assert len(result['sass_quote']) > 0
    
    def test_multiple_quotes(self, generator, sample_sentiment):
        """Test multiple quote generation"""
        quotes = generator.generate_multiple_quotes(sample_sentiment, count=3)
        
        assert len(quotes) == 3
        for quote in quotes:
            assert 'sass_quote' in quote
            assert 'formatted_output' in quote

if __name__ == "__main__":
    pytest.main([__file__])