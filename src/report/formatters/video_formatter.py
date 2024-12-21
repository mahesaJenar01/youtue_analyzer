from typing import Dict, List
from .base_formatter import BaseDocFormatter

class VideoFormatter(BaseDocFormatter):
    def format_videos_section(self, videos: List[Dict]) -> Dict:
        """Format video details section."""
        text = "Video Performance\n\n"
        for video in videos:
            text += self._format_single_video(video)
        return self.create_section_request(text)

    def _format_single_video(self, video: Dict) -> str:
        """Format individual video details."""
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