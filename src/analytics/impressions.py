from typing import Dict, Any
from datetime import datetime, timedelta

class ImpressionAnalytics:
    def __init__(self, youtube_analytics):
        self.youtube_analytics = youtube_analytics

    def get_impression_metrics(self, video_id: str, days: int = 30) -> Dict[str, Any]:
        """Get impression metrics for a video."""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            response = self.youtube_analytics.reports().query(
                ids="channel==MINE",
                startDate=start_date,
                endDate=end_date,
                metrics="views,likes",
                dimensions="video",
                filters=f"video=={video_id}"
            ).execute()
            
            # If no rows, return default metrics
            if 'rows' not in response or not response['rows']:
                return {
                    'impressions': 0,
                    'click_through_rate': 0.0
                }
                
            # If rows exist, process them
            metrics = response['rows'][0]
            views = int(metrics[1])
            likes = int(metrics[2])
            
            return {
                'impressions': views,  # Using views as impressions
                'click_through_rate': (likes / views * 100) if views > 0 else 0.0
            }
        except Exception as e:
            # Silently handle errors, returning default metrics
            return {
                'impressions': 0,
                'click_through_rate': 0.0
            }