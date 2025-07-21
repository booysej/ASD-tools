import os
from pathlib import Path

DATA_DIR = Path.home() / '.cogtools_data'

os.makedirs(DATA_DIR, exist_ok=True)

def get_plugin_data_dir(plugin_name):
    path = DATA_DIR / plugin_name
    os.makedirs(path, exist_ok=True)
    return path