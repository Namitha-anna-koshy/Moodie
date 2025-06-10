# sentiment/__init__.py
"""
Sentiment Analysis Module
Provides comprehensive sentiment analysis using TextBlob, VADER, and GPT
"""

from .analyzer import SentimentAnalyzer, quick_analyze

__all__ = ['SentimentAnalyzer', 'quick_analyze']

__version__ = '1.0.0'
__author__ = 'Sentiment Bot Team'
__description__ = 'Multi-layered sentiment analysis with TextBlob, VADER, and GPT'