import importlib
import os
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent.parent / 'plugins'

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        sys.path.insert(0, str(PLUGIN_DIR.parent))
        for plugin_dir in PLUGIN_DIR.iterdir():
            if plugin_dir.is_dir() and (plugin_dir / 'plugin.py').exists():
                module_name = f'cogtools.plugins.{plugin_dir.name}.plugin'
                try:
                    module = importlib.import_module(module_name)
                    plugin_class = getattr(module, 'Plugin', None)
                    if plugin_class:
                        self.plugins[plugin_dir.name] = plugin_class
                except Exception as e:
                    print(f"Failed to load plugin {plugin_dir.name}: {e}")

    def get_plugins(self):
        return self.plugins