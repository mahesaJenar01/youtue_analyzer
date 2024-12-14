import os
from typing import Dict, List
from googleapiclient.discovery import build
from src.utils.date_helper import DateHelper
from src.utils.formatters import DataFormatter

class GDocsReporter:
    def __init__(self, credentials):
        """Initialize Google Docs client."""
        self.docs_service = build('docs', 'v1', credentials=credentials)
        self.formatter = DataFormatter()
        self.date_helper = DateHelper()

    def create_report(self, channel_stats: Dict, period_stats: Dict, videos: List[Dict], 
                    peak_viewing: Dict, geo_data: Dict, trend_data: Dict = None) -> str:
        """Create or update analytics report in Google Docs."""
        document_id = os.getenv('YOUTUBE_ANALYSIS_DOCS_ID')
        
        if not document_id:
            raise ValueError("YOUTUBE_ANALYSIS_DOCS_ID not found in environment variables")
        
        self._write_report(document_id, channel_stats, period_stats, videos, peak_viewing, geo_data, trend_data)
        return document_id

    def _create_peak_viewing_request(self, peak_data: Dict) -> Dict:
        """Create peak viewing section request."""
        text = "Peak Viewing Times\n"
        peak_times = peak_data.get('peak_times', [])[:5]
        
        for day in peak_times:
            text += (
                f"Date: {day['date']} - "
                f"Views: {self.formatter.format_number(day['views'])} - "
                f"Watch Time: {self.formatter.format_time(day['watch_time'])}\n"
            )
        
        return {'insertText': {'text': text + '\n', 'endOfSegmentLocation': {}}}

    def _create_geography_request(self, geo_data: List[Dict]) -> Dict:
        """Create geographic distribution section request."""
        text = "Geographic Distribution\n"
        
        # Take top 5 countries
        top_countries = geo_data[:5]
        
        for country in top_countries:
            text += (
                f"{country['country']}: "
                f"{self.formatter.format_number(country['views'])} views "
                f"({self.formatter.format_time(country['watch_time_minutes'])} watch time)\n"
            )
        
        return {'insertText': {'text': text + '\n', 'endOfSegmentLocation': {}}}
    
    def _write_report(self, doc_id: str, channel_stats: Dict, period_stats: Dict, 
                        videos: List[Dict], peak_viewing: Dict, geo_data: Dict, 
                        trend_data: Dict = None):
        """Write formatted content to document."""
        # Instead of deleting content, replace entire document content
        requests = [
            {
                'replaceAllText': {
                    'containsText': {
                        'text': '.',
                        'matchCase': False
                    },
                    'replaceText': ''
                }
            }
        ]

        # Add new content
        requests.extend([
            self._create_header_request("YouTube Analytics Report"),
            self._create_channel_overview_request(channel_stats),
            self._create_period_stats_request(period_stats),
            self._create_videos_section_request(videos),
            self._create_peak_viewing_request(peak_viewing),
            self._create_geography_request(geo_data)
        ])

        # Add trend analysis if available
        if trend_data:
            requests.append(self._create_trend_analysis_request(trend_data))

        # Execute batch update
        self.docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

    def _create_header_request(self, text: str) -> Dict:
        """Create header formatting request."""
        return {
            'insertText': {
                'location': {'index': 1},
                'text': f'{text}\n\n'
            }
        }
    def _create_trend_analysis_request(self, trend_data: Dict) -> Dict:
        """Create trend analysis section request."""
        text = "\nPerformance Trends\n"
        
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
        
        return {'insertText': {'text': text, 'endOfSegmentLocation': {}}}

    def _create_channel_overview_request(self, stats: Dict) -> Dict:
        """Create channel overview section request."""
        text = (
            "Channel Overview\n"
            f"Subscribers: {self.formatter.format_number(stats.get('subscriber_count', 0))}\n"
            f"Total Views: {self.formatter.format_number(stats.get('view_count', 0))}\n"
            f"Total Videos: {self.formatter.format_number(stats.get('video_count', 0))}\n\n"
        )
        return {'insertText': {'text': text, 'endOfSegmentLocation': {}}}

    def _create_period_stats_request(self, stats: Dict) -> Dict:
        """Create period statistics section request."""
        text = (
            "Recent Performance\n"
            f"Views: {self.formatter.format_number(stats.get('total_views', 0))}\n"
            f"Watch Time: {self.formatter.format_time(stats.get('watch_time_hours', 0)*60)}\n"
            f"Average Daily Views: {self.formatter.format_number(stats.get('avg_daily_views', 0))}\n\n"
        )
        return {'insertText': {'text': text, 'endOfSegmentLocation': {}}}

    def _create_videos_section_request(self, videos: List[Dict]) -> Dict:
        """Create video details section request."""
        text = "Video Performance\n\n"
        for video in videos:
            text += self._format_video_details(video)
        return {'insertText': {'text': text, 'endOfSegmentLocation': {}}}

    def _format_video_details(self, video: Dict) -> str:
        """Format single video details."""
        stats = video['stats']
        text = (
            f"Title: {video['title']}\n"
            f"Views: {self.formatter.format_number(stats['views'])}\n"
            f"Likes: {self.formatter.format_number(stats['likes'])}\n"
        )
        
        if 'performance' in video:
            perf = video['performance']
            text += (
                f"Watch Time: {self.formatter.format_time(perf['watch_time'])}\n"
                f"Average View Duration: {perf['avg_view_duration']}s\n"
            )
        
        return text + "\n"