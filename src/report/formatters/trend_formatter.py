from typing import Dict
from .base_formatter import BaseDocFormatter

class TrendFormatter(BaseDocFormatter):
    def format_trends(self, trend_data: Dict) -> Dict:
        """Format trend analysis section."""
        text = "Performance Trends\n"
        
        # Views Trend
        views_trend = trend_data.get('performance_trends', {}).get('views', {})
        text += f"Views Trend: {self.formatter.format_percentage(views_trend.get('total_trend', 0))} change\n"
        
        # Engagement Trend
        engagement_trend = trend_data.get('performance_trends', {}).get('engagement_rate', {})
        text += f"Average Engagement: {self.formatter.format_percentage(engagement_trend.get('average_engagement', 0))}\n"
        
        # Top Performing Videos
        content_insights = trend_data.get('content_insights', {})
        text += "\nTop Performing Videos:\n"
        top_videos = content_insights.get('best_performing_videos', [])
        for video in top_videos[:3]:
            text += f"- {video['title']}: {self.formatter.format_number(video['stats']['views'])} views\n"
        
        return self.create_section_request(text)