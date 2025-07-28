# 📥 DownloadYoutube

Uma aplicação em Python com interface **Web (FastAPI)** e **Terminal (CLI)** para baixar vídeos do **YouTube**, **TikTok** e **Instagram**, com suporte a autenticação por cookies e geração de logs automáticos.

---

## 🚀 Funcionalidades

- 🎞️ Suporte a YouTube, TikTok e Instagram
- 📥 Download de vídeos com escolha de qualidade e formato
- 🔐 Autenticação com cookies (`cookies_tiktok.txt` e `cookies_instagram.txt`)
- 🌐 Interface web simples via FastAPI + Jinja2
- 💻 Modo terminal interativo (CLI)
- ⚙️ Configuração via `configs/config.ini`
- 📁 Organização por pastas: logs, configs, views, cookies, etc.
- 📝 Logs automáticos dos downloads

---

## 🗂️ Estrutura do Projeto

```
DownloadYoutube/
├── configs/           # Configurações (config.ini)
├── cookies/           # Cookies de autenticação
├── logs/              # Logs de download
├── views/             # Interface web (HTML, CSS, ícones)
├── server/            # FastAPI e inicializador da interface
├── src/               # Lógica principal (downloader, utils)
├── main.py            # Executável da versão terminal (CLI)
├── requirements.txt   # Dependências
├── main.spec          # Configuração do PyInstaller
```

---

## 🧩 Requisitos

- Python 3.10+
- `pip install -r requirements.txt`
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- FastAPI, uvicorn, requests, etc.

---

## 🛠️ Como Executar

### ✅ Versão CLI (Terminal)

```bash
python main.py
```

Ou empacotado com PyInstaller:

```bash
dist/main.exe
```

### ✅ Versão Web (FastAPI)

```bash
python server/abrir_interface.py
```

Abre automaticamente em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## ⚙️ Configuração (`configs/config.ini`)

```ini
[PADRAO]
caminho_destino = C:/Videos
qualidade = 720
formato_padrao = mp4
log_em_arquivo = sim
sobrescrever = não
modo_verbose = sim
nome_padrao = video_baixado
mostrar_qualidades = sim
idioma = pt
```

---

## 🔐 Cookies

Coloque os arquivos `cookies_tiktok.txt` e `cookies_instagram.txt` na pasta `cookies/`.  
Utilizados para baixar vídeos privados ou autenticados.

---

## 🧪 Empacotamento com PyInstaller

### 📦 CLI (.exe)

```bash
pyinstaller --onefile --icon=views/static/img/icon.ico --add-data "configs;configs" --add-data "cookies;cookies" --add-data "logs;logs" main.py
```

### 📦 Web (.exe)

```bash
pyinstaller --onefile --icon=views/static/img/icon.ico --add-data "configs;configs" --add-data "cookies;cookies" --add-data "logs;logs" --add-data "views;views" --add-data "server;server" server/abrir_interface.py
```

O executável será salvo em `dist/`.

---

## 🧼 Limpeza de Build

```bash
rmdir /s /q build dist __pycache__
del *.spec
```

---

## 📌 Observações

- Certifique-se de que o caminho de `caminho_destino` no `config.ini` exista.
- O projeto já trata logs automaticamente.
- Pode ser expandido com novos plugins (baixe áudio, playlists, shorts etc.).

---

## 👨‍💻 Autor

Desenvolvido por **Raphael Monteiro**  
Contato:   
Marca: **RaphaWeb**

---

## 📄 Licença

Este projeto é de uso pessoal e educacional. Para usos comerciais, consulte o autor.
