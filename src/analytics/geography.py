from typing import Dict, List
from datetime import datetime, timedelta

class GeographyAnalytics:
    def __init__(self, youtube_analytics):
        self.youtube_analytics = youtube_analytics

    def get_watch_time_by_country(self, video_id: str = None, days: int = 30) -> List[Dict]:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        filters = f"video=={video_id}" if video_id else ""
        
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="estimatedMinutesWatched,views",
            dimensions="country",
            filters=filters,
            sort="-estimatedMinutesWatched",
            maxResults=25
        ).execute()
        
        return [{
            'country': row[0],
            'watch_time_minutes': float(row[1]),
            'views': int(row[2])
        } for row in response.get('rows', [])]