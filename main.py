import os
import logging
from pathlib import Path
from typing import Dict, Any
from src.auth import SetAuth
from dotenv import load_dotenv
from config.settings import Settings
from googleapiclient.discovery import build
from src.report import GDocsReporter
from src.analytics import (
    ChannelAnalytics, 
    VideoAnalytics, 
    analyze_trends,
    GeographyAnalytics,
    EngagementAnalytics,
    ImpressionAnalytics
)

def initialize_apis(config: Dict[str, Any]):
    """Initialize YouTube API clients."""
    auth = SetAuth(config['credentials_path'])
    credentials = auth.get_credentials()
    
    if not credentials:
        logging.error("Failed to obtain credentials")
        return None, None
        
    youtube = build('youtube', 'v3', credentials=credentials)
    youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
    
    return youtube, youtube_analytics, credentials

def gather_analytics_data(youtube, youtube_analytics, config: Dict[str, Any]) -> Dict[str, Any]:
    """Gather all analytics data."""
    # Initialize analytics components
    channel = ChannelAnalytics(youtube, youtube_analytics)
    video = VideoAnalytics(youtube, youtube_analytics)
    geography = GeographyAnalytics(youtube_analytics)
    engagement = EngagementAnalytics(youtube_analytics)
    impressions = ImpressionAnalytics(youtube_analytics)
    
    # Gather channel data
    channel_stats = channel.get_basic_stats()
    period_stats = channel.get_period_analytics(config['report_period_days'])
    
    # Gather video data
    videos = video.get_recent_videos(config['max_videos'])
    
    # For each video, gather additional metrics
    for video_data in videos:
        video_id = video_data['id']
        video_data.update({
            'geography': geography.get_watch_time_by_country(video_id),
            'retention': video.get_audience_retention(video_id),
            'engagement': engagement.get_video_engagement(video_id),
            'real_time': engagement.get_real_time_metrics(video_id),
            'impressions': impressions.get_impression_metrics(video_id)
        })
    
    # Gather channel-wide metrics
    peak_viewing = engagement.get_peak_viewing_times(config['report_period_days'])
    geo_distribution = geography.get_watch_time_by_country()
    trend_data = analyze_trends(videos)
    
    return {
        'channel_stats': channel_stats,
        'period_stats': period_stats,
        'videos': videos,
        'peak_viewing': peak_viewing,
        'geo_distribution': geo_distribution,
        'trend_analysis': trend_data
    }

def generate_report(data: Dict[str, Any], credentials) -> None:
    """Generate analytics report in Google Docs."""
    reporter = GDocsReporter(credentials)

    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
    
    doc_id = os.getenv('YOUTUBE_ANALYSIS_DOCS_ID')
    reporter.create_report(
        data['channel_stats'],
        data['period_stats'],
        data['videos'],
        data['peak_viewing'],
        data['geo_distribution'],
        data.get('trend_analysis')
    )
    print(f"Report updated: https://docs.google.com/document/d/{doc_id}")

def main():
    """Run YouTube Analytics report generation."""
    try:
        # Load settings
        config = Settings.load()
        
        # Setup logging
        logging.basicConfig(level=config['log_level'])
        
        # Initialize APIs
        youtube, youtube_analytics, credentials = initialize_apis(config)
        if not youtube or not youtube_analytics:
            return
            
        # Gather all analytics data
        analytics_data = gather_analytics_data(youtube, youtube_analytics, config)
        
        # Generate report
        generate_report(analytics_data, credentials)
            
    except Exception as e:
        logging.error(f"Error running analytics: {e}")
        raise

if __name__ == "__main__":
    main()