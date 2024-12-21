from typing import Dict
from .base_formatter import BaseDocFormatter

class PeakViewingFormatter(BaseDocFormatter):
    def format_peak_viewing(self, peak_data: Dict) -> Dict:
        """Format peak viewing section."""
        text = "Peak Viewing Times\n"
        peak_times = peak_data.get('peak_times', [])[:5]
        
        for day in peak_times:
            text += (
                f"Date: {day['date']} - "
                f"Views: {self.formatter.format_number(day['views'])} - "
                f"Watch Time: {self.formatter.format_time(day['watch_time'])}\n"
            )
        
        return self.create_section_request(text)