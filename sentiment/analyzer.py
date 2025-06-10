from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import openai
from typing import Dict, Any
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        openai.api_key = Config.OPENAI_API_KEY
        
    def analyze_textblob(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            return {
                'polarity': blob.sentiment.polarity,  # -1 to 1
                'subjectivity': blob.sentiment.subjectivity  # 0 to 1
            }
        except Exception as e:
            logger.error(f"TextBlob analysis failed: {e}")
            return {'polarity': 0.0, 'subjectivity': 0.0}
    
    def analyze_vader(self, text: str) -> Dict[str, float]:
        """Analyze sentiment using VADER"""
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            return scores  # Returns: neg, neu, pos, compound
        except Exception as e:
            logger.error(f"VADER analysis failed: {e}")
            return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
    
    def analyze_gpt(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using GPT with a simple prompt"""
        try:
            prompt = f"""
            Analyze the sentiment of this text on a scale from -1 to 1, where:
            -1 = Very Negative
            0 = Neutral  
            1 = Very Positive
            
            Also provide a brief emotional context (1-3 words).
            
            Text: "{text}"
            
            Respond in this exact format:
            Score: [number]
            Emotion: [emotion words]
            """
            
            response = openai.chat.completions.create(
                model=Config.GPT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=Config.GPT_MAX_TOKENS,
                temperature=0.3  # Lower temp for more consistent scoring
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse the response
            lines = content.split('\n')
            score = 0.0
            emotion = "neutral"
            
            for line in lines:
                if line.startswith('Score:'):
                    try:
                        score = float(line.split(':')[1].strip())
                    except:
                        pass
                elif line.startswith('Emotion:'):
                    emotion = line.split(':')[1].strip()
            
            return {
                'score': max(-1, min(1, score)),  # Clamp between -1 and 1
                'emotion': emotion,
                'raw_response': content
            }
            
        except Exception as e:
            logger.error(f"GPT analysis failed: {e}")
            return {'score': 0.0, 'emotion': 'neutral', 'raw_response': ''}
    
    def get_mood_category(self, combined_score: float) -> str:
        """Convert combined score to mood category"""
        if combined_score >= 0.5:
            return 'very_positive'
        elif combined_score >= Config.SENTIMENT_THRESHOLD_POSITIVE:
            return 'positive'
        elif combined_score <= -0.5:
            return 'very_negative'
        elif combined_score <= Config.SENTIMENT_THRESHOLD_NEGATIVE:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_comprehensive(self, text: str) -> Dict[str, Any]:
        """Run all three sentiment analyses and combine results"""
        logger.info(f"Analyzing text: {text[:50]}...")
        
        # Get all three analyses
        textblob_result = self.analyze_textblob(text)
        vader_result = self.analyze_vader(text)
        gpt_result = self.analyze_gpt(text)
        
        # Combine scores (weighted average)
        combined_score = (
            textblob_result['polarity'] * 0.3 +
            vader_result['compound'] * 0.3 +
            gpt_result['score'] * 0.4
        )
        
        # Get mood category and labels
        mood_category = self.get_mood_category(combined_score)
        mood_info = Config.MOOD_LABELS[mood_category]
        
        result = {
            'text': text,
            'combined_score': round(combined_score, 3),
            'mood_category': mood_category,
            'mood_emoji': mood_info['emoji'],
            'mood_vibe': mood_info['vibe'],
            'individual_scores': {
                'textblob': textblob_result,
                'vader': vader_result,
                'gpt': gpt_result
            },
            'analysis_summary': f"{mood_info['emoji']} {mood_info['vibe']} (Score: {combined_score:.2f})"
        }
        
        logger.info(f"Analysis complete: {result['analysis_summary']}")
        return result

# Convenience function for quick analysis
def quick_analyze(text: str) -> Dict[str, Any]:
    """Quick sentiment analysis function"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_comprehensive(text)