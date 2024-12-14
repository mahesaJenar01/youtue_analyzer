from typing import Dict, List, Any
from datetime import datetime, timedelta
from src.analytics.demographics import DemographicsAnalytics

class VideoAnalytics:
    def __init__(self, youtube, youtube_analytics):
        """Initialize with API clients."""
        self.youtube = youtube
        self.youtube_analytics = youtube_analytics
        self.demographics = DemographicsAnalytics(youtube_analytics)

    def get_recent_videos(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get recent videos with basic stats."""
        # Get video IDs
        videos_response = self.youtube.search().list(
            part="snippet",
            forMine=True,
            maxResults=max_results,
            type="video",
            order="date"
        ).execute()

        if 'items' not in videos_response:
            return []

        # Get detailed stats
        video_ids = [item['id']['videoId'] for item in videos_response['items']]
        stats_response = self.youtube.videos().list(
            part="statistics,snippet,contentDetails",
            id=','.join(video_ids)
        ).execute()

        videos_data = []
        for i, item in enumerate(stats_response.get('items', []), 1):
            stats = item['statistics']
            video_data = {
                'title': item['snippet']['title'],
                'id': item['id'],
                'stats': {
                    'views': int(stats.get('viewCount', 0)),
                    'likes': int(stats.get('likeCount', 0)),
                    'comments': int(stats.get('commentCount', 0))
                },
                'published_at': item['snippet']['publishedAt'],
                'duration': self._format_duration(item['contentDetails']['duration']),
                'demographics': self.demographics.get_video_demographics(item['id'])
            }
            # Add performance metrics
            perf_data = self._get_performance_metrics(item['id'])
            if perf_data:
                video_data['performance'] = perf_data
            
            videos_data.append(video_data)
        
        return videos_data

    def _get_performance_metrics(self, video_id: str) -> Dict[str, Any]:
        """Get performance metrics for a specific video."""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="estimatedMinutesWatched,averageViewDuration,averageViewPercentage",
            filters=f"video=={video_id}"
        ).execute()

        if 'rows' not in response:
            return {}

        metrics = response['rows'][0]
        return {
            'watch_time': round(float(metrics[0]), 2),
            'avg_view_duration': round(float(metrics[1]), 2),
            'avg_percentage_watched': round(float(metrics[2]), 2)
        }

    @staticmethod
    def _format_duration(duration: str) -> str:
        """Format video duration from ISO 8601 to readable format."""
        duration = duration.replace('PT', '')
        if 'H' in duration:
            hours, rest = duration.split('H')
            minutes = rest.split('M')[0] if 'M' in rest else '0'
            seconds = rest.split('M')[1].replace('S', '') if 'S' in rest else '0'
            return f"{hours}:{minutes.zfill(2)}:{seconds.zfill(2)}"
        elif 'M' in duration:
            minutes, seconds = duration.split('M')
            seconds = seconds.replace('S', '')
            return f"{minutes}:{seconds.zfill(2)}"
        else:
            seconds = duration.replace('S', '')
            return f"0:{seconds.zfill(2)}"
        
    def get_audience_retention(self, video_id: str) -> Dict[str, Any]:
        """Get audience retention data for a video."""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="relativeRetentionPerformance",
            dimensions="elapsedVideoTimeRatio",
            filters=f"video=={video_id}",
            sort="elapsedVideoTimeRatio"
        ).execute()
        
        if 'rows' not in response:
            return {}
            
        return {
            'retention_points': [
                {
                    'position': float(row[0]),
                    'retention_percentage': float(row[1])
                }
                for row in response['rows']
            ]
        }