from globais import *

# Informe aqui a posição do sprites que deseja pegar do spritesheet

texturas_sheet = {
    'mago_idle': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (0,0), 'quant': 6},
    'mago_run': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (0,16),'quant': 6},
    'mago_hit': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (16,0),'quant': 3}
}

# Insira aqui a imagem, o tipo e o caminho dela para ser carregado.

texturas_por_imagem = {
    'fundo': {'tipo': 'background', 'caminho': 'imgs/bg.jpg', 'tamanho': (SCREEN_WIDTH, SCREEN_WIDTH)},
    'inimigo': {'tipo': 'inimigo', 'caminho': 'imgs/inimigo.png', 'tamanho': (64,64)},
    'inimigo_hit': {'tipo': 'inimigo', 'caminho': 'imgs/inimigo_hit.png', 'tamanho': (32,32)}
}