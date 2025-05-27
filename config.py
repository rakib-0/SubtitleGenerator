# Translation Configuration Settings

class TranslationConfig:
    """Configuration settings for enhanced translation accuracy."""
    
    # Translation Services (in order of preference)
    TRANSLATION_SERVICES = ['google', 'mymemory']
    
    # Chunk size for text splitting (smaller = more accurate context, larger = faster)
    MAX_CHUNK_SIZE = 3000
    
    # Quality validation settings
    MIN_WORD_RATIO = 0.3  # Minimum translated words ratio compared to original
    MAX_WORD_RATIO = 3.0  # Maximum translated words ratio compared to original
    
    # Retry settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    RATE_LIMIT_DELAY = 0.1  # seconds between chunks
    
    # Language-specific settings
    LANGUAGE_SPECIFIC_SETTINGS = {
        'fa': {  # Persian/Farsi
            'punctuation_map': {'?': '؟', ',': '،'},
            'rtl': True,  # Right-to-left language
            'preserve_english_numbers': True
        },
        'ar': {  # Arabic
            'punctuation_map': {'?': '؟', ',': '،'},
            'rtl': True,
            'preserve_english_numbers': True
        },
        'he': {  # Hebrew
            'punctuation_map': {'?': '؟'},
            'rtl': True,
            'preserve_english_numbers': True
        },
        'ur': {  # Urdu
            'punctuation_map': {'?': '؟', ',': '،'},
            'rtl': True,
            'preserve_english_numbers': True
        }
    }
    
    # Advanced post-processing options
    POST_PROCESSING = {
        'fix_spacing': True,
        'fix_punctuation': True,
        'remove_duplicate_spaces': True,
        'capitalize_sentences': True,
        'fix_quote_spacing': True
    } 