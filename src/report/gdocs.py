import os
from typing import Dict, List
from googleapiclient.discovery import build
from .formatters import (
    ChannelFormatter, 
    VideoFormatter, 
    GeographyFormatter, 
    PeakViewingFormatter, 
    TrendFormatter,
    GenderFormatter, 
    AgeRangeFormatter
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
        self.gender_formatter = GenderFormatter()
        self.age_formatter = AgeRangeFormatter()

    def create_report(self, channel_stats: Dict, period_stats: Dict, videos: List[Dict], 
                     peak_viewing: Dict, geo_data: Dict, trend_data: Dict = None) -> str:
        """Create or update analytics report in Google Docs."""
        document_id = os.getenv('YOUTUBE_ANALYSIS_DOCS_ID')
        
        if not document_id:
            raise ValueError("YOUTUBE_ANALYSIS_DOCS_ID not found in environment variables")
        
        # Clear existing content
        self._clear_document(document_id)
        
        # Get demographics data from videos
        demographics_data = [
            video.get('demographics', {}).get('audience', [])
            for video in videos
            if video.get('demographics', {}).get('audience')
        ]
        
        # Generate new content sections
        requests = self._generate_report_sections(
            document_id,
            channel_stats,
            period_stats,
            videos,
            peak_viewing,
            geo_data,
            demographics_data,
            trend_data
        )
        
        # Execute update
        self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()
        
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

    def _generate_report_sections(
        self,
        document_id: str,
        channel_stats: Dict,
        period_stats: Dict,
        videos: List[Dict],
        peak_viewing: Dict,
        geo_data: Dict,
        demographics_data: List[Dict],
        trend_data: Dict = None
    ) -> List[Dict]:
        """Generate all sections of the report."""
        requests = [
            # Title
            {
                'insertText': {
                    'location': {'index': 1},
                    'text': 'YouTube Analytics Report\n\n'
                }
            },
            
            # Channel Overview
            self.channel_formatter.format_overview(channel_stats),
            
            # Period Statistics
            self.channel_formatter.format_period_stats(period_stats),
            
            # Video Performance
            self.video_formatter.format_videos_section(videos),
            
            # Peak Viewing Times
            self.peak_viewing_formatter.format_peak_viewing(peak_viewing),
            
            # Geographic Distribution
            self.geography_formatter.format_geography(geo_data)
        ]

        # Trend Analysis (if available)
        if trend_data:
            requests.append(self.trend_formatter.format_trends(trend_data))
        
        # Gender Demographics
        if demographics_data:
            requests.append(self.gender_formatter.format_gender_breakdown(demographics_data))
            
        # Age Range Demographics (new section)
        if demographics_data:
            requests.append(self.age_formatter.format_age_breakdown(demographics_data))

        return requests

    def _create_section_styles(self, requests: List[Dict], doc_id: str) -> None:
        """Apply consistent styling to document sections."""
        try:
            # Apply title styling
            requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': 1,
                        'endIndex': 25  # Approximate length of title
                    },
                    'paragraphStyle': {
                        'namedStyleType': 'HEADING_1',
                        'alignment': 'CENTER'
                    },
                    'fields': 'namedStyleType,alignment'
                }
            })

            # Apply section header styling
            sections = self.docs_service.documents().get(
                documentId=doc_id
            ).execute().get('body', {}).get('content', [])

            for section in sections:
                if 'paragraph' in section:
                    paragraph = section.get('paragraph', {})
                    if paragraph.get('paragraphStyle', {}).get('namedStyleType') == 'NORMAL_TEXT':
                        start_index = section.get('startIndex', 0)
                        end_index = section.get('endIndex', 0)
                        
                        requests.append({
                            'updateParagraphStyle': {
                                'range': {
                                    'startIndex': start_index,
                                    'endIndex': end_index
                                },
                                'paragraphStyle': {
                                    'namedStyleType': 'HEADING_2'
                                },
                                'fields': 'namedStyleType'
                            }
                        })
        except Exception as e:
            raise Exception(f"Error applying styles: {str(e)}")