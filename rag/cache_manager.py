"""Query result caching for performance optimization"""

from functools import lru_cache
import hashlib
from typing import Dict, Any

class CacheManager:
    """Manage query caching with TTL support"""
    
    def __init__(self, max_cache_size: int = 1000):
        self.max_cache_size = max_cache_size
        self.cache: Dict[str, Any] = {}
        self.hit_count = 0
        self.miss_count = 0
    
    @staticmethod
    def generate_cache_key(query: str, user_role: str, n_results: int) -> str:
        """Generate cache key from query parameters"""
        cache_input = f"{query}|{user_role}|{n_results}".lower().strip()
        return hashlib.md5(cache_input.encode()).hexdigest()
    
    def get(self, query: str, user_role: str, n_results: int) -> Any:
        """Get cached result if exists"""
        key = self.generate_cache_key(query, user_role, n_results)
        if key in self.cache:
            self.hit_count += 1
            return self.cache[key]
        self.miss_count += 1
        return None
    
    def set(self, query: str, user_role: str, n_results: int, result: Any) -> None:
        """Cache a result"""
        key = self.generate_cache_key(query, user_role, n_results)
        
        # Simple LRU: remove oldest if at capacity
        if len(self.cache) >= self.max_cache_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        self.cache[key] = result
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        total = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total * 100) if total > 0 else 0
        return {
            "hits": self.hit_count,
            "misses": self.miss_count,
            "hit_rate": f"{hit_rate:.1f}%",
            "cache_size": len(self.cache)
        }


# Global cache instance
_cache_manager = CacheManager()

def get_cache_manager() -> CacheManager:
    """Get global cache manager instance"""
    return _cache_manager
