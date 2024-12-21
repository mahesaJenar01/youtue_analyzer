from typing import Dict, Any, Optional
from src.utils.formatters import DataFormatter
from src.utils.date_helper import DateHelper

class BaseDocFormatter:
    """Base class for Google Doc section formatters."""
    
    def __init__(self):
        """Initialize common formatters and helpers."""
        self.formatter = DataFormatter()
        self.date_helper = DateHelper()

    def create_section_request(self, 
                             text: str, 
                             header: Optional[str] = None, 
                             add_newline: bool = True) -> Dict[str, Any]:
        """
        Create a Google Docs API request to insert a section of text.
        
        Args:
            text: The main text content to insert
            header: Optional section header (will be formatted differently)
            add_newline: Whether to add extra newline after the section
        
        Returns:
            Dict containing the Google Docs API request
        """
        formatted_text = ""
        
        if header:
            formatted_text = f"{header}\n"
        
        formatted_text += text
        
        if add_newline:
            formatted_text += "\n\n"
        
        return {
            'insertText': {
                'text': formatted_text,
                'endOfSegmentLocation': {}
            }
        }

    def create_styled_section_request(self, 
                                    text: str,
                                    bold: bool = False,
                                    italic: bool = False,
                                    font_size: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a request for styled text section.
        
        Args:
            text: Text content to insert
            bold: Whether to make text bold
            italic: Whether to make text italic
            font_size: Font size in points (optional)
            
        Returns:
            Dict containing the Google Docs API request with styling
        """
        request = {
            'insertText': {
                'text': text,
                'endOfSegmentLocation': {}
            }
        }

        if any([bold, italic, font_size]):
            request['updateTextStyle'] = {
                'textStyle': {
                    'bold': bold,
                    'italic': italic,
                },
                'fields': 'bold,italic'
            }
            
            if font_size:
                request['updateTextStyle']['textStyle']['fontSize'] = {
                    'magnitude': font_size,
                    'unit': 'PT'
                }
                request['updateTextStyle']['fields'] += ',fontSize'

        return request

    def format_list_section(self, 
                          items: list, 
                          header: Optional[str] = None,
                          bullet_style: str = 'BULLET') -> Dict[str, Any]:
        """
        Create a bulleted or numbered list section.
        
        Args:
            items: List of items to format
            header: Optional section header
            bullet_style: Style of list ('BULLET' or 'NUMBER')
            
        Returns:
            Dict containing the Google Docs API request for a list
        """
        text = ""
        if header:
            text = f"{header}\n"
        
        for item in items:
            text += f"• {str(item)}\n" if bullet_style == 'BULLET' else f"1. {str(item)}\n"
            
        return self.create_section_request(text)

    def format_table_row(self, *args: Any) -> str:
        """
        Format table row with proper spacing.
        
        Args:
            *args: Values to include in the row
            
        Returns:
            Formatted table row string
        """
        return " | ".join(str(arg) for arg in args)

    def safe_format_number(self, value: Any, default: str = "N/A") -> str:
        """
        Safely format a number with error handling.
        
        Args:
            value: Number to format
            default: Default value if formatting fails
            
        Returns:
            Formatted number string or default value
        """
        try:
            if value is None:
                return default
            return self.formatter.format_number(float(value))
        except (ValueError, TypeError):
            return default
            
    def safe_format_percentage(self, 
                             value: Any, 
                             decimal_places: int = 1, 
                             default: str = "N/A") -> str:
        """
        Safely format a percentage with error handling.
        
        Args:
            value: Number to format as percentage
            decimal_places: Number of decimal places to show
            default: Default value if formatting fails
            
        Returns:
            Formatted percentage string or default value
        """
        try:
            if value is None:
                return default
            return self.formatter.format_percentage(float(value), decimal_places)
        except (ValueError, TypeError):
            return default