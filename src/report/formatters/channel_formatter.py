from typing import Dict
from .base_formatter import BaseDocFormatter

class ChannelFormatter(BaseDocFormatter):
    def format_overview(self, stats: Dict) -> Dict:
        """Format channel overview section."""
        text = (
            "Channel Overview\n"
            f"Subscribers: {self.formatter.format_number(stats.get('subscriber_count', 0))}\n"
            f"Total Views: {self.formatter.format_number(stats.get('view_count', 0))}\n"
            f"Total Videos: {self.formatter.format_number(stats.get('video_count', 0))}\n"
        )
        return self.create_section_request(text)

    def format_period_stats(self, stats: Dict) -> Dict:
        """Format period statistics section."""
        text = (
            "Recent Performance\n"
            f"Views: {self.formatter.format_number(stats.get('total_views', 0))}\n"
            f"Watch Time: {self.formatter.format_time(stats.get('watch_time_hours', 0)*60)}\n"
            f"Average Daily Views: {self.formatter.format_number(stats.get('avg_daily_views', 0))}\n"
        )
        return self.create_section_request(text)