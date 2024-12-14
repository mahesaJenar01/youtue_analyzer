def analyze_trends(videos):
    """Comprehensive trend analysis for YouTube channel."""
    if not videos:
        return {
            'performance_trends': {
                'views': {'total_trend': 0, 'rolling_average': []},
                'engagement_rate': {'average_engagement': 0, 'trend': 0},
                'watch_time': {'total_trend': 0, 'rolling_average': []}
            },
            'content_insights': {
                'best_performing_videos': [],
                'worst_performing_videos': [],
                'content_type_performance': {}
            },
            'audience_trends': {
                'demographic_shifts': [],
                'geographic_expansion': []
            }
        }

    return {
        'performance_trends': {
            'views': _calculate_view_trend(videos),
            'engagement_rate': _calculate_engagement_trend(videos),
            'watch_time': _calculate_watch_time_trend(videos)
        },
        'content_insights': {
            'best_performing_videos': _find_top_videos(videos),
            'worst_performing_videos': _find_bottom_videos(videos),
            'content_type_performance': _analyze_content_types(videos)
        },
        'audience_trends': {
            'demographic_shifts': _track_demographic_changes(videos),
            'geographic_expansion': _analyze_geographic_growth(videos)
        }
    }

def _calculate_view_trend(videos):
    """Calculate view trend over time."""
    views = [video['stats']['views'] for video in videos]
    
    if not views or len(views) < 2 or views[0] == 0:
        return {'total_trend': 0, 'rolling_average': []}
    
    return {
        'total_trend': _calculate_percentage_change(views),
        'rolling_average': _calculate_rolling_average(views)
    }

def _calculate_engagement_trend(videos):
    """Calculate engagement trend."""
    engagement_rates = [
        (video['stats']['likes'] / video['stats']['views'] * 100) 
        for video in videos if video['stats']['views'] > 0
    ]
    
    if not engagement_rates:
        return {'average_engagement': 0, 'trend': 0}
    
    return {
        'average_engagement': sum(engagement_rates) / len(engagement_rates),
        'trend': _calculate_percentage_change(engagement_rates) if len(engagement_rates) > 1 else 0
    }

def _calculate_watch_time_trend(videos):
    """Calculate watch time trend."""
    watch_times = [
        video.get('performance', {}).get('watch_time', 0) 
        for video in videos
    ]
    
    if not watch_times or len(watch_times) < 2 or watch_times[0] == 0:
        return {'total_trend': 0, 'rolling_average': []}
    
    return {
        'total_trend': _calculate_percentage_change(watch_times),
        'rolling_average': _calculate_rolling_average(watch_times)
    }

def _calculate_percentage_change(values):
    """Calculate percentage change between first and last values."""
    if len(values) < 2 or values[0] == 0:
        return 0
    return ((values[-1] - values[0]) / values[0]) * 100

def _calculate_rolling_average(values, window=3):
    """Calculate rolling average."""
    return [
        sum(values[max(0, i-window):i+1]) / min(window, i+1) 
        for i in range(len(values))
    ]

def _find_top_videos(videos, top_n=5):
    """Find top performing videos."""
    return sorted(videos, key=lambda x: x['stats']['views'], reverse=True)[:top_n]

def _find_bottom_videos(videos, bottom_n=5):
    """Find bottom performing videos."""
    return sorted(videos, key=lambda x: x['stats']['views'])[:bottom_n]

def _analyze_content_types(videos):
    """Analyze performance by content type or tags."""
    # Placeholder for more sophisticated content type extraction
    return {}

def _track_demographic_changes(videos):
    """Track shifts in audience demographics."""
    demographic_data = [
        video.get('demographics', {}).get('audience', []) 
        for video in videos
    ]
    return demographic_data

def _analyze_geographic_growth(videos):
    """Analyze geographic distribution growth."""
    geographic_data = [
        video.get('geography', []) 
        for video in videos
    ]
    return geographic_data