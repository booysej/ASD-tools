from cogtools.core.plugin_base import PluginBase
from .ui import FamilySupportCompassWidget

class Plugin(PluginBase):
    name = "Family Support & Relationship Compass"
    icon = None  # TODO: Set icon path

    def get_widget(self):
        return FamilySupportCompassWidget()