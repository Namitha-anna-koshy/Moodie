# utils/__init__.py
"""
Utility functions for Sentiment Bot
"""

from .helpers import (
    clean_text, 
    format_results, 
    validate_text_input,
    format_sentiment_breakdown,
    save_results_to_json,
    load_results_from_json,
    get_emoji_sentiment_scale,
    batch_process_texts,
    print_colored_output,
    create_mood_summary,
    export_to_csv,
    interactive_mood_analyzer
)

__all__ = [
    'clean_text',
    'format_results', 
    'validate_text_input',
    'format_sentiment_breakdown',
    'save_results_to_json',
    'load_results_from_json',
    'get_emoji_sentiment_scale',
    'batch_process_texts',
    'print_colored_output',
    'create_mood_summary',
    'export_to_csv',
    'interactive_mood_analyzer'
]

__version__ = '1.0.0'
__author__ = 'Sentiment Bot Team'
__description__ = 'Utility functions for text processing, result formatting, and interactive features'