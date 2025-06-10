# sass_quotes/__init__.py
"""
Sass Quote Generation Module
Generates sassy quotes based on sentiment analysis results
"""

from .sass_gen import SassQuoteGenerator, quick_sass

__all__ = ['SassQuoteGenerator', 'quick_sass']

__version__ = '1.0.0'
__author__ = 'Sentiment Bot Team'
__description__ = 'GPT-powered sassy quote generation based on mood analysis'