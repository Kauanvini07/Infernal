from globais import *

# Informe aqui a posição do sprites que deseja pegar do spritesheet

texturas_sheet = {
    'mago_idle': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (0, 0), 'quant': 6},
    'mago_run': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (0, 16), 'quant': 6},
    'mago_hit': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (16, 0), 'quant': 3}
}

# Insira aqui a imagem, o tipo e o caminho dela para ser carregado.

texturas_por_imagem = {
    'fundo': {'tipo': 'background', 'caminho': 'imgs/maps/F01.png', 'tamanho': (SCREEN_WIDTH, SCREEN_WIDTH),"csv":'mapcsv\F01.csv'},
    'tijolo': {'tipo': 'bloco', 'caminho': 'imgs/tijolo.png', 'tamanho': (BLOCO_TAM, BLOCO_TAM)},
    'inimigo': {'tipo': 'inimigo', 'caminho': 'imgs/inimigo.png', 'tamanho': (48,48)},
    'inimigo_hit': {'tipo': 'inimigo', 'caminho': 'imgs/inimigo_hit.png', 'tamanho': (32,32)}
}

textura_ataque = {
    'cajado_madeira1': {'tipo': 'item', 'caminho': 'imgs/Little Mage/Attack/StaffWood/AttackWood1.png', 'tamanho': (32, 32)},
    'cajado_madeira2': {'tipo': 'item', 'caminho': 'imgs/Little Mage/Attack/StaffWood/AttackWood2.png', 'tamanho': (32, 32)},
    'cajado_madeira3': {'tipo': 'item', 'caminho': 'imgs/Little Mage/Attack/StaffWood/AttackWood3.png', 'tamanho': (32, 32)},
    'cajado_madeira4': {'tipo': 'item', 'caminho': 'imgs/Little Mage/Attack/StaffWood/AttackWood4.png', 'tamanho': (32, 32)},
    'cajado_madeira5': {'tipo': 'item', 'caminho': 'imgs/Little Mage/Attack/StaffWood/AttackWood5.png', 'tamanho': (32, 32)},
    'cajado_madeira6': {'tipo': 'item', 'caminho': 'imgs/Little Mage/Attack/StaffWood/AttackWood6.png', 'tamanho': (32, 32)}
}