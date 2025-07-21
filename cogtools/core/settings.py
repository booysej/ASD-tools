import os
import yaml

class Settings:
    DEFAULTS = {
        'verbosity': 1,
        'literal_mode': True,
        'animation_speed': 1.0,
        'clarify_tooltips': True,
        'audio_cues': False,
    }
    def __init__(self, path=None):
        self.path = path or os.path.expanduser('~/.cogtools_settings.yaml')
        self.data = dict(self.DEFAULTS)
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                self.data.update(yaml.safe_load(f) or {})

    def save(self):
        with open(self.path, 'w') as f:
            yaml.safe_dump(self.data, f)

    def get(self, key):
        return self.data.get(key, self.DEFAULTS.get(key))

    def set(self, key, value):
        self.data[key] = value
        self.save()