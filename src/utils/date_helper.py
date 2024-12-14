from datetime import datetime, timedelta
from typing import Tuple, Dict

class DateHelper:
    @staticmethod
    def get_date_range(days: int = 30) -> Tuple[str, str]:
        """Get start and end dates in YYYY-MM-DD format."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return (
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )

    @staticmethod
    def format_duration(duration: str) -> str:
        """Format ISO 8601 duration to readable format."""
        minutes, seconds = '0', '0'
        duration = duration.replace('PT', '')
        
        if 'H' in duration:
            hours, rest = duration.split('H')
            minutes = rest.split('M')[0] if 'M' in rest else '0'
            seconds = rest.split('M')[1].replace('S', '') if 'S' in rest else '0'
            return f"{hours}:{minutes.zfill(2)}:{seconds.zfill(2)}"
        
        if 'M' in duration:
            minutes, seconds = duration.split('M')
            seconds = seconds.replace('S', '')
        else:
            seconds = duration.replace('S', '')
            
        return f"{minutes}:{seconds.zfill(2)}"

    @staticmethod
    def format_timestamp(timestamp: str) -> str:
        """Format ISO timestamp to readable format."""
        dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        return dt.strftime('%B %d, %Y %I:%M %p')