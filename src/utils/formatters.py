from typing import Dict, Any, Union

class DataFormatter:
    @staticmethod
    def format_number(value: Union[int, float]) -> str:
        """Format numbers with thousands separator."""
        return f"{value:,}"

    @staticmethod
    def format_percentage(value: float, decimal_places: int = 1) -> str:
        """Format percentage with specified decimal places."""
        return f"{round(value, decimal_places)}%"

    @staticmethod
    def format_time(minutes: float) -> str:
        """Format minutes into hours and minutes."""
        if minutes == 0:
            return "0m"
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return f"{hours}h {mins:02d}m" if hours > 0 else f"{mins}m"

    @staticmethod
    def format_traffic_source(source: str) -> str:
        """Format traffic source names."""
        replacements = {
            'EXTERNAL': 'External Links',
            'ADVERTISING': 'Advertising',
            'PLAYLIST': 'Playlists',
            'NOTIFICATION': 'Notifications',
            'BROWSE': 'Browse',
            'SEARCH': 'Search',
            'SUGGESTED': 'Suggested',
            'END_SCREEN': 'End Screen',
            'CHANNEL': 'Channel',
            'SHORTS': 'Shorts',
            'OTHER': 'Other',
            'NO_LINK_OTHER': 'Other',
            'YT_SEARCH': 'Search',
            'YT_CHANNEL': 'Channel',
            'YT_OTHER_PAGE': 'Other Pages'
        }
        return replacements.get(source, source.title())