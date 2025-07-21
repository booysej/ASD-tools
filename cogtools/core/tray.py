from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QAction, QMessageBox
from PySide6.QtGui import QIcon
from .plugin_loader import PluginManager

class CogToolsTray(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon())  # TODO: Set a real icon
        self.setToolTip("CogTools: Cognitive Assist Suite")
        self.menu = QMenu()
        self.plugin_manager = PluginManager()
        self.plugin_actions = {}
        for name, plugin_class in self.plugin_manager.get_plugins().items():
            action = QAction(plugin_class.name)
            action.triggered.connect(lambda checked, n=name: self.launch_plugin(n))
            self.menu.addAction(action)
            self.plugin_actions[name] = action
        self.menu.addSeparator()
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit)
        self.menu.addAction(self.quit_action)
        self.setContextMenu(self.menu)

    def launch_plugin(self, plugin_name):
        QMessageBox.information(None, "Plugin Launch", f"Launching plugin: {plugin_name}\n(Plugin UI coming soon)")

    def quit(self):
        from PySide6.QtWidgets import QApplication
        QApplication.quit()