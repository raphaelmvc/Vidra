
import os
import sys
import yt_dlp
from datetime import datetime
from configs.config import carregar_configuracoes

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def escolher_plataforma():
    print("\n🌐 Selecione a plataforma:")
    print("1 - YouTube")
    print("2 - TikTok")
    print("3 - Instagram")

    opcoes = {
        '1': 'youtube.com',
        '2': 'tiktok.com',
        '3': 'instagram.com',
    }

    escolha = input("👉 Digite o número correspondente: ").strip()
    if escolha not in opcoes:
        print("❌ Opção inválida. Encerrando o programa.")
        sys.exit(1)

    dominio = opcoes[escolha]
    if dominio == 'instagram.com':
        print("⚠️ Atenção: vídeos privados exigem login ou cookies.")

    return dominio

def obter_url():
    url = input("🔗 Cole a URL do vídeo: ").strip()
    if not url.startswith("http"):
        print("❌ URL inválida. Encerrando o programa.")
        sys.exit(1)
    return url

def validar_url_por_plataforma(url, plataforma):
    if plataforma not in url:
        print(f"❌ A URL não corresponde à plataforma selecionada ({plataforma}). Encerrando o programa.")
        sys.exit(1)

def escolher_tipo_download():
    print("\n📥 Tipo de conteúdo:")
    print("1 - 🎞️ Vídeo com áudio (MP4)")
    print("2 - 🎵 Somente áudio (MP3)")
    print("3 - 🎬 Somente vídeo (sem áudio)")
    tipo = input("👉 Escolha (1/2/3): ").strip()
    if tipo not in ['1', '2', '3']:
        print("❌ Opção inválida. Encerrando o programa.")
        sys.exit(1)
    return tipo

def escolher_qualidade_disponivel(url):
    try:
        ydl_opts = {'quiet': True}

        if "tiktok.com" in url and os.path.exists(resource_path("cookies/cookies_tiktok.txt")):
            ydl_opts['cookiefile'] = resource_path("cookies/cookies_tiktok.txt")
            print("🍪 Usando cookies_tiktok.txt")
        elif "instagram.com" in url and os.path.exists(resource_path("cookies/cookies_instagram.txt")):
            ydl_opts['cookiefile'] = resource_path("cookies/cookies_instagram.txt")
            print("🍪 Usando cookies_instagram.txt")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formatos = info.get('formats', [])
            qualidades = sorted(set(str(f['height']) for f in formatos if f.get('height')), reverse=True)

            if not qualidades:
                print("⚠️ Nenhuma qualidade detectada.")
                return "", []

            print("\n📺 Qualidades disponíveis:")
            print(" 🎯 " + " | ".join([q + "p" for q in qualidades]))
            escolha = input("👉 Digite a qualidade desejada ou pressione Enter para automático: ").replace("p", "").strip()

            if escolha and escolha not in qualidades:
                print("❌ Qualidade inválida. Encerrando o programa.")
                sys.exit(1)

            return escolha, qualidades

    except Exception as e:
        print(f"❌ Erro ao obter qualidades: {e}")
        print("Encerrando o programa.")
        sys.exit(1)

def obter_nome_arquivo(caminho_destino):
    try:
        config = carregar_configuracoes()

        nome_input = input("\n📄 Nome do arquivo (sem extensão): ").strip()
        extensao = f".{config.get('formato_padrao', 'mp4')}"
        sobrescrever = config.get("sobrescrever", "sim").lower() == "sim"
        nome_padrao = config.get("nome_padrao", "video_baixado")

        if not nome_input:
            contador = 1
            nome_base = nome_padrao
            nome_final = nome_base
            destino = os.path.join(caminho_destino, nome_final + extensao)

            while os.path.exists(destino) and not sobrescrever:
                contador += 1
                nome_final = f"{nome_base}_{contador}"
                destino = os.path.join(caminho_destino, nome_final + extensao)

            return nome_final

        destino = os.path.join(caminho_destino, nome_input + extensao)
        if os.path.exists(destino) and not sobrescrever:
            print("⚠️ Arquivo já existe e sobrescrever está desativado. Encerrando o programa.")
            sys.exit(1)

        return nome_input

    except Exception as e:
        print(f"❌ Erro ao gerar nome de arquivo: {e}")
        print("Encerrando o programa.")
        sys.exit(1)

def obter_caminho_destino():
    try:
        config = carregar_configuracoes()
        caminho = os.path.join(os.getcwd(), config.get("caminho_destino", "videos"))
        os.makedirs(caminho, exist_ok=True)
        return caminho
    except Exception as e:
        print(f"❌ Erro ao criar pasta de destino: {e}")
        print("Encerrando o programa.")
        sys.exit(1)

def log_download(url, titulo, tipo, qualidade, caminho, sucesso, arquivo_final=None, tempo_download=None):
    try:
        os.makedirs(resource_path("logs"), exist_ok=True)
        log_path = resource_path(os.path.join("logs", "download_log.txt"))
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "✅ OK" if sucesso else "❌ ERRO"

        tamanho = "-"
        if arquivo_final and os.path.exists(arquivo_final):
            tamanho_bytes = os.path.getsize(arquivo_final)
            tamanho = f"{tamanho_bytes / (1024 * 1024):.2f} MB"

        tempo = f"{tempo_download:.2f}s" if tempo_download else "-"

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(
                f"[🕒 {agora}] {status} | 🧾 Título: {titulo} | 🧠 Tipo: {tipo} | 🎯 Qualidade: {qualidade or 'auto'}p | "
                f"🔗 URL: {url} | 📁 Arquivo: {arquivo_final or caminho} | 📦 Tamanho: {tamanho} | ⏱️ Tempo: {tempo}\n"
            )
    except Exception as e:
        print(f"❌ Falha ao registrar log: {e}")
