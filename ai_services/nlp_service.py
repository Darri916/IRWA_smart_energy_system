"""
NLP Service for text processing and analysis
Includes summarization, sentiment analysis, and entity extraction
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Try to import NLP libraries
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    import spacy
    try:
        nlp_model = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
    except OSError:
        SPACY_AVAILABLE = False
        nlp_model = None
except ImportError:
    SPACY_AVAILABLE = False
    nlp_model = None

logger = logging.getLogger(__name__)


class NLPService:
    """
    Natural Language Processing service for energy system text analysis
    """
    
    def __init__(self):
        self.textblob_available = TEXTBLOB_AVAILABLE
        self.spacy_available = SPACY_AVAILABLE
        
        if TEXTBLOB_AVAILABLE:
            logger.info("✓ TextBlob NLP initialized")
        if SPACY_AVAILABLE:
            logger.info("✓ Spacy NLP initialized")
        
        if not TEXTBLOB_AVAILABLE and not SPACY_AVAILABLE:
            logger.warning("⚠️  Advanced NLP libraries not available - using basic processing")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text (cities, numbers, dates, etc.)
        """
        entities = {
            'cities': [],
            'numbers': [],
            'dates': [],
            'energy_terms': [],
            'weather_terms': []
        }
        
        try:
            if SPACY_AVAILABLE and nlp_model:
                # Use Spacy for entity extraction
                doc = nlp_model(text)
                
                for ent in doc.ents:
                    if ent.label_ == "GPE":  # Geopolitical entity (cities)
                        entities['cities'].append(ent.text)
                    elif ent.label_ == "DATE":
                        entities['dates'].append(ent.text)
                    elif ent.label_ in ["CARDINAL", "QUANTITY"]:
                        entities['numbers'].append(ent.text)
            
            # Extract energy-related terms (rule-based)
            energy_keywords = [
                'solar', 'wind', 'renewable', 'fossil', 'coal', 'gas', 'nuclear',
                'grid', 'power', 'energy', 'electricity', 'generation', 'demand',
                'MW', 'GW', 'kWh', 'capacity', 'storage', 'battery'
            ]
            
            weather_keywords = [
                'temperature', 'wind', 'cloud', 'rain', 'sun', 'weather',
                'forecast', 'climate', 'humidity', 'pressure'
            ]
            
            text_lower = text.lower()
            
            for keyword in energy_keywords:
                if keyword in text_lower:
                    entities['energy_terms'].append(keyword)
            
            for keyword in weather_keywords:
                if keyword in text_lower:
                    entities['weather_terms'].append(keyword)
            
            # Extract numbers with units
            number_patterns = re.findall(r'\d+\.?\d*\s*(?:MW|GW|kWh|°C|m/s|%)', text)
            entities['numbers'].extend(number_patterns)
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
        
        return entities
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text (positive/negative/neutral)
        Useful for analyzing user feedback or reports
        """
        try:
            if TEXTBLOB_AVAILABLE:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity  # -1 to 1
                subjectivity = blob.sentiment.subjectivity  # 0 to 1
                
                # Classify sentiment
                if polarity > 0.1:
                    sentiment = "positive"
                elif polarity < -0.1:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                
                return {
                    'sentiment': sentiment,
                    'polarity': round(polarity, 3),
                    'subjectivity': round(subjectivity, 3),
                    'confidence': abs(polarity)
                }
            else:
                # Fallback: simple keyword-based sentiment
                positive_words = ['good', 'excellent', 'optimal', 'efficient', 'stable', 'surplus']
                negative_words = ['poor', 'deficit', 'critical', 'warning', 'shortage', 'unstable']
                
                text_lower = text.lower()
                pos_count = sum(1 for word in positive_words if word in text_lower)
                neg_count = sum(1 for word in negative_words if word in text_lower)
                
                if pos_count > neg_count:
                    sentiment = "positive"
                    polarity = 0.5
                elif neg_count > pos_count:
                    sentiment = "negative"
                    polarity = -0.5
                else:
                    sentiment = "neutral"
                    polarity = 0.0
                
                return {
                    'sentiment': sentiment,
                    'polarity': polarity,
                    'subjectivity': 0.5,
                    'confidence': 0.5
                }
                
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                'sentiment': 'neutral',
                'polarity': 0.0,
                'subjectivity': 0.0,
                'confidence': 0.0
            }
    
    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """
        Create extractive summary of text
        """
        try:
            # Split into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
            
            if len(sentences) <= max_sentences:
                return text
            
            # Score sentences by importance (simple heuristic)
            scored_sentences = []
            
            # Keywords that indicate importance
            important_keywords = [
                'critical', 'important', 'significant', 'major', 'key',
                'recommend', 'should', 'must', 'alert', 'warning',
                'optimal', 'efficient', 'balance', 'generation', 'demand'
            ]
            
            for sentence in sentences:
                score = 0
                sentence_lower = sentence.lower()
                
                # Score based on keywords
                for keyword in important_keywords:
                    if keyword in sentence_lower:
                        score += 2
                
                # Score based on length (prefer medium-length sentences)
                word_count = len(sentence.split())
                if 10 <= word_count <= 25:
                    score += 1
                
                # Score based on numbers/data (indicates factual content)
                if re.search(r'\d+', sentence):
                    score += 1
                
                scored_sentences.append((score, sentence))
            
            # Sort by score and take top sentences
            scored_sentences.sort(reverse=True, key=lambda x: x[0])
            top_sentences = [s[1] for s in scored_sentences[:max_sentences]]
            
            # Return in original order
            summary_sentences = []
            for sentence in sentences:
                if sentence in top_sentences:
                    summary_sentences.append(sentence)
            
            return '. '.join(summary_sentences) + '.'
            
        except Exception as e:
            logger.error(f"Text summarization failed: {e}")
            # Return first few sentences as fallback
            sentences = text.split('.')[:max_sentences]
            return '. '.join(sentences) + '.'
    
    def extract_key_metrics(self, text: str) -> Dict[str, List[str]]:
        """
        Extract key energy metrics from text
        """
        metrics = {
            'power_values': [],
            'temperatures': [],
            'percentages': [],
            'timestamps': []
        }
        
        try:
            # Extract power values (MW, GW, kWh)
            power_pattern = r'(\d+\.?\d*)\s*(MW|GW|kWh|MWh)'
            metrics['power_values'] = re.findall(power_pattern, text)
            
            # Extract temperatures
            temp_pattern = r'(\d+\.?\d*)\s*°C'
            metrics['temperatures'] = re.findall(temp_pattern, text)
            
            # Extract percentages
            percentage_pattern = r'(\d+\.?\d*)\s*%'
            metrics['percentages'] = re.findall(percentage_pattern, text)
            
            # Extract dates/times
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{2}:\d{2}:\d{2}'   # HH:MM:SS
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, text)
                metrics['timestamps'].extend(matches)
            
        except Exception as e:
            logger.error(f"Metric extraction failed: {e}")
        
        return metrics
    
    def classify_intent(self, question: str) -> Dict[str, Any]:
        """
        Classify user question intent for better routing
        """
        question_lower = question.lower()
        
        intents = {
            'weather_query': ['weather', 'temperature', 'wind', 'rain', 'forecast', 'climate'],
            'demand_query': ['demand', 'consumption', 'usage', 'load', 'peak'],
            'renewable_query': ['renewable', 'solar', 'wind', 'green', 'clean'],
            'grid_query': ['grid', 'balance', 'stability', 'frequency', 'voltage'],
            'optimization': ['optimize', 'improve', 'enhance', 'recommend', 'suggest'],
            'status_query': ['status', 'current', 'now', 'today'],
            'forecast_query': ['forecast', 'predict', 'future', 'tomorrow', 'next']
        }
        
        detected_intents = []
        intent_scores = {}
        
        for intent, keywords in intents.items():
            score = sum(1 for keyword in keywords if keyword in question_lower)
            if score > 0:
                detected_intents.append(intent)
                intent_scores[intent] = score
        
        # Determine primary intent
        if intent_scores:
            primary_intent = max(intent_scores, key=intent_scores.get)
        else:
            primary_intent = 'general_query'
        
        return {
            'primary_intent': primary_intent,
            'all_intents': detected_intents,
            'confidence': min(1.0, max(intent_scores.values()) / 3) if intent_scores else 0.3
        }
    
    def generate_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract top keywords from text
        """
        try:
            # Remove common stop words
            stop_words = set([
                'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
                'in', 'with', 'to', 'for', 'of', 'as', 'by', 'this', 'that'
            ])
            
            # Tokenize and count
            words = re.findall(r'\b[a-z]{3,}\b', text.lower())
            words = [w for w in words if w not in stop_words]
            
            # Count frequency
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            
            return [word for word, freq in sorted_words[:top_n]]
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {e}")
            return []
    
    def get_status(self) -> Dict[str, Any]:
        """Get NLP service status"""
        return {
            'textblob_available': self.textblob_available,
            'spacy_available': self.spacy_available,
            'capabilities': [
                'entity_extraction',
                'sentiment_analysis',
                'text_summarization',
                'metric_extraction',
                'intent_classification',
                'keyword_generation'
            ]
        }
