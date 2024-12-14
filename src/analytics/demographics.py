from typing import Dict, List, Any
from datetime import datetime, timedelta

class DemographicsAnalytics:
    def __init__(self, youtube_analytics):
        """Initialize with YouTube Analytics API client."""
        self.youtube_analytics = youtube_analytics

    def get_video_demographics(self, video_id: str, days: int = 30) -> Dict[str, Any]:
        """Get demographic data for specific video."""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

        demographics = self._get_audience_demographics(video_id, start_date, end_date)
        traffic_sources = self._get_traffic_sources(video_id, start_date, end_date)

        return {
            'audience': demographics,
            'traffic': traffic_sources
        }

    def _get_audience_demographics(self, video_id: str, start_date: str, end_date: str) -> List[Dict]:
        """Get age and gender demographics."""
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="viewerPercentage",
            dimensions="ageGroup,gender",
            filters=f"video=={video_id}"
        ).execute()

        if 'rows' not in response:
            return []

        return [
            {
                'age_group': row[0].replace('age', ''),
                'gender': 'Female' if row[1] == 'female' else 'Male',
                'percentage': round(float(row[2]), 2)
            }
            for row in response['rows']
        ]

    def _get_traffic_sources(self, video_id: str, start_date: str, end_date: str) -> List[Dict]:
        """Get top traffic sources."""
        response = self.youtube_analytics.reports().query(
            ids="channel==MINE",
            startDate=start_date,
            endDate=end_date,
            metrics="views",
            dimensions="insightTrafficSourceType",
            filters=f"video=={video_id}",
            sort="-views",
            maxResults=5
        ).execute()

        if 'rows' not in response:
            return []

        return [
            {
                'source': self._format_source_name(row[0]),
                'views': int(row[1])
            }
            for row in response['rows']
        ]

    def _format_source_name(self, source: str) -> str:
        """Format traffic source name for readability."""
        source_map = {
            'SHORTS': 'Shorts',
            'CHANNEL': 'Channel',
            'SEARCH': 'Search',
            'OTHER_PAGE': 'Other',
            'NO_LINK_OTHER': 'Other',
            'SUGGESTED': 'Suggested'
        }
        source = source.upper()
        source = source.replace('YT_', '').replace('YOUTUBE_', '')
        return source_map.get(source, source.title())