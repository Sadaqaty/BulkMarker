import os
import json

class PresetsManager:
    def __init__(self, presets_dir):
        self.presets_dir = presets_dir
        os.makedirs(self.presets_dir, exist_ok=True)

    def load_presets_list(self):
        presets = []
        for file in os.listdir(self.presets_dir):
            if file.endswith('.json'):
                presets.append(file[:-5])
        return presets

    def save_preset(self, name, data):
        with open(os.path.join(self.presets_dir, name + '.json'), 'w') as f:
            json.dump(data, f)

    def load_preset(self, name):
        with open(os.path.join(self.presets_dir, name + '.json'), 'r') as f:
            return json.load(f)

    def delete_preset(self, name):
        os.remove(os.path.join(self.presets_dir, name + '.json'))