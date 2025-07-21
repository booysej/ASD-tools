from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
                               QStackedWidget, QListWidget, QListWidgetItem,
                               QPushButton, QLabel, QFrame, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, Signal, QTimer
from PySide6.QtGui import QIcon, QPainter, QPixmap, QBrush, QPen
from .theme import AppleTheme, AppleColors
from .plugin_loader import PluginManager
import os

class SidebarItem(QListWidgetItem):
    """Custom sidebar item with icon and text"""
    def __init__(self, text, icon_path=None):
        super().__init__(text)
        self.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if icon_path:
            self.setIcon(QIcon(icon_path))

class AppleSidebar(QListWidget):
    """Apple-style sidebar navigation"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSpacing(2)
        
        # Apply custom styling
        self.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                outline: none;
                padding: 8px;
            }
            QListWidget::item {
                color: #333333;
                padding: 8px 12px;
                border-radius: 6px;
                margin: 2px 0px;
            }
            QListWidget::item:hover {
                background-color: rgba(0, 122, 255, 0.1);
            }
            QListWidget::item:selected {
                background-color: rgba(0, 122, 255, 0.15);
                color: #007AFF;
                font-weight: 500;
            }
        """)

class CogToolsMainWindow(QMainWindow):
    """Main application window with Apple-style design"""
    
    window_closed = Signal()
    
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager()
        self.plugin_widgets = {}
        self.current_plugin = None
        self.setup_ui()
        self.load_plugins()
        
    def setup_ui(self):
        """Setup the main window UI"""
        self.setWindowTitle("CogTools")
        self.setMinimumSize(1000, 700)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icons/app_icon_256.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar container
        sidebar_container = QWidget()
        sidebar_container.setFixedWidth(240)
        sidebar_container.setStyleSheet(f"""
            QWidget {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border-right: 1px solid {AppleColors.LIGHT_SEPARATOR.name()};
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(0, 20, 0, 0)
        
        # App title in sidebar
        title_label = QLabel("CogTools")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 700;
                color: #333333;
                padding: 0px 0px 20px 0px;
            }
        """)
        sidebar_layout.addWidget(title_label)
        
        # Sidebar navigation
        self.sidebar = AppleSidebar()
        self.sidebar.currentRowChanged.connect(self.switch_plugin)
        sidebar_layout.addWidget(self.sidebar)
        
        # Settings button at bottom
        settings_btn = QPushButton("Settings")
        settings_btn.setProperty("secondary", True)
        settings_btn.setStyleSheet("""
            QPushButton {
                margin: 10px;
                padding: 10px;
            }
        """)
        sidebar_layout.addWidget(settings_btn)
        
        main_layout.addWidget(sidebar_container)
        
        # Content area
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(30, 30, 30, 30)
        
        # Stacked widget for plugin content
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack)
        
        # Welcome screen
        welcome_widget = self.create_welcome_screen()
        self.content_stack.addWidget(welcome_widget)
        
        main_layout.addWidget(content_container)
        
        # Apply window shadow effect
        self.setWindowFlags(Qt.Window)
        
    def create_welcome_screen(self):
        """Create a beautiful welcome screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # Welcome message
        welcome_label = QLabel("Welcome to CogTools")
        welcome_label.setProperty("heading", True)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: 700;
                color: #333333;
                margin-bottom: 10px;
            }
        """)
        
        subtitle_label = QLabel("Your cognitive assistance suite")
        subtitle_label.setProperty("subheading", True)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #666666;
                margin-bottom: 40px;
            }
        """)
        
        # Feature cards container
        cards_container = QWidget()
        cards_container.setMaximumWidth(800)
        cards_layout = QVBoxLayout(cards_container)
        
        features = [
            ("🎯", "Focus Task Manager", "Stay organized with our beautiful Kanban board"),
            ("🧠", "Memory Vault", "Never forget important information"),
            ("💻", "Visual Coding Helper", "Code with clarity and confidence"),
            ("📅", "Executive Function Coach", "Plan and execute like a pro")
        ]
        
        for emoji, title, description in features:
            card = self.create_feature_card(emoji, title, description)
            cards_layout.addWidget(card)
        
        layout.addWidget(welcome_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(cards_container)
        layout.addStretch()
        
        return widget
    
    def create_feature_card(self, emoji, title, description):
        """Create a beautiful feature card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {AppleColors.LIGHT_SECONDARY_BACKGROUND.name()};
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 12px;
            }}
            QFrame:hover {{
                background-color: {AppleColors.LIGHT_TERTIARY_BACKGROUND.name()};
            }}
        """)
        
        layout = QHBoxLayout(card)
        
        # Emoji
        emoji_label = QLabel(emoji)
        emoji_label.setStyleSheet("font-size: 36px; margin-right: 20px;")
        
        # Text container
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(4)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #333333;
        """)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            font-size: 13px;
            color: #666666;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        
        layout.addWidget(emoji_label)
        layout.addWidget(text_container)
        layout.addStretch()
        
        # Add shadow effect
        shadow = AppleTheme.create_shadow_effect(QColor(0, 0, 0, 30), 10, 0, 2)
        card.setGraphicsEffect(shadow)
        
        return card
    
    def load_plugins(self):
        """Load all available plugins"""
        plugins = self.plugin_manager.get_plugins()
        
        for name, plugin_class in plugins.items():
            # Add to sidebar
            item = SidebarItem(plugin_class.name)
            self.sidebar.addItem(item)
            
            # Create plugin widget
            plugin_instance = plugin_class(self)
            widget = plugin_instance.get_widget()
            self.content_stack.addWidget(widget)
            self.plugin_widgets[name] = (plugin_instance, widget)
    
    def switch_plugin(self, index):
        """Switch to selected plugin with animation"""
        if index < 0:
            self.content_stack.setCurrentIndex(0)  # Welcome screen
            return
            
        # Index + 1 because welcome screen is at index 0
        self.content_stack.setCurrentIndex(index + 1)
        
        # Activate plugin
        plugin_name = list(self.plugin_widgets.keys())[index]
        plugin_instance, _ = self.plugin_widgets[plugin_name]
        
        if self.current_plugin:
            self.current_plugin.on_deactivate()
        
        plugin_instance.on_activate()
        self.current_plugin = plugin_instance
        
        # Add fade animation
        opacity_effect = QGraphicsOpacityEffect()
        self.content_stack.currentWidget().setGraphicsEffect(opacity_effect)
        
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(200)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.window_closed.emit()
        event.accept()