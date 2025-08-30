import eel
import os
import sys
import json
from pathlib import Path
from installer import Installer
from config_handler import ConfigHandler
from sounds_handler import SoundsHandler

is_exe: bool = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

if is_exe:
    path: Path = Path(os.getenv("APPDATA")) / "Soundpad"
else:
    path: Path = Path(os.path.dirname(__file__))

Installer(path=path, is_exe=is_exe).assert_integrity()

config_handler: ConfigHandler = ConfigHandler(path=path)
sounds_handler: SoundsHandler = SoundsHandler(path=path)

# Funções
# _____________________________________________________________________________________________________________________#

# Essa função serve para tocar um som específico
@eel.expose
def play_sound(sound: str) -> None:
    """
    Toca o som requisitado conforme o nome do arquivo
    :param sound: nome do arquivo com a extensão (sem o caminho)
    :return:
    """
    sounds_handler.play_sound(sound=sound)


# Essa função serve para enviar para o JS o resultado do arquivo de configuração
@eel.expose
def get_config_data() -> json:
    """
    Retorna o que tem dentro do "config.json" já em JSON
    :return: config_data_json: json
    """
    return config_handler.get_config_json()


# Essa função serve para copiar o arquivo de audio corretamente para a pasta de sons
@eel.expose
def create_new_button(button_name, button_file_name, file_bytes) -> dict:
    """
    Essa função é a junção das outras classes para a geração completa de um novo botão, criando-o no arquivo e copiando
    o som escolhido pelo "usuário" para a pasta de sons
    """
    result: dict = sounds_handler.create_new_sound(file_name=button_file_name, file_bytes=file_bytes)

    if not result['success']:
        return result

    config_handler.save_new_button(button_name=button_name, button_file=button_file_name)

    return {'success': True, 'message': f'Botão \"{button_name}\" foi criado.'}


# Essa função serve para atualizar o nome do botão dentro do arquivo de configurações
@eel.expose
def update_button_name(button_file: str, new_button_name: str) -> None:
    """
    Essa função envia para a devida classe para atualizar o nome dos botões (no momento funciona apenas para os
    manualmente adicionados)
    """
    result: dict = config_handler.update_button_name(button_file=button_file, new_button_name=new_button_name)

    if not result['success']:
        eel.send_error(result['message'])


# Essa função serve para deletar os dados de um botão dentro do arquivo de configurações
@eel.expose
def delete_button(button_file: str) -> dict:
    """
    Essa função deleta o som requisitado, juntamente com seu registro do botão no arquivo de configuração
    """
    result: dict = sounds_handler.delete_sound(file_name=button_file)

    if not result['success']:
        return result

    return config_handler.delete_button(button_file=button_file)  # Retorna um dicionário, do qual o JS tratará.


# Essa função serve para alterar o som de algum botão.
@eel.expose
def change_button_sound(old_file_name: str, new_file_name: str, file_bytes: list[int]) -> dict:
    result: dict = sounds_handler.create_new_sound(file_name=new_file_name, file_bytes=file_bytes)

    if not result['success']:
        return result

    result: dict = sounds_handler.delete_sound(file_name=old_file_name)

    if not result['success']:
        return result

    return config_handler.update_button_file(old_file_name=old_file_name, new_file_name=new_file_name)


@eel.expose
def pause_sound():
    sounds_handler.pause_sound()


@eel.expose
def is_playing() -> bool:
    return sounds_handler.is_playing()
