"""
Information Retrieval Engine
Search and retrieve historical data from the system
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class IREngine:
    """
    Information Retrieval Engine for searching system data
    Implements keyword search, ranking, and filtering
    """
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager
        self.search_cache = {}
        self.cache_timeout = 300  # 5 minutes
        
        logger.info("✓ Information Retrieval Engine initialized")
    
    def search(self, query: str, filters: Dict[str, Any] = None, 
               limit: int = 50) -> Dict[str, Any]:
        """
        Main search function
        
        Args:
            query: Search query string
            filters: Optional filters (date_range, city, type, etc.)
            limit: Maximum results to return
        """
        try:
            # Check cache first
            cache_key = f"{query}_{str(filters)}_{limit}"
            if cache_key in self.search_cache:
                cached = self.search_cache[cache_key]
                if (datetime.now() - cached['timestamp']).seconds < self.cache_timeout:
                    logger.info(f"Cache hit for query: {query}")
                    return cached['results']
            
            # Preprocess query
            processed_query = self._preprocess_query(query)
            keywords = self._extract_keywords(processed_query)
            
            # Search in different data sources
            results = {
                'query': query,
                'keywords': keywords,
                'total_results': 0,
                'results': [],
                'filters_applied': filters or {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Search weather data
            if self._should_search_type('weather', filters):
                weather_results = self._search_weather(keywords, filters, limit)
                results['results'].extend(weather_results)
            
            # Search demand data
            if self._should_search_type('demand', filters):
                demand_results = self._search_demand(keywords, filters, limit)
                results['results'].extend(demand_results)
            
            # Search grid data
            if self._should_search_type('grid', filters):
                grid_results = self._search_grid(keywords, filters, limit)
                results['results'].extend(grid_results)
            
            # Search AI decisions
            if self._should_search_type('decisions', filters):
                decision_results = self._search_decisions(keywords, filters, limit)
                results['results'].extend(decision_results)
            
            # Rank and sort results
            results['results'] = self._rank_results(results['results'], keywords)[:limit]
            results['total_results'] = len(results['results'])
            
            # Cache results
            self.search_cache[cache_key] = {
                'results': results,
                'timestamp': datetime.now()
            }
            
            logger.info(f"Search completed: '{query}' - {results['total_results']} results")
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                'query': query,
                'error': str(e),
                'total_results': 0,
                'results': []
            }
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess search query"""
        # Convert to lowercase
        query = query.lower()
        
        # Remove special characters
        query = re.sub(r'[^\w\s]', ' ', query)
        
        # Remove extra whitespace
        query = ' '.join(query.split())
        
        return query
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from query"""
        # Remove stop words
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but',
            'in', 'with', 'to', 'for', 'of', 'as', 'by', 'from', 'what', 'when',
            'where', 'how', 'why', 'this', 'that', 'these', 'those'
        }
        
        words = query.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    def _should_search_type(self, data_type: str, filters: Optional[Dict]) -> bool:
        """Check if should search this data type based on filters"""
        if not filters or 'type' not in filters:
            return True
        
        filter_type = filters['type']
        if filter_type == 'all':
            return True
        
        return filter_type == data_type
    
    def _search_weather(self, keywords: List[str], filters: Optional[Dict], 
                       limit: int) -> List[Dict]:
        """Search weather data"""
        results = []
        
        if not self.db_manager:
            return results
        
        try:
            # Get date range
            days = filters.get('days', 7) if filters else 7
            city = filters.get('city') if filters else None
            
            # Get weather history
            if city:
                weather_records = self.db_manager.get_weather_history(city, days)
            else:
                weather_records = self.db_manager.get_weather_history('Colombo', days)
            
            # Filter and score results
            for record in weather_records:
                score = self._calculate_relevance_score(record, keywords)
                if score > 0:
                    results.append({
                        'type': 'weather',
                        'score': score,
                        'data': record,
                        'summary': f"Weather in {record['city']}: {record['temperature']}°C, Renewable Score: {record['renewable_score']:.1f}%"
                    })
            
        except Exception as e:
            logger.error(f"Weather search failed: {e}")
        
        return results
    
    def _search_demand(self, keywords: List[str], filters: Optional[Dict], 
                      limit: int) -> List[Dict]:
        """Search demand data"""
        results = []
        
        if not self.db_manager:
            return results
        
        try:
            days = filters.get('days', 7) if filters else 7
            demand_records = self.db_manager.get_demand_history(days)
            
            for record in demand_records:
                score = self._calculate_relevance_score(record, keywords)
                if score > 0:
                    results.append({
                        'type': 'demand',
                        'score': score,
                        'data': record,
                        'summary': f"Demand: {record['predicted_demand_mw']} MW (Confidence: {record['confidence']:.0%})"
                    })
            
        except Exception as e:
            logger.error(f"Demand search failed: {e}")
        
        return results
    
    def _search_grid(self, keywords: List[str], filters: Optional[Dict], 
                    limit: int) -> List[Dict]:
        """Search grid data"""
        results = []
        
        if not self.db_manager:
            return results
        
        try:
            days = filters.get('days', 7) if filters else 7
            grid_records = self.db_manager.get_grid_history(days)
            
            for record in grid_records:
                score = self._calculate_relevance_score(record, keywords)
                if score > 0:
                    results.append({
                        'type': 'grid',
                        'score': score,
                        'data': record,
                        'summary': f"Grid: {record['grid_balance']}, Renewable: {record['renewable_percentage']:.1f}%, Efficiency: {record['efficiency']:.1f}%"
                    })
            
        except Exception as e:
            logger.error(f"Grid search failed: {e}")
        
        return results
    
    def _search_decisions(self, keywords: List[str], filters: Optional[Dict], 
                         limit: int) -> List[Dict]:
        """Search AI decisions"""
        results = []
        
        if not self.db_manager:
            return results
        
        try:
            days = filters.get('days', 7) if filters else 7
            agent_id = filters.get('agent_id') if filters else None
            
            decision_records = self.db_manager.get_decision_history(agent_id, days)
            
            for record in decision_records:
                # Search in decision text
                decision_text = str(record.get('decision', '')).lower()
                score = sum(1 for keyword in keywords if keyword in decision_text)
                
                if score > 0:
                    results.append({
                        'type': 'decision',
                        'score': score * 2,  # Boost decision scores
                        'data': record,
                        'summary': f"Decision by {record['agent_id']}: {record['decision'][:100]}..."
                    })
            
        except Exception as e:
            logger.error(f"Decision search failed: {e}")
        
        return results
    
    def _calculate_relevance_score(self, record: Dict, keywords: List[str]) -> float:
        """Calculate relevance score for a record"""
        score = 0
        record_text = str(record).lower()
        
        # Count keyword matches
        for keyword in keywords:
            if keyword in record_text:
                score += 1
        
        # Boost for exact phrase match
        if all(keyword in record_text for keyword in keywords):
            score += len(keywords)
        
        # Boost for recent records
        if 'timestamp' in record:
            try:
                timestamp = datetime.fromisoformat(record['timestamp'])
                age_hours = (datetime.now() - timestamp).total_seconds() / 3600
                
                if age_hours < 24:
                    score += 2
                elif age_hours < 168:  # 1 week
                    score += 1
            except:
                pass
        
        return score
    
    def _rank_results(self, results: List[Dict], keywords: List[str]) -> List[Dict]:
        """Rank results by relevance score"""
        return sorted(results, key=lambda x: x['score'], reverse=True)
    
    def get_suggestions(self, partial_query: str, limit: int = 5) -> List[str]:
        """Get search suggestions based on partial query"""
        suggestions = []
        
        # Common search terms
        common_terms = [
            'weather forecast',
            'renewable energy',
            'grid balance',
            'demand prediction',
            'solar potential',
            'wind generation',
            'carbon intensity',
            'energy efficiency',
            'peak demand',
            'surplus energy'
        ]
        
        partial_lower = partial_query.lower()
        
        for term in common_terms:
            if partial_lower in term or term.startswith(partial_lower):
                suggestions.append(term)
        
        return suggestions[:limit]
    
    def get_trending_searches(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get trending search topics"""
        # This would track actual searches in a real system
        # For now, return common topics
        return [
            {'topic': 'renewable energy', 'count': 45},
            {'topic': 'grid balance', 'count': 32},
            {'topic': 'weather forecast', 'count': 28},
            {'topic': 'demand prediction', 'count': 21},
            {'topic': 'solar potential', 'count': 18}
        ]
    
    def clear_cache(self):
        """Clear search cache"""
        self.search_cache.clear()
        logger.info("Search cache cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get IR engine status"""
        return {
            'cache_size': len(self.search_cache),
            'cache_timeout': self.cache_timeout,
            'db_connected': self.db_manager is not None,
            'capabilities': [
                'keyword_search',
                'multi_source_search',
                'relevance_ranking',
                'date_filtering',
                'type_filtering',
                'search_suggestions',
                'result_caching'
            ]
        }
