from PySide6.QtWidgets import QWidget

class PluginBase:
    name = "BasePlugin"
    icon = None  # Path to icon

    def __init__(self, main_window=None):
        self.main_window = main_window

    def get_widget(self) -> QWidget:
        raise NotImplementedError

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass