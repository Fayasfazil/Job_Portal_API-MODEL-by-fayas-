"""
Theme Module
-----------
Defines the color palette and font settings for the 'Stealth Mode' UI.
"""

class Theme:
    # Colors
    BACKGROUND = "#121212"       # Deep Black/Gray
    SURFACE = "#1e1e1e"          # Slightly lighter for cards/sidebar
    ACCENT = "#ffffff"           # High contrast white
    TEXT = "#e0e0e0"             # Off-white for text
    TEXT_SECONDARY = "#a0a0a0"   # Gray for subtitles
    
    # Input Fields
    INPUT_BG = "#2b2b2b"
    INPUT_FG = "#ffffff"
    
    # Success/Error (Muted)
    SUCCESS = "#81c784"
    ERROR = "#e57373"
    
    # Fonts
    FONT_FAMILY = "Roboto"
    HEADER_FONT = ("Roboto", 28, "bold")
    SUBHEADER_FONT = ("Roboto", 20)
    BODY_FONT = ("Roboto", 14)
    BUTTON_FONT = ("Roboto", 14, "bold")
