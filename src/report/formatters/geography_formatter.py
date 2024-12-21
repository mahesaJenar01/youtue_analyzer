from typing import List, Dict
from .base_formatter import BaseDocFormatter

class GeographyFormatter(BaseDocFormatter):
    def format_geography(self, geo_data: List[Dict]) -> Dict:
        """Format geographic distribution section."""
        text = "Geographic Distribution\n"
        
        # Take top 5 countries
        top_countries = geo_data[:5]
        
        for country in top_countries:
            text += (
                f"{country['country']}: "
                f"{self.formatter.format_number(country['views'])} views "
                f"({self.formatter.format_time(country['watch_time_minutes'])} watch time)\n"
            )
        
        return self.create_section_request(text)