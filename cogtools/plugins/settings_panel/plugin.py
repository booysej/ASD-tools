from cogtools.core.plugin_base import PluginBase
from .ui import SettingsPanelWidget

class Plugin(PluginBase):
    name = "Settings Panel"
    icon = None  # TODO: Set icon path

    def get_widget(self):
        return SettingsPanelWidget()