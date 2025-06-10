import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenAI API Key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Sentiment Analysis Settings
    SENTIMENT_THRESHOLD_POSITIVE = 0.1
    SENTIMENT_THRESHOLD_NEGATIVE = -0.1
    
    # GPT Settings
    GPT_MODEL = "gpt-3.5-turbo"
    GPT_MAX_TOKENS = 150
    GPT_TEMPERATURE = 0.8
    
    # Mood Labels with Emojis
    MOOD_LABELS = {
        'very_positive': {'emoji': '🔥', 'vibe': 'On Fire', 'intensity': 0.5},
        'positive': {'emoji': '😊', 'vibe': 'Good Vibes', 'intensity': 0.25},
        'neutral': {'emoji': '😐', 'vibe': 'Meh Energy', 'intensity': 0.0},
        'negative': {'emoji': '😞', 'vibe': 'Down Bad', 'intensity': -0.25},
        'very_negative': {'emoji': '💀', 'vibe': 'Big Oof', 'intensity': -0.5}
    }
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return True