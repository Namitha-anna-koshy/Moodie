#!/usr/bin/env python3
"""
Sentiment Bot - Day 1 Implementation
Core sentiment analysis + sass quote generation
"""

import sys
import json
from config import Config
from sentiment.analyzer import SentimentAnalyzer
from sass_quotes.sass_gen import SassQuoteGenerator
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to test the sentiment analysis and sass quote generation"""
    try:
        # Validate configuration
        Config.validate_config()
        logger.info("Configuration validated successfully")
        
        # Initialize components
        sentiment_analyzer = SentimentAnalyzer()
        sass_generator = SassQuoteGenerator()
        
        print("🤖 SENTIMENT BOT - DAY 1 🤖")
        print("=" * 50)
        print("Enter text to analyze (or 'quit' to exit)")
        print("=" * 50)
        
        while True:
            # Get user input
            user_input = input("\n💭 Enter your text: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using Sentiment Bot!")
                break
            
            if not user_input:
                print("❌ Please enter some text to analyze")
                continue
            
            print("\n🔍 ANALYZING...")
            
            # Step 1: Analyze sentiment
            sentiment_result = sentiment_analyzer.analyze_comprehensive(user_input)
            
            # Step 2: Generate sass quote
            sass_result = sass_generator.generate_sass_quote(sentiment_result)
            
            # Display results
            print("\n" + "="*50)
            print("📊 SENTIMENT ANALYSIS RESULTS")
            print("="*50)
            print(f"📝 Text: {sentiment_result['text']}")
            print(f"🎯 Overall Score: {sentiment_result['combined_score']}")
            print(f"😊 Mood: {sentiment_result['analysis_summary']}")
            
            print(f"\n📈 Detailed Scores:")
            print(f"  • TextBlob: {sentiment_result['individual_scores']['textblob']['polarity']:.3f}")
            print(f"  • VADER: {sentiment_result['individual_scores']['vader']['compound']:.3f}")
            print(f"  • GPT: {sentiment_result['individual_scores']['gpt']['score']:.3f}")
            
            print("\n" + "="*50)
            print("💬 SASS QUOTE")
            print("="*50)
            print(f"🔥 {sass_result['formatted_output']}")
            print(f"📱 Generated via: {sass_result['generation_method'].upper()}")
            
            # Ask if user wants to see alternative quotes
            show_more = input("\n🎲 Want to see more sass quotes? (y/n): ").lower()
            if show_more in ['y', 'yes']:
                alternative_quotes = sass_generator.generate_multiple_quotes(sentiment_result, count=3)
                print("\n🎭 ALTERNATIVE SASS QUOTES:")
                for i, quote in enumerate(alternative_quotes[1:], 1):  # Skip the first one (already shown)
                    print(f"  {i}. {quote['formatted_output']}")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ An error occurred: {e}")

def test_mode():
    """Test mode with predefined texts"""
    test_texts = [
        "I'm having the best day ever! Everything is going perfectly!",
        "Today was okay, nothing special happened.",
        "I'm feeling really down and everything seems to be going wrong.",
        "Just got promoted at work! I can't believe it!",
        "I hate Mondays so much, everything is terrible."
    ]
    
    print("🧪 RUNNING TEST MODE")
    print("=" * 50)
    
    sentiment_analyzer = SentimentAnalyzer()
    sass_generator = SassQuoteGenerator()
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. Testing: '{text}'")
        
        # Analyze
        sentiment_result = sentiment_analyzer.analyze_comprehensive(text)
        sass_result = sass_generator.generate_sass_quote(sentiment_result)
        
        # Display
        print(f"   📊 {sentiment_result['analysis_summary']}")
        print(f"   💬 {sass_result['formatted_output']}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_mode()
    else:
        main()