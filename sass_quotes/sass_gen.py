import openai
import random
from typing import Dict, List, Any
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SassQuoteGenerator:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        
        # Fallback sass quotes for each mood (in case GPT fails)
        self.fallback_quotes = {
            'very_positive': [
                "You're literally glowing right now ✨",
                "Main character energy is OFF THE CHARTS 🔥",
                "Someone's living their best life and I'm here for it 💫"
            ],
            'positive': [
                "Look at you being all optimistic and stuff 😊",
                "Good vibes only, I see you 🌟",
                "Your energy is giving 'everything's gonna be fine' ✨"
            ],
            'neutral': [
                "Giving off strong 'existing' vibes today 😐",
                "Ah, the classic 'I'm fine' energy. Iconic. 🤷",
                "Neutrality is a choice, and you chose... adequately 📱"
            ],
            'negative': [
                "Someone's having a whole mood today 😞",
                "Life really said 'let's test this one' huh? 💔",
                "Your vibe is giving 'Monday morning' energy 🌧️"
            ],
            'very_negative': [
                "Bestie, who hurt you? (We're gonna key their car) 💀",
                "You're serving 'main character tragic backstory' realness 🖤",
                "This energy is DARK dark. We Stan a dramatic queen 👑"
            ]
        }
    
    def generate_gpt_sass_quote(self, mood_category: str, mood_vibe: str, sentiment_score: float, original_text: str = "") -> str:
        """Generate a sassy quote using GPT based on sentiment analysis"""
        try:
            # Create a dynamic prompt based on mood
            mood_descriptions = {
                'very_positive': "extremely happy, energetic, over-the-top positive",
                'positive': "happy, upbeat, optimistic",
                'neutral': "indifferent, meh, neither good nor bad",
                'negative': "sad, disappointed, down",
                'very_negative': "very upset, angry, devastated"
            }
            
            prompt = f"""
            You're a sassy, witty friend giving quotes based on someone's mood. 
            
            Their current vibe: {mood_vibe} ({mood_descriptions.get(mood_category, 'unknown')})
            Sentiment score: {sentiment_score} (where -1 is very negative, +1 is very positive)
            
            Generate a SHORT (under 15 words), sassy, modern quote that matches their energy.
            
            Style guidelines:
            - Use Gen Z/millennial language 
            - Include 1-2 relevant emojis
            - Be supportive but sassy
            - Match the energy level (don't be too upbeat for negative moods)
            
            Examples for reference:
            Very positive: "You're literally the main character today ✨🔥"
            Positive: "Someone's radiating good energy and I'm here for it 🌟"
            Neutral: "Giving off strong 'existing peacefully' vibes 😌"
            Negative: "Life really tested you today, huh? 💔"
            Very negative: "Bestie, we're surviving this together 💀🖤"
            
            Generate ONE quote:
            """
            
            response = openai.chat.completions.create(
                model=Config.GPT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=Config.GPT_MAX_TOKENS,
                temperature=Config.GPT_TEMPERATURE
            )
            
            quote = response.choices[0].message.content.strip()
            
            # Clean up the quote (remove quotes if GPT added them)
            quote = quote.strip('"').strip("'")
            
            logger.info(f"Generated GPT sass quote: {quote}")
            return quote
            
        except Exception as e:
            logger.error(f"GPT sass quote generation failed: {e}")
            return self.get_fallback_quote(mood_category)
    
    def get_fallback_quote(self, mood_category: str) -> str:
        """Get a random fallback quote for the mood category"""
        quotes = self.fallback_quotes.get(mood_category, self.fallback_quotes['neutral'])
        return random.choice(quotes)
    
    def generate_sass_quote(self, sentiment_analysis: Dict[str, Any], use_gpt: bool = True) -> Dict[str, Any]:
        """Generate a sass quote based on sentiment analysis results"""
        mood_category = sentiment_analysis['mood_category']
        mood_vibe = sentiment_analysis['mood_vibe']
        sentiment_score = sentiment_analysis['combined_score']
        original_text = sentiment_analysis.get('text', '')
        
        logger.info(f"Generating sass quote for {mood_category} mood")
        
        if use_gpt:
            sass_quote = self.generate_gpt_sass_quote(
                mood_category, mood_vibe, sentiment_score, original_text
            )
        else:
            sass_quote = self.get_fallback_quote(mood_category)
        
        result = {
            'sass_quote': sass_quote,
            'mood_category': mood_category,
            'mood_vibe': mood_vibe,
            'mood_emoji': sentiment_analysis['mood_emoji'],
            'sentiment_score': sentiment_score,
            'generation_method': 'gpt' if use_gpt else 'fallback',
            'formatted_output': f"{sentiment_analysis['mood_emoji']} {sass_quote}"
        }
        
        logger.info(f"Sass quote generated: {result['formatted_output']}")
        return result
    
    def generate_multiple_quotes(self, sentiment_analysis: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
        """Generate multiple sass quotes for variety"""
        quotes = []
        
        # Generate one GPT quote
        quotes.append(self.generate_sass_quote(sentiment_analysis, use_gpt=True))
        
        # Add fallback quotes for variety
        for _ in range(count - 1):
            fallback_quote = self.get_fallback_quote(sentiment_analysis['mood_category'])
            quotes.append({
                'sass_quote': fallback_quote,
                'mood_category': sentiment_analysis['mood_category'],
                'mood_vibe': sentiment_analysis['mood_vibe'],
                'mood_emoji': sentiment_analysis['mood_emoji'],
                'sentiment_score': sentiment_analysis['combined_score'],
                'generation_method': 'fallback',
                'formatted_output': f"{sentiment_analysis['mood_emoji']} {fallback_quote}"
            })
        
        return quotes

# Convenience function for quick sass quote generation
def quick_sass(text: str) -> str:
    """Quick sass quote generation from text"""
    from sentiment.analyzer import quick_analyze
    
    # Analyze sentiment first
    sentiment_result = quick_analyze(text)
    
    # Generate sass quote
    sass_generator = SassQuoteGenerator()
    sass_result = sass_generator.generate_sass_quote(sentiment_result)
    
    return sass_result['formatted_output']