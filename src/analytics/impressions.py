from typing import Dict, Any
from datetime import datetime, timedelta

class ImpressionAnalytics:
    def __init__(self, youtube_analytics):
        self.youtube_analytics = youtube_analytics

    def get_impression_metrics(self, video_id: str, days: int = 30) -> Dict[str, Any]:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views,estimatedMinutesWatched",
            filters=f"video=={video_id}"
        ).execute()
        
        if 'rows' not in response:
            return {}
            
        metrics = response['rows'][0]
        return {
            'views': int(metrics[0]),
            'watch_time': float(metrics[1])
        }