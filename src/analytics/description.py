# src/description.py
from typing import Dict, Any

class DescriptionAnalytics:
     def __init__(self, youtube):
         """Initialize with YouTube API client."""
         self.youtube = youtube

     def get_video_description(self, video_id: str) -> str:
         """Get the description of a video."""
         try:
             response = self.youtube.videos().list(
                 part="snippet",
                 id=video_id
             ).execute()
         
             if 'items' not in response or not response['items']:
                 return "No description available."
         
             return response['items'][0]['snippet'].get('description', "No description available.")
         
         except Exception:
             return "Error retrieving description."