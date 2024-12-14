from typing import Dict, List, Any
from src.utils.formatters import DataFormatter
from src.utils.date_helper import DateHelper

class ConsoleReporter:
    def __init__(self):
        self.formatter = DataFormatter()
        self.date_helper = DateHelper()

    def print_channel_overview(self, stats: Dict[str, int]) -> None:
        """Print channel overview stats."""
        print("\n=== Channel Overview ===")
        print(f"Subscribers: {self.formatter.format_number(stats.get('subscriber_count', 0))}")
        print(f"Total Views: {self.formatter.format_number(stats.get('view_count', 0))}")
        print(f"Total Videos: {self.formatter.format_number(stats.get('video_count', 0))}")

    def print_period_analytics(self, data: Dict[str, Any], days: int) -> None:
        """Print period analytics."""
        print(f"\n=== Analytics Overview (Last {days} days) ===")
        print(f"Total Views: {self.formatter.format_number(data['total_views'])}")
        print(f"Watch Time: {self.formatter.format_time(data['watch_time_hours']*60)}")
        print(f"Avg Daily Views: {self.formatter.format_number(data['avg_daily_views'])}")

    def print_video_details(self, videos: List[Dict[str, Any]]) -> None:
        """Print video performance details."""
        print("\n=== Video Performance ===")
        for video in videos:
            self._print_single_video(video)

    def _print_single_video(self, video: Dict[str, Any]) -> None:
        """Print individual video details."""
        print(f"\n{video['title']}")
        stats = video['stats']
        
        print("Basic Metrics:")
        print(f"- Views: {self.formatter.format_number(stats['views'])}")
        print(f"- Likes: {self.formatter.format_number(stats['likes'])}")
        
        if stats['views'] > 0:
            engagement = (stats['likes'] / stats['views']) * 100
            print(f"- Engagement: {self.formatter.format_percentage(engagement)}")
            
        if 'performance' in video:
            perf = video['performance']
            print("\nEngagement Metrics:")
            print(f"- Watch Time: {self.formatter.format_time(perf['watch_time'])}")
            print(f"- Avg View Duration: {perf['avg_view_duration']}s")
            print(f"- Avg Watched: {self.formatter.format_percentage(perf['avg_percentage_watched'])}")
            
        if 'demographics' in video:
            demo = video['demographics']
            if demo.get('audience'):
                print("\nAudience Demographics:")
                for group in demo['audience']:
                    print(f"- {group['age_group']} {group['gender']}: {self.formatter.format_percentage(group['percentage'])}")
                    
            if demo.get('traffic'):
                print("\nTop Traffic Sources:")
                for source in demo['traffic'][:3]:
                    print(f"- {source['source']}: {self.formatter.format_number(source['views'])} views")

    def print_peak_viewing(self, peak_data: Dict[str, List]) -> None:
        print("\n=== Peak Viewing Days ===")
        for day in peak_data.get('peak_times', [])[:5]:
            print(f"Date: {day['date']} - Views: {self.formatter.format_number(day['views'])} - "
                f"Watch Time: {self.formatter.format_time(day['watch_time'])}")

    def print_geography(self, geo_data: Dict) -> None:
        """Print geographical distribution data."""
        print("\n=== Geographic Distribution ===")
        for country in geo_data[:5]:  # Show top 5 countries
            print(f"{country['country']}: {self.formatter.format_number(country['views'])} views "
                f"({self.formatter.format_time(country['watch_time_minutes'])} watch time)")
            
    def print_trend_analysis(self, trend_data: Dict) -> None:
        """Print comprehensive trend analysis."""
        print("\n=== Performance Trends ===")
        
        # Views Trend
        views_trend = trend_data.get('performance_trends', {}).get('views', {})
        print("Views Trend:")
        print(f"- Total Change: {self.formatter.format_percentage(views_trend.get('total_trend', 0))}")
        
        # Engagement Trend
        engagement_trend = trend_data.get('performance_trends', {}).get('engagement_rate', {})
        print("\nEngagement Trend:")
        print(f"- Average Engagement: {self.formatter.format_percentage(engagement_trend.get('average_engagement', 0))}")
        print(f"- Engagement Change: {self.formatter.format_percentage(engagement_trend.get('trend', 0))}")
        
        # Top/Bottom Performing Videos
        content_insights = trend_data.get('content_insights', {})
        print("\nTop Performing Videos:")
        top_videos = content_insights.get('best_performing_videos', [])
        for video in top_videos[:3]:
            print(f"- {video['title']}: {self.formatter.format_number(video['stats']['views'])} views")
        
        print("\nWorst Performing Videos:")
        bottom_videos = content_insights.get('worst_performing_videos', [])
        for video in bottom_videos[:3]:
            print(f"- {video['title']}: {self.formatter.format_number(video['stats']['views'])} views")