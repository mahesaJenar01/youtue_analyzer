import os
from typing import Dict, Any

class Settings:
    DEFAULT_CONFIG = {
        'credentials_path': 'credentials.json',
        'token_path': 'token.pickle',
        'report_period_days': 30,
        'max_videos': 50,
        'log_level': 'INFO'
    }

    @classmethod
    def load(cls) -> Dict[str, Any]:
        """Load settings from environment or defaults."""
        return {
            'credentials_path': os.getenv('YT_CREDENTIALS_PATH', cls.DEFAULT_CONFIG['credentials_path']),
            'token_path': os.getenv('YT_TOKEN_PATH', cls.DEFAULT_CONFIG['token_path']),
            'report_period_days': int(os.getenv('YT_REPORT_PERIOD', cls.DEFAULT_CONFIG['report_period_days'])),
            'max_videos': int(os.getenv('YT_MAX_VIDEOS', cls.DEFAULT_CONFIG['max_videos'])),
            'log_level': os.getenv('YT_LOG_LEVEL', cls.DEFAULT_CONFIG['log_level'])
        }