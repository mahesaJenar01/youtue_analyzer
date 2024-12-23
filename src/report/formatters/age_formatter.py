from typing import Dict, List
from .base_formatter import BaseDocFormatter

class AgeRangeFormatter(BaseDocFormatter):
    def format_age_breakdown(self, demographics_data: List[Dict]) -> Dict:
        """Format age range breakdown section."""
        text = "Viewer Age Ranges\n"
        
        # Initialize age ranges totals
        age_totals = {
            '13-17': 0.0,
            '18-24': 0.0,
            '25-34': 0.0,
            '35-44': 0.0,
            '45-54': 0.0,
            '55-64': 0.0,
            '65+': 0.0
        }
        
        # Aggregate age data across all videos
        count = 0
        for demo in demographics_data:
            if demo:  # Check if demographics data exists
                count += 1
                for item in demo:
                    age_group = item.get('age_group', '')
                    if age_group in age_totals:
                        age_totals[age_group] += item.get('percentage', 0)
        
        # Calculate averages
        if count > 0:
            for age_group in age_totals:
                age_totals[age_group] /= count
        
        # Format output
        for age_group, percentage in age_totals.items():
            if percentage > 0:  # Only show age ranges with viewers
                text += f"{age_group}: {self.formatter.format_percentage(percentage)}\n"
        
        return self.create_section_request(text)