from typing import Dict, Any
from datetime import datetime, timedelta
from googleapiclient.discovery import build

class ChannelAnalytics:
    def __init__(self, youtube, youtube_analytics):
        """Initialize with API clients."""
        self.youtube = youtube
        self.youtube_analytics = youtube_analytics

    def get_basic_stats(self) -> Dict[str, int]:
        """Get channel's basic statistics."""
        response = self.youtube.channels().list(
            part="statistics",
            mine=True
        ).execute()
        
        if 'items' not in response:
            return {}
            
        stats = response['items'][0]['statistics']
        return {
            'subscriber_count': int(stats['subscriberCount']),
            'view_count': int(stats['viewCount']),
            'video_count': int(stats['videoCount'])
        }

    def get_period_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics for specified time period."""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="estimatedMinutesWatched,views,averageViewDuration",
            dimensions="day",
            sort="day"
        ).execute()
        
        if 'rows' not in response:
            return {}
            
        rows = response['rows']
        total_views = sum(int(row[2]) for row in rows)
        total_watch_minutes = sum(float(row[1]) for row in rows)
        
        return {
            'total_views': total_views,
            'watch_time_hours': round(total_watch_minutes / 60, 2),
            'avg_daily_views': round(total_views / len(rows), 2),
            'daily_data': rows
        }