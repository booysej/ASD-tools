from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QAction, QMessageBox
from PySide6.QtGui import QIcon, QPainter, QPixmap, QBrush, QPen
from PySide6.QtCore import Qt
from .plugin_loader import PluginManager
from .main_window import CogToolsMainWindow
from .theme import AppleColors
import os

class CogToolsTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = None
        self.setup_icon()
        self.setToolTip("CogTools: Cognitive Assist Suite")
        self.setup_menu()
        
        # Double-click to show window
        self.activated.connect(self.on_tray_activated)
        
    def setup_icon(self):
        """Create or load tray icon"""
        # Try to load from file first
        icon_path = os.path.join(os.path.dirname(__file__), "../assets/icons/tray_icon_32.png")
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        else:
            # Create icon dynamically if file doesn't exist
            pixmap = self.create_tray_icon(32)
            self.setIcon(QIcon(pixmap))
    
    def create_tray_icon(self, size=32):
        """Create a tray icon dynamically"""
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw a rounded rectangle background
        brush = QBrush(AppleColors.ACCENT)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(4, 4, 24, 24, 8, 8)
        
        # Draw the "C" for CogTools
        painter.setPen(QPen(Qt.white, 2))
        painter.setFont(painter.font())
        font = painter.font()
        font.setPixelSize(16)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "C")
        
        painter.end()
        
        return pixmap
        
    def setup_menu(self):
        """Setup the tray menu"""
        self.menu = QMenu()
        
        # Apply menu styling
        self.menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #E5E5E5;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
                color: #333333;
            }
            QMenu::item:selected {
                background-color: #007AFF;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background-color: #E5E5E5;
                margin: 4px 0px;
            }
        """)
        
        # Show/Hide action
        self.show_action = QAction("Show CogTools")
        self.show_action.triggered.connect(self.toggle_window)
        self.menu.addAction(self.show_action)
        
        self.menu.addSeparator()
        
        # Quick access to plugins
        self.plugin_manager = PluginManager()
        for name, plugin_class in self.plugin_manager.get_plugins().items():
            action = QAction(f"Open {plugin_class.name}")
            action.triggered.connect(lambda checked, n=name: self.open_plugin(n))
            self.menu.addAction(action)
        
        self.menu.addSeparator()
        
        # Settings action
        settings_action = QAction("Settings")
        settings_action.triggered.connect(lambda: self.open_plugin("settings_panel"))
        self.menu.addAction(settings_action)
        
        # About action
        about_action = QAction("About CogTools")
        about_action.triggered.connect(self.show_about)
        self.menu.addAction(about_action)
        
        self.menu.addSeparator()
        
        # Quit action
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit)
        self.menu.addAction(self.quit_action)
        
        self.setContextMenu(self.menu)
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window()
    
    def toggle_window(self):
        """Show or hide the main window"""
        if not self.main_window:
            self.main_window = CogToolsMainWindow()
            self.main_window.window_closed.connect(self.on_window_closed)
            
        if self.main_window.isVisible():
            self.main_window.hide()
            self.show_action.setText("Show CogTools")
        else:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()
            self.show_action.setText("Hide CogTools")
    
    def open_plugin(self, plugin_name):
        """Open main window and switch to specific plugin"""
        if not self.main_window:
            self.main_window = CogToolsMainWindow()
            self.main_window.window_closed.connect(self.on_window_closed)
        
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        
        # Find and select the plugin in sidebar
        plugins = list(self.plugin_manager.get_plugins().keys())
        if plugin_name in plugins:
            index = plugins.index(plugin_name)
            self.main_window.sidebar.setCurrentRow(index)
    
    def on_window_closed(self):
        """Handle main window close"""
        self.show_action.setText("Show CogTools")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(None, "About CogTools", 
                         "<h2>CogTools</h2>"
                         "<p>Cognitive Assistance Suite</p>"
                         "<p>Version 1.0.0</p>"
                         "<p>A beautiful, accessible tool suite designed to help "
                         "with focus, memory, and executive function.</p>")
    
    def quit(self):
        """Quit the application"""
        if self.main_window:
            self.main_window.close()
        from PySide6.QtWidgets import QApplication
        QApplication.quit()