import os
import sys
import shutil
from pathlib import Path


class Installer:
    def __init__(self, path: Path, is_exe: bool):
        self.base_path: Path = path
        self.sounds_path: Path = path / "Sounds"
        self.configs_path: Path = path / "configs"
        self.is_exe: bool = is_exe

    def assert_integrity(self):
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.sounds_path.mkdir(parents=True, exist_ok=True)
        if not (self.configs_path / 'config.json').exists():
            self.generate_files()

    def generate_files(self):
        if self.is_exe:
            internal_path: Path = Path(sys._MEIPASS)
        else:
            internal_path: Path = Path(os.path.dirname(__file__))

        self.configs_path.mkdir(parents=True, exist_ok=True)

        config_file_path: Path = internal_path / "config.json"
        print(config_file_path)
        if not os.path.exists(self.configs_path / "config.json"):
            shutil.copy(config_file_path, self.configs_path / "config.json")
