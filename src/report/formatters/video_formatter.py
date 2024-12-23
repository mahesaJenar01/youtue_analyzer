from typing import Dict, List
from .base_formatter import BaseDocFormatter

class VideoFormatter(BaseDocFormatter):
    def format_videos_section(self, videos: List[Dict]) -> Dict:
        """Format video details section."""
        if not videos:
            return self.create_section_request("No videos found in the specified period.\n")

        text = "Video Performance\n\n"
        
        # Format each video's details
        for video in videos:
            text += self._format_single_video(video)
            
        return self.create_section_request(text)

    def _format_single_video(self, video: Dict) -> str:
        """Format individual video details."""
        stats = video.get('stats', {})
        impression_data = video.get('impressions', {})
        
        text = (
            f"Title: {video.get('title', 'Untitled')}\n"
            f"Upload Date: {self.date_helper.format_timestamp(video.get('published_at', ''))}\n"
            f"Views: {self.formatter.format_number(stats.get('views', 0))}\n"
            f"Likes: {self.formatter.format_number(stats.get('likes', 0))}\n"
        )
        
        # Add impression metrics
        text += (
            f"Impressions: {self.formatter.format_number(impression_data.get('impressions', 0))}\n"
            f"Click-through Rate: {self.formatter.format_percentage(impression_data.get('click_through_rate', 0))}\n"
        )
        
        if 'performance' in video:
            perf = video['performance']
            text += (
                f"Watch Time: {self.formatter.format_time(perf.get('watch_time', 0))}\n"
                f"Average View Duration: {perf.get('avg_view_duration', 0)}s\n"
            )
        
        # Add duration if available
        if 'duration' in video:
            text += f"Duration: {video['duration']}\n"
            
        if 'stats' in video and 'comments' in video['stats']:
            text += f"Comments: {self.formatter.format_number(video['stats']['comments'])}\n"
        
        return text + "\n"

    def format_video_demographics(self, demographics: Dict) -> str:
        """Format video demographics information."""
        if not demographics or 'audience' not in demographics:
            return ""
            
        text = "Audience Demographics:\n"
        for demo in demographics.get('audience', []):
            text += (
                f"{demo.get('age_group', 'Unknown Age')} "
                f"{demo.get('gender', 'Unknown Gender')}: "
                f"{self.formatter.format_percentage(demo.get('percentage', 0))}\n"
            )
        return text

    def format_video_traffic_sources(self, traffic_data: List[Dict]) -> str:
        """Format video traffic source information."""
        if not traffic_data:
            return ""
            
        text = "Traffic Sources:\n"
        for source in traffic_data:
            text += (
                f"{source.get('source', 'Unknown')}: "
                f"{self.formatter.format_number(source.get('views', 0))} views\n"
            )
        return text