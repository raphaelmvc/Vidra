import yt_dlp
import os

def progresso_download(d):
    if d['status'] == 'downloading':
        print(f"📦 Baixando: {d['_percent_str']} ({d['_eta_str']} restantes)")
    elif d['status'] == 'finished':
        print("✅ Download finalizado. Convertendo...")

def verificar_tamanho_arquivo(info, limite_mb=500):
    tamanho_bytes = info.get('filesize') or info.get('filesize_approx') or 0
    tamanho_mb = tamanho_bytes / (1024 * 1024)
    if tamanho_mb > limite_mb:
        print(f"🛑 Arquivo com {tamanho_mb:.2f} MB excede o limite de {limite_mb} MB.")
        confirmar = input("❓ Deseja continuar? (s/n): ").strip().lower()
        if confirmar != 's':
            print("🚫 Download cancelado.")
            raise Exception("Download cancelado por tamanho")

def montar_opcoes(tipo, qualidade, caminho, nome, url):
    saida = os.path.join(caminho, nome + ".%(ext)s")
    opcoes = {
        'outtmpl': saida,
        'progress_hooks': [progresso_download],
        'verbose': True,
        'noplaylist': False,
    }
    if "instagram.com" in url and os.path.exists("cookies/cookies_instagram.txt"):
        opcoes['cookiefile'] = os.path.join("cookies", "cookies_instagram.txt")
    elif "tiktok.com" in url and os.path.exists("cookies/cookies_tiktok.txt"):
        opcoes['cookiefile'] = os.path.abspath("cookies/cookies_tiktok.txt")

    if tipo == '1':
        opcoes['format'] = f"bestvideo[height<={qualidade}]+bestaudio/best" if qualidade else "bestvideo+bestaudio/best"
        opcoes['merge_output_format'] = 'mp4'
    elif tipo == '2':
        opcoes.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif tipo == '3':
        opcoes['format'] = f"bestvideo[height<={qualidade}]" if qualidade else 'bestvideo'

    return opcoes

def iniciar_download(url, tipo, qualidade, caminho, nome):
    try:
        print("🚀 Preparando para iniciar o download...")

        # Garante que o diretório de destino existe
        os.makedirs(caminho, exist_ok=True)

        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            verificar_tamanho_arquivo(info)

        ydl_opts = montar_opcoes(tipo, qualidade, caminho, nome, url)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        saida_final = os.path.join(caminho, nome + ".mp4")
        if not os.path.exists(saida_final):
            print("❌ Erro: arquivo final não foi criado.")
            return False, ""

        titulo = info.get("title", "Sem título")
        print(f"\n✅ Download concluído com sucesso: {titulo}")
        return True, titulo

    except yt_dlp.utils.DownloadError as e:
        print(f"❌ Falha no download: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    return False, ""
