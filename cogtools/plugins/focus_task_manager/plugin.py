from cogtools.core.plugin_base import PluginBase
from .ui import FocusTaskManagerWidget

class Plugin(PluginBase):
    name = "Focus Task Manager"
    icon = None  # TODO: Set icon path

    def get_widget(self):
        return FocusTaskManagerWidget()