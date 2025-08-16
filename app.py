from os import _exit
import eel_functions
import socket
import ctypes
import eel
import os

path = os.getcwd()

# Funções
# _____________________________________________________________________________________________________________________#


# Função para encontrar uma porta que esteja livre.
def find_free_port(start_port: int = 8000, max_tries: int = 11) -> int:
    """Tenta encontrar uma porta livre começando de uma porta inicial."""
    for i in range(1, max_tries):
        if is_port_open(start_port + i):
            return start_port + i
    raise Exception(f"Não foi possível encontrar uma porta livre em {max_tries - 1} tentativas.")


# Função para verificar se a porta atual está aberta
def is_port_open(port: int) -> bool:
    """Verifica se a porta está aberta (disponível) no localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', port))  # Tenta se conectar ao localhost na porta especificada
        return result != 0  # Se o resultado for diferente de 0, a porta está livre


# Função para obter a escala do monitor
def get_scale() -> float:
    """
    Obtém a escala do monitor principal, para que a janela seja centralizada independentemente da resolução utilizada
    :return: float
    """
    try:
        user32 = ctypes.windll.user32
        hdc = user32.GetDC(0)
        gdi32 = ctypes.windll.gdi32

        dpi = gdi32.GetDeviceCaps(hdc, 88)
        scaling_factor = dpi / 96
        user32.ReleaseDC(0, hdc)
        return scaling_factor
    except Exception as e:
        print(f"{e}")
        return 1.0


# Função para obter a posição do centro da tela
def center_screen(window_width: int, window_height: int) -> tuple[int, int]:
    """
    Obtém as coordenadas relativas da tela principal retornando x e y.
    :arg window_width: Largura da janela.
    :arg window_height: Altura da janela.
    :return: tuple[int, int]
    """
    user32 = ctypes.windll.user32
    scaling: float = get_scale()

    screen_width: int = int(user32.GetSystemMetrics(0) / scaling)
    screen_height: int = int(user32.GetSystemMetrics(1) / scaling)

    x: int = (screen_width - window_width) // 2
    y: int = (screen_height - window_height) // 2
    return x, y


# Função para fechar o código ao fechar o eel
def on_close_callback(route, sockets):
    """
    Encerra o código ao fechar a tela para não gastar memória e CPU.
    :return:
    """
    _exit(0)


# Função para iniciar o eel
def start_eel():
    """
    Obtém/calcula os valores necessários e inicia a janela, por padrão iniciada no centro da tela.
    """
    # Definindo as dimensões da janela criada
    width: int = 1920
    height: int = 1080

    # Definindo variáveis para receber as coordenadas do centro
    x: int
    y: int
    x, y = center_screen(window_width=width, window_height=height)

    # Achando a porta livre para iniciar o app
    port = find_free_port(start_port=8000)

    # Eel inicia a pasta chamada 'web' e o nome pode ser mudado se necessário
    eel.init('web')
    # Aqui é onde o eel inicia a tela de verdade, as únicas coisas que realmente não podem mudar são:
    #     block=True | mode='chrome' (não recomendo mudar) | close_callback=on_close_callback
    eel.start('app.html', size=(width, height), position=(x, y), mode='firefox', port=port,
              close_callback=on_close_callback, cmdline_args=['--incognito'])

# Main
# _____________________________________________________________________________________________________________________#


if __name__ == '__main__':
    start_eel()
