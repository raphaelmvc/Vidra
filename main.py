import traceback
import time
import os
from datetime import datetime
from configs.config import carregar_configuracoes
from src.downloader import iniciar_download
from src.utils import (
    obter_url,
    escolher_tipo_download,
    obter_nome_arquivo,
    obter_caminho_destino,
    escolher_plataforma,
    validar_url_por_plataforma,
    log_download,
    escolher_qualidade_disponivel,
)

def main():
    config = carregar_configuracoes()

    print("🟢 Iniciando downloader...\n")

    plataforma = escolher_plataforma()
    print(f"📡 Plataforma escolhida: {plataforma}")

    url = obter_url()
    print(f"🔗 URL: {url}")

    validar_url_por_plataforma(url, plataforma)
    print("✅ Plataforma validada")

    tipo = escolher_tipo_download()
    print(f"📥 Tipo: {tipo}")

    qualidade_config = config.get("qualidade", "")
    qualidade, _ = escolher_qualidade_disponivel(url) if config.get("mostrar_qualidades", "sim") == "sim" else (qualidade_config, [])
    print(f"🎯 Qualidade: {qualidade or 'automático'}")

    caminho = obter_caminho_destino()
    print(f"📁 Pasta destino: {caminho}")

    nome = obter_nome_arquivo(caminho)
    print(f"📄 Nome do arquivo: {nome}")

    # 🔁 Cronômetro do tempo de download
    inicio = time.time()
    sucesso, titulo = iniciar_download(url, tipo, qualidade, caminho, nome)
    fim = time.time()
    tempo_total = fim - inicio

    # 📦 Caminho completo do arquivo final
    extensao = config.get("formato_padrao", "mp4")
    arquivo_final = os.path.join(caminho, f"{nome}.{extensao}")

    # 📝 Log avançado
    if config.get("log_em_arquivo", "sim") == "sim":
        log_download(
            url=url,
            titulo=titulo,
            tipo=tipo,
            qualidade=qualidade,
            caminho=caminho,
            sucesso=sucesso,
            arquivo_final=arquivo_final,
            tempo_download=tempo_total
        )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERRO GERAL: {e}")
        traceback.print_exc()
