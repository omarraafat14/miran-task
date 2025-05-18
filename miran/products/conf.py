DEFAULT_SIMILARITY_THRESHOLD = 0.3

SEARCH_WEIGHTS = {
    "name": "A",  # Highest priority
    "name_ar": "A",  # Highest priority for Arabic
    "description": "B",  # Medium priority
    "description_ar": "B",  # Medium priority for Arabic
    "brand__name": "C",  # Lower priority
    "category__name": "C",  # Lower priority
}
# Cache settings
SEARCH_QUERY_CACHE_TIMEOUT = 60 * 60
SEARCH_RESULTS_CACHE_TIMEOUT = 60 * 15
# Minimum query length for caching
MIN_QUERY_LENGTH_FOR_CACHE = 3
# Maximum number of cached queries to store
MAX_CACHED_QUERIES = 1000
