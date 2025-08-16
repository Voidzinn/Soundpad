import os
from pathlib import Path
from pygame import mixer, time


class SoundsHandler:
    def __init__(self, path: Path):
        self.sounds_path: Path = path / 'Sounds'

        mixer.init()

    def play_sound(self, sound: str):
        mixer.music.load(self.sounds_path / sound)

        mixer.music.play()

    @staticmethod
    def pause_sound() -> None:
        mixer.music.unload()

    @staticmethod
    def is_playing() -> bool:
        return mixer.music.get_busy()

    def create_new_sound(self, file_name, file_bytes) -> dict:
        if file_name in os.listdir(self.sounds_path):
            return {'success': False, 'message': 'Arquivo com esse nome já existe.'}

        with open(self.sounds_path / file_name, 'wb') as file:
            file.write(bytearray(file_bytes))

        return {'success': True, 'message': 'Arquivo criado com sucesso'}

    def delete_sound(self, file_name) -> dict:
        if file_name not in os.listdir(self.sounds_path):
            return {'success': False, 'message': 'Arquivo não encontrado.'}

        try:
            os.remove(self.sounds_path / file_name)

        except Exception as e:
            return {'success': False, 'message': f'Houve um erro inesperado: \n {e}'}

        return {'success': True, 'message': 'Arquivo criado com sucesso'}
