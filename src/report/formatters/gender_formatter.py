from typing import Dict, List
from .base_formatter import BaseDocFormatter

class GenderFormatter(BaseDocFormatter):
    def format_gender_breakdown(self, demographics_data: List[Dict]) -> Dict:
        """Format gender breakdown section."""
        text = "Viewer Gender Breakdown\n"
        
        # Group by gender and sum percentages
        gender_totals = {'Male': 0.0, 'Female': 0.0}
        for demo in demographics_data:
            for item in demo:
                gender_totals[item['gender']] += item['percentage']
                
        # Calculate averages
        if len(demographics_data) > 0:
            for gender in gender_totals:
                gender_totals[gender] /= len(demographics_data)
        
        # Format output
        for gender, percentage in gender_totals.items():
            text += f"{gender}: {self.formatter.format_percentage(percentage)}\n"
        
        return self.create_section_request(text)