import re
import json
from pathlib import Path


def find_button_key(button_file: str, data: dict) -> str or None:
    for key, value in data.items():
        if button_file == value['file']:
            return key

    return None


class ConfigHandler:
    def __init__(self, path: Path):
        self.CONFIG_FILE = path / 'configs' / 'config.json'

        with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
            self.config_data: dict[str: dict[str: str]] = json.load(f)

    # Essa função serve para retornar o resultado em JSON do arquivo "config.json"
    def get_config_json(self) -> json:
        return json.dumps(self.config_data)

    # Essa função atualiza o arquivo "config.json"
    def _update_config_file(self) -> None:
        with open(self.CONFIG_FILE, 'w') as file:
            file.write(json.dumps(self.config_data, indent=True))

    # Essa função serve para criar corretamente o botão dentro do arquivo
    def save_new_button(self, button_name, button_file):
        existing_buttons = self.config_data['created_buttons'].keys()
        max_index = 0
        for key in existing_buttons:
            match = re.match(r'button(\d+)', key)
            if match:
                max_index = max(max_index, int(match.group(1)))

        button_index = max_index + 1

        self.config_data['created_buttons'][f'button{button_index}'] = {'file': button_file, 'name': button_name}
        self._update_config_file()

    def update_button_name(self, button_file, new_button_name) -> dict:
        button_key: str or None = find_button_key(button_file=button_file, data=self.config_data['created_buttons'])

        if not button_key:
            return {'success': False, 'message': 'Botão não foi encontrado.'}

        self.config_data['created_buttons'][button_key] = {'file': button_file, 'name': new_button_name}
        self._update_config_file()

        return {'success': True, 'message': 'Nome do botão atualizado.'}

    def delete_button(self, button_file) -> dict:
        button_key: str or None = find_button_key(button_file=button_file, data=self.config_data['created_buttons'])

        if not button_key:
            return {'success': False, 'message': 'Botão não foi encontrado.'}

        del self.config_data['created_buttons'][button_key]
        self._update_config_file()

        return {'success': True, 'message': 'Botão foi removido do arquivo'}

    def update_button_file(self, old_file_name: str, new_file_name: str):
        button_key: str or None = find_button_key(old_file_name, self.config_data['created_buttons'])

        if not button_key:
            return {'success': False, 'message': 'Botão não foi encontrado.'}

        button_reference: dict[str, str] = self.config_data['created_buttons'][button_key]

        self.config_data['created_buttons'][button_key] = {'file': new_file_name, 'name': button_reference['name']}
        self._update_config_file()

        return {'success': True, 'message': 'Música do botão foi alterada com sucesso'}
