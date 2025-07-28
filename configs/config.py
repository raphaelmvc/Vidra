# configs/config.py

import configparser
import os
import sys


def carregar_configuracoes():
    config = configparser.ConfigParser()

    # Detecta se está rodando como .exe (PyInstaller)
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    caminho_config = os.path.normpath(os.path.join(base_path, "configs", "config.ini"))

    if not os.path.exists(caminho_config):
        print("⚠️ Arquivo config.ini não encontrado. Usando valores padrão.")
        return {
            'caminho_destino': os.path.abspath('videos'),
            'qualidade': '',
            'sobrescrever': 'sim',
            'formato_padrao': 'mp4',
            'modo_verbose': 'sim',
            'nome_padrao': 'video_baixado',
            'mostrar_qualidades': 'sim',
            'usar_nome_original': 'não',
            'baixar_legendas': 'não',
            'log_em_arquivo': 'sim',
            'idioma': 'pt'
        }

    config.read(caminho_config, encoding="utf-8")
    padrao = config['PADRAO']

    # Funções utilitárias
    def get_str(key, default):
        return padrao.get(key, default).strip().lower()

    def get_path(key, default):
        raw = padrao.get(key, default).strip()
        return os.path.abspath(os.path.normpath(raw))

    caminho_destino = get_path('caminho_destino', 'videos')
    print("📂 Caminho final destino:", caminho_destino)

    return {
        'caminho_destino': caminho_destino,
        'qualidade': get_str('qualidade', ''),
        'sobrescrever': get_str('sobrescrever', 'sim'),
        'formato_padrao': get_str('formato_padrao', 'mp4'),
        'modo_verbose': get_str('modo_verbose', 'sim'),
        'nome_padrao': padrao.get('nome_padrao', 'video_baixado').strip(),
        'mostrar_qualidades': get_str('mostrar_qualidades', 'sim'),
        'usar_nome_original': get_str('usar_nome_original', 'não'),
        'baixar_legendas': get_str('baixar_legendas', 'não'),
        'log_em_arquivo': get_str('log_em_arquivo', 'sim'),
        'idioma': get_str('idioma', 'pt')
    }
