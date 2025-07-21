from cogtools.core.plugin_base import PluginBase
from .ui import VisualCodingHelperWidget

class Plugin(PluginBase):
    name = "Visual Coding Helper"
    icon = None  # TODO: Set icon path

    def get_widget(self):
        return VisualCodingHelperWidget()