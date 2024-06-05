from globais import *

# Informe aqui a posição do sprites que deseja pegar do spritesheet

texturas_sheet = {
    'mago_idle': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (0, 0), 'quant': 6},
    'mago_run': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (0, 16), 'quant': 6},
    'mago_hit': {'tipo': 'player', 'tamanho': (16, 16), 'posicao': (16, 0), 'quant': 3},
}

relacao_mapas = {
    'm01': {'tipo': 'barco', 'caminho': 'mapcsv/m01.csv', 'fundo': 'imgs/maps/m01.png', 'tamanho': (960, 960), 'prox_map': 'm02'},
    'm02': {'tipo': 'barco', 'caminho': 'mapcsv/m02.csv', 'fundo': 'imgs/maps/m02.png', 'tamanho': (960, 960), 'prox_map': 'm03'},
    'm03': {'tipo': 'vila', 'caminho': 'mapcsv/m03.csv', 'fundo': 'imgs/maps/m03.png', 'tamanho': (1088, 832), 'prox_map': 'm04'}
}

# Insira aqui a imagem, o tipo e o caminho dela para ser carregado.

texturas_por_imagem = {
    'tijolo': {'tipo': 'bloco', 'caminho': 'imgs/tijolo.png', 'tamanho': (BLOCO_TAM, BLOCO_TAM)},
    'inimigo': {'tipo': 'inimigo', 'caminho': 'imgs/inimigo.png', 'tamanho': (32,32)},
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
