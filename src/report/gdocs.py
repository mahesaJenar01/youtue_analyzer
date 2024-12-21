import os
from typing import Dict, List
from googleapiclient.discovery import build
from .formatters import (
    ChannelFormatter, 
    VideoFormatter, 
    GeographyFormatter, 
    PeakViewingFormatter, 
    TrendFormatter
)

class GDocsReporter:
    def __init__(self, credentials):
        """Initialize Google Docs client and formatters."""
        self.docs_service = build('docs', 'v1', credentials=credentials)
        self.channel_formatter = ChannelFormatter()
        self.video_formatter = VideoFormatter()
        self.geography_formatter = GeographyFormatter()
        self.peak_viewing_formatter = PeakViewingFormatter()
        self.trend_formatter = TrendFormatter()

    def create_report(self, channel_stats: Dict, period_stats: Dict, videos: List[Dict], 
                     peak_viewing: Dict, geo_data: Dict, trend_data: Dict = None) -> str:
        """Create or update analytics report in Google Docs."""
        document_id = os.getenv('YOUTUBE_ANALYSIS_DOCS_ID')
        
        if not document_id:
            raise ValueError("YOUTUBE_ANALYSIS_DOCS_ID not found in environment variables")
        
        # Clear existing content
        self._clear_document(document_id)
        
        # Generate new content
        self._write_report(document_id, channel_stats, period_stats, videos, 
                          peak_viewing, geo_data, trend_data)
        return document_id

    def _clear_document(self, doc_id: str) -> None:
        """Clear all content from the document if it exists."""
        try:
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            
            if document.get('body', {}).get('content', []):
                end_index = document['body']['content'][-1]['endIndex'] - 1
                
                if end_index > 1:
                    self.docs_service.documents().batchUpdate(
                        documentId=doc_id,
                        body={
                            'requests': [{
                                'deleteContentRange': {
                                    'range': {
                                        'startIndex': 1,
                                        'endIndex': end_index
                                    }
                                }
                            }]
                        }
                    ).execute()
        except Exception as e:
            raise Exception(f"Error clearing document: {str(e)}")

    def _write_report(self, doc_id: str, channel_stats: Dict, period_stats: Dict, 
                     videos: List[Dict], peak_viewing: Dict, geo_data: Dict, 
                     trend_data: Dict = None) -> None:
        """Write formatted content to document."""
        requests = [
            {'insertText': {'location': {'index': 1}, 'text': 'YouTube Analytics Report\n\n'}},
            self.channel_formatter.format_overview(channel_stats),
            self.channel_formatter.format_period_stats(period_stats),
            self.video_formatter.format_videos_section(videos),
            self.peak_viewing_formatter.format_peak_viewing(peak_viewing),
            self.geography_formatter.format_geography(geo_data)
        ]

        if trend_data:
            requests.append(self.trend_formatter.format_trends(trend_data))

        self.docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()