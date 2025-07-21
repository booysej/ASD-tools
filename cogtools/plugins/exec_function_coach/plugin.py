from cogtools.core.plugin_base import PluginBase
from .ui import ExecFunctionCoachWidget

class Plugin(PluginBase):
    name = "Executive Function Coach"
    icon = None  # TODO: Set icon path

    def get_widget(self):
        return ExecFunctionCoachWidget()