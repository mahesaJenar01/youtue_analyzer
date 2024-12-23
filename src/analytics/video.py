from typing import Dict, List, Any
from datetime import datetime, timedelta
from .demographics import DemographicsAnalytics
from .impressions import ImpressionAnalytics

class VideoAnalytics:
    def __init__(self, youtube, youtube_analytics):
        """Initialize with API clients."""
        self.youtube = youtube
        self.youtube_analytics = youtube_analytics
        self.demographics = DemographicsAnalytics(youtube_analytics)
        self.impressions = ImpressionAnalytics(youtube_analytics)

    def get_recent_videos(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """Get recent videos with basic stats."""
        all_videos = []
        page_token = None
        
        while len(all_videos) < max_results:
            # Get video IDs with pagination
            videos_response = self.youtube.search().list(
                part="snippet",
                forMine=True,
                maxResults=min(50, max_results - len(all_videos)),  # YouTube API limit is 50
                type="video",
                order="date",
                pageToken=page_token
            ).execute()
            
            if 'items' not in videos_response:
                break
                
            # Get video IDs from this page
            video_ids = [item['id']['videoId'] for item in videos_response['items']]
            
            # Get detailed stats for these videos
            stats_response = self.youtube.videos().list(
                part="statistics,snippet,contentDetails",
                id=','.join(video_ids)
            ).execute()
            
            # Process videos and add to list
            for item in stats_response.get('items', []):
                video_data = self._process_video_item(item)
                all_videos.append(video_data)
            
            # Check if there are more pages
            page_token = videos_response.get('nextPageToken')
            if not page_token:
                break
        
        return all_videos

    def _process_video_item(self, item: Dict) -> Dict:
        """Process a single video item."""
        video_id = item['id']
        stats = item['statistics']
        video_data = {
            'title': item['snippet']['title'],
            'id': video_id,
            'stats': {
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0))
            },
            'published_at': item['snippet']['publishedAt'],
            'duration': self._format_duration(item['contentDetails']['duration'])
        }
        
        # Add performance metrics
        perf_data = self._get_performance_metrics(video_id)
        if perf_data:
            video_data['performance'] = perf_data
            
        # Add impression metrics
        impression_data = self.impressions.get_impression_metrics(video_id)
        if impression_data:
            video_data['impressions'] = impression_data
        
        return video_data

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