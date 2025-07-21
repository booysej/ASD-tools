from PySide6.QtGui import QPalette, QColor, QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
import sys

class AppleColors:
    """Apple-style color palette"""
    # Light theme colors
    LIGHT_BACKGROUND = QColor(255, 255, 255)
    LIGHT_SECONDARY_BACKGROUND = QColor(242, 242, 247)
    LIGHT_TERTIARY_BACKGROUND = QColor(229, 229, 234)
    LIGHT_TEXT = QColor(0, 0, 0)
    LIGHT_SECONDARY_TEXT = QColor(142, 142, 147)
    LIGHT_SEPARATOR = QColor(198, 198, 200)
    
    # Dark theme colors
    DARK_BACKGROUND = QColor(28, 28, 30)
    DARK_SECONDARY_BACKGROUND = QColor(44, 44, 46)
    DARK_TERTIARY_BACKGROUND = QColor(58, 58, 60)
    DARK_TEXT = QColor(255, 255, 255)
    DARK_SECONDARY_TEXT = QColor(152, 152, 157)
    DARK_SEPARATOR = QColor(54, 54, 56)
    
    # Accent colors
    BLUE = QColor(0, 122, 255)
    GREEN = QColor(52, 199, 89)
    INDIGO = QColor(88, 86, 214)
    ORANGE = QColor(255, 149, 0)
    PINK = QColor(255, 45, 85)
    PURPLE = QColor(175, 82, 222)
    RED = QColor(255, 59, 48)
    TEAL = QColor(90, 200, 250)
    YELLOW = QColor(255, 204, 0)
    
    # Semantic colors
    ACCENT = BLUE
    SUCCESS = GREEN
    WARNING = YELLOW
    DANGER = RED

class AppleTheme:
    """Apple-style theme manager"""
    
    def __init__(self):
        self.is_dark = self._detect_dark_mode()
        
    def _detect_dark_mode(self):
        # Simple dark mode detection - can be enhanced with system detection
        return False
    
    def apply_theme(self):
        """Apply the Apple-style theme to the application"""
        app = QApplication.instance()
        if not app:
            return
            
        # Load SF Pro font if available, fallback to system font
        font = QFont()
        if sys.platform == "darwin":
            font.setFamily("SF Pro Display")
        else:
            font.setFamily("Segoe UI" if sys.platform == "win32" else "Ubuntu")
        font.setPixelSize(13)
        app.setFont(font)
        
        # Apply color palette
        palette = self._create_palette()
        app.setPalette(palette)
        
        # Apply global stylesheet
        app.setStyleSheet(self._get_global_stylesheet())
    
    def _create_palette(self):
        """Create the color palette based on theme"""
        palette = QPalette()
        
        if self.is_dark:
            palette.setColor(QPalette.Window, AppleColors.DARK_BACKGROUND)
            palette.setColor(QPalette.WindowText, AppleColors.DARK_TEXT)
            palette.setColor(QPalette.Base, AppleColors.DARK_SECONDARY_BACKGROUND)
            palette.setColor(QPalette.AlternateBase, AppleColors.DARK_TERTIARY_BACKGROUND)
            palette.setColor(QPalette.Text, AppleColors.DARK_TEXT)
            palette.setColor(QPalette.Button, AppleColors.DARK_SECONDARY_BACKGROUND)
            palette.setColor(QPalette.ButtonText, AppleColors.DARK_TEXT)
            palette.setColor(QPalette.BrightText, AppleColors.ACCENT)
            palette.setColor(QPalette.Highlight, AppleColors.ACCENT)
            palette.setColor(QPalette.HighlightedText, AppleColors.DARK_TEXT)
        else:
            palette.setColor(QPalette.Window, AppleColors.LIGHT_BACKGROUND)
            palette.setColor(QPalette.WindowText, AppleColors.LIGHT_TEXT)
            palette.setColor(QPalette.Base, AppleColors.LIGHT_BACKGROUND)
            palette.setColor(QPalette.AlternateBase, AppleColors.LIGHT_SECONDARY_BACKGROUND)
            palette.setColor(QPalette.Text, AppleColors.LIGHT_TEXT)
            palette.setColor(QPalette.Button, AppleColors.LIGHT_SECONDARY_BACKGROUND)
            palette.setColor(QPalette.ButtonText, AppleColors.LIGHT_TEXT)
            palette.setColor(QPalette.BrightText, AppleColors.ACCENT)
            palette.setColor(QPalette.Highlight, AppleColors.ACCENT)
            palette.setColor(QPalette.HighlightedText, AppleColors.LIGHT_BACKGROUND)
            
        return palette
    
    def _get_global_stylesheet(self):
        """Get the global stylesheet with Apple-style components"""
        bg = AppleColors.DARK_BACKGROUND if self.is_dark else AppleColors.LIGHT_BACKGROUND
        secondary_bg = AppleColors.DARK_SECONDARY_BACKGROUND if self.is_dark else AppleColors.LIGHT_SECONDARY_BACKGROUND
        text = AppleColors.DARK_TEXT if self.is_dark else AppleColors.LIGHT_TEXT
        secondary_text = AppleColors.DARK_SECONDARY_TEXT if self.is_dark else AppleColors.LIGHT_SECONDARY_TEXT
        separator = AppleColors.DARK_SEPARATOR if self.is_dark else AppleColors.LIGHT_SEPARATOR
        
        return f"""
        /* Global styles */
        QWidget {{
            background-color: {bg.name()};
            color: {text.name()};
        }}
        
        /* Beautiful buttons with Apple style */
        QPushButton {{
            background-color: {AppleColors.ACCENT.name()};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
            font-size: 13px;
        }}
        
        QPushButton:hover {{
            background-color: {AppleColors.ACCENT.darker(110).name()};
        }}
        
        QPushButton:pressed {{
            background-color: {AppleColors.ACCENT.darker(120).name()};
        }}
        
        QPushButton:disabled {{
            background-color: {secondary_bg.name()};
            color: {secondary_text.name()};
        }}
        
        /* Secondary button style */
        QPushButton[secondary="true"] {{
            background-color: {secondary_bg.name()};
            color: {text.name()};
        }}
        
        QPushButton[secondary="true"]:hover {{
            background-color: {secondary_bg.darker(110).name()};
        }}
        
        /* Text inputs */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {secondary_bg.name()};
            border: 1px solid {separator.name()};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {AppleColors.ACCENT.name()};
            outline: none;
        }}
        
        /* Labels */
        QLabel {{
            color: {text.name()};
            font-size: 13px;
        }}
        
        QLabel[heading="true"] {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        
        QLabel[subheading="true"] {{
            font-size: 15px;
            font-weight: 500;
            color: {secondary_text.name()};
        }}
        
        /* Lists */
        QListWidget, QTreeWidget, QTableWidget {{
            background-color: {bg.name()};
            border: 1px solid {separator.name()};
            border-radius: 8px;
            outline: none;
        }}
        
        QListWidget::item, QTreeWidget::item, QTableWidget::item {{
            padding: 8px;
            border-radius: 6px;
        }}
        
        QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {{
            background-color: {AppleColors.ACCENT.name()};
            color: white;
        }}
        
        /* Scroll bars */
        QScrollBar:vertical {{
            background-color: transparent;
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {separator.name()};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {separator.darker(110).name()};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        /* Menu styling */
        QMenu {{
            background-color: {bg.name()};
            border: 1px solid {separator.name()};
            border-radius: 8px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 20px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {AppleColors.ACCENT.name()};
            color: white;
        }}
        
        QMenu::separator {{
            height: 1px;
            background-color: {separator.name()};
            margin: 4px 0px;
        }}
        
        /* Tab widget */
        QTabWidget::pane {{
            border: none;
            background-color: {bg.name()};
        }}
        
        QTabBar::tab {{
            background-color: transparent;
            padding: 8px 16px;
            margin-right: 4px;
            border-radius: 6px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {secondary_bg.name()};
        }}
        
        /* Progress bar */
        QProgressBar {{
            background-color: {secondary_bg.name()};
            border: none;
            border-radius: 4px;
            height: 8px;
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: {AppleColors.ACCENT.name()};
            border-radius: 4px;
        }}
        """
    
    @staticmethod
    def create_shadow_effect(color=QColor(0, 0, 0, 80), blur_radius=20, offset_x=0, offset_y=2):
        """Create an Apple-style shadow effect"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(color)
        shadow.setBlurRadius(blur_radius)
        shadow.setOffset(offset_x, offset_y)
        return shadow
    
    @staticmethod
    def create_fade_animation(widget, duration=200):
        """Create a fade-in animation"""
        animation = QPropertyAnimation(widget, b"windowOpacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        return animation

# Global theme instance
theme = AppleTheme()

def apply_flat_theme():
    """Legacy function - now applies Apple theme"""
    theme.apply_theme()