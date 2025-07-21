from cogtools.core.plugin_base import PluginBase
from .ui import MemoryVaultWidget

class Plugin(PluginBase):
    name = "Memory & Reference Vault"
    icon = None  # TODO: Set icon path

    def get_widget(self):
        return MemoryVaultWidget()