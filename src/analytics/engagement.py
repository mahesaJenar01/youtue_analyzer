from typing import Dict, List, Any
from datetime import datetime, timedelta

class EngagementAnalytics:
    def __init__(self, youtube_analytics):
        self.youtube_analytics = youtube_analytics

    def get_video_engagement(self, video_id: str, days: int = 30) -> Dict[str, Any]:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views,estimatedMinutesWatched,averageViewDuration",
            filters=f"video=={video_id}"
        ).execute()
        
        if 'rows' not in response:
            return {}
            
        metrics = response['rows'][0]
        return {
            'views': int(metrics[0]),
            'watch_time': float(metrics[1]),
            'avg_view_duration': float(metrics[2])
        }

    def get_real_time_metrics(self, video_id: str) -> Dict[str, Any]:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views",
            dimensions="day",
            filters=f"video=={video_id}",
            sort="day"
        ).execute()
        
        return {
            'daily_views': [
                {
                    'date': row[0],
                    'views': int(row[1])
                }
                for row in response.get('rows', [])
            ]
        }

    def get_peak_viewing_times(self, days: int = 30) -> Dict[str, List]:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="estimatedMinutesWatched,views",
            dimensions="day",
            sort="-views"
        ).execute()
        
        if 'rows' not in response:
            return {'peak_times': []}
        
        return {
            'peak_times': [
                {
                    'date': row[0],
                    'watch_time': float(row[1]),
                    'views': int(row[2])
                }
                for row in response.get('rows', [])
            ]
        }