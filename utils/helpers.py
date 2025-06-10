import re
import string
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and preprocess text for sentiment analysis"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    
    # Remove @mentions and #hashtags (but keep the text)
    text = re.sub(r'[@#]([A-Za-z0-9_]+)', r'\1', text)
    
    # Remove excessive punctuation
    text = re.sub(r'[!]{2,}', '!', text)
    text = re.sub(r'[?]{2,}', '?', text)
    text = re.sub(r'[.]{3,}', '...', text)
    
    return text.strip()

def format_results(sentiment_result: Dict[str, Any], sass_result: Dict[str, Any]) -> str:
    """Format results for display"""
    output = []
    output.append("=" * 50)
    output.append("🤖 SENTIMENT BOT RESULTS")
    output.append("=" * 50)
    output.append(f"📝 Text: {sentiment_result['text']}")
    output.append(f"📊 Sentiment: {sentiment_result['analysis_summary']}")
    output.append(f"💬 Sass Quote: {sass_result['formatted_output']}")
    output.append("=" * 50)
    
    return "\n".join(output)

def validate_text_input(text: str, min_length: int = 1, max_length: int = 1000) -> bool:
    """Validate text input"""
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    if len(text) < min_length or len(text) > max_length:
        return False
        
    return True

def format_sentiment_breakdown(sentiment_result: Dict[str, Any]) -> str:
    """Format detailed sentiment breakdown"""
    breakdown = []
    breakdown.append("📊 DETAILED SENTIMENT BREAKDOWN")
    breakdown.append("-" * 40)
    
    # Individual scores
    individual = sentiment_result.get('individual_scores', {})
    
    if 'textblob' in individual:
        tb = individual['textblob']
        breakdown.append(f"🔤 TextBlob: {tb.get('polarity', 0):.3f} (subjectivity: {tb.get('subjectivity', 0):.3f})")
    
    if 'vader' in individual:
        vader = individual['vader']
        breakdown.append(f"⚡ VADER: {vader.get('compound', 0):.3f} (pos: {vader.get('pos', 0):.2f}, neg: {vader.get('neg', 0):.2f})")
    
    if 'gpt' in individual:
        gpt = individual['gpt']
        breakdown.append(f"🤖 GPT: {gpt.get('score', 0):.3f} ({gpt.get('emotion', 'neutral')})")
    
    breakdown.append(f"🎯 Combined: {sentiment_result.get('combined_score', 0):.3f}")
    breakdown.append("-" * 40)
    
    return "\n".join(breakdown)

def save_results_to_json(sentiment_result: Dict[str, Any], sass_result: Dict[str, Any], filename: Optional[str] = None) -> str:
    """Save results to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sentiment_analysis_{timestamp}.json"
    
    combined_results = {
        "timestamp": datetime.now().isoformat(),
        "sentiment_analysis": sentiment_result,
        "sass_quote": sass_result
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(combined_results, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to {filename}")
        return filename
    except Exception as e:
        logger.error(f"Failed to save results: {e}")
        return ""

def load_results_from_json(filename: str) -> Optional[Dict[str, Any]]:
    """Load results from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            results = json.load(f)
        logger.info(f"Results loaded from {filename}")
        return results
    except Exception as e:
        logger.error(f"Failed to load results: {e}")
        return None

def get_emoji_sentiment_scale() -> str:
    """Get visual emoji sentiment scale"""
    scale = [
        "💀 Very Negative (-1.0 to -0.5)",
        "😞 Negative (-0.5 to -0.1)",
        "😐 Neutral (-0.1 to 0.1)",
        "😊 Positive (0.1 to 0.5)",
        "🔥 Very Positive (0.5 to 1.0)"
    ]
    return "\n".join(scale)

def batch_process_texts(texts: List[str]) -> List[Dict[str, Any]]:
    """Process multiple texts at once"""
    from sentiment.analyzer import SentimentAnalyzer
    from sass_quotes.sass_gen import SassQuoteGenerator
    
    analyzer = SentimentAnalyzer()
    generator = SassQuoteGenerator()
    results = []
    
    logger.info(f"Processing {len(texts)} texts in batch")
    
    for i, text in enumerate(texts, 1):
        try:
            logger.info(f"Processing text {i}/{len(texts)}")
            sentiment_result = analyzer.analyze_comprehensive(text)
            sass_result = generator.generate_sass_quote(sentiment_result)
            
            results.append({
                'index': i,
                'text': text,
                'sentiment': sentiment_result,
                'sass_quote': sass_result
            })
        except Exception as e:
            logger.error(f"Error processing text {i}: {e}")
            results.append({
                'index': i,
                'text': text,
                'error': str(e)
            })
    
    return results

def print_colored_output(text: str, color: str = 'white') -> None:
    """Print colored text to terminal"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'end': '\033[0m'
    }
    
    color_code = colors.get(color.lower(), colors['white'])
    print(f"{color_code}{text}{colors['end']}")

def create_mood_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Create summary statistics from multiple analyses"""
    if not results:
        return {}
    
    mood_counts = {}
    total_score = 0
    valid_results = 0
    
    for result in results:
        if 'sentiment' in result:
            sentiment = result['sentiment']
            mood = sentiment.get('mood_category', 'neutral')
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
            total_score += sentiment.get('combined_score', 0)
            valid_results += 1
    
    avg_score = total_score / valid_results if valid_results > 0 else 0
    
    return {
        'total_texts': len(results),
        'valid_analyses': valid_results,
        'average_score': round(avg_score, 3),
        'mood_distribution': mood_counts,
        'dominant_mood': max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else 'neutral'
    }

def export_to_csv(results: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
    """Export results to CSV file"""
    import csv
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sentiment_results_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['text', 'sentiment_score', 'mood_category', 'mood_emoji', 'sass_quote']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in results:
                if 'sentiment' in result:
                    writer.writerow({
                        'text': result['text'],
                        'sentiment_score': result['sentiment'].get('combined_score', 0),
                        'mood_category': result['sentiment'].get('mood_category', 'neutral'),
                        'mood_emoji': result['sentiment'].get('mood_emoji', '😐'),
                        'sass_quote': result['sass_quote'].get('sass_quote', '') if 'sass_quote' in result else ''
                    })
        
        logger.info(f"Results exported to {filename}")
        return filename
    except Exception as e:
        logger.error(f"Failed to export to CSV: {e}")
        return ""

def interactive_mood_analyzer():
    """Interactive command-line mood analyzer"""
    from sentiment.analyzer import SentimentAnalyzer
    from sass_quotes.sass_gen import SassQuoteGenerator
    
    analyzer = SentimentAnalyzer()
    generator = SassQuoteGenerator()
    
    print_colored_output("🎭 INTERACTIVE MOOD ANALYZER", 'cyan')
    print_colored_output("=" * 50, 'cyan')
    print("Commands: 'help', 'scale', 'batch', 'save', 'quit'")
    print_colored_output("=" * 50, 'cyan')
    
    session_results = []
    
    while True:
        try:
            user_input = input("\n💭 Enter text (or command): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print_colored_output("👋 Goodbye!", 'green')
                break
            elif user_input.lower() == 'help':
                print("Available commands:")
                print("  help  - Show this help")
                print("  scale - Show emoji sentiment scale")
                print("  batch - Process multiple texts")
                print("  save  - Save session results")
                print("  quit  - Exit analyzer")
                continue
            elif user_input.lower() == 'scale':
                print_colored_output(get_emoji_sentiment_scale(), 'yellow')
                continue
            elif user_input.lower() == 'batch':
                print("Enter texts (one per line, empty line to finish):")
                batch_texts = []
                while True:
                    text = input("Text: ").strip()
                    if not text:
                        break
                    batch_texts.append(text)
                
                if batch_texts:
                    batch_results = batch_process_texts(batch_texts)
                    for result in batch_results:
                        if 'sentiment' in result:
                            print(f"{result['index']}. {result['sass_quote']['formatted_output']}")
                    session_results.extend(batch_results)
                continue
            elif user_input.lower() == 'save':
                if session_results:
                    filename = save_results_to_json({'session_results': session_results}, {})
                    print_colored_output(f"Session saved to {filename}", 'green')
                else:
                    print_colored_output("No results to save", 'yellow')
                continue
            
            if not validate_text_input(user_input):
                print_colored_output("❌ Please enter valid text", 'red')
                continue
            
            # Analyze sentiment
            sentiment_result = analyzer.analyze_comprehensive(user_input)
            sass_result = generator.generate_sass_quote(sentiment_result)
            
            # Display results
            print_colored_output(f"\n📊 {sentiment_result['analysis_summary']}", 'blue')
            print_colored_output(f"💬 {sass_result['formatted_output']}", 'purple')
            
            # Add to session results
            session_results.append({
                'text': user_input,
                'sentiment': sentiment_result,
                'sass_quote': sass_result,
                'timestamp': datetime.now().isoformat()
            })
            
        except KeyboardInterrupt:
            print_colored_output("\n👋 Goodbye!", 'green')
            break
        except Exception as e:
            print_colored_output(f"❌ Error: {e}", 'red')

if __name__ == "__main__":
    # Run interactive mode if called directly
    interactive_mood_analyzer()