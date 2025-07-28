import sys
import os
from fastapi import FastAPI, Query
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from src.downloader import iniciar_download
from src.utils import obter_caminho_destino, obter_nome_arquivo
from configs.config import carregar_configuracoes
from src.utils import log_download
import time


app = FastAPI()

BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath("."))  # compatível com PyInstaller

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "views/static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "views/templates"))


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class DownloadRequest(BaseModel):
    url: str
    tipo: str = "1"  # 1=video+audio, 2=audio, 3=video sem audio
    qualidade: Optional[str] = ""
    nome: Optional[str] = None

@app.get("/")
def home():
    return {"status": "🟢 API do Downloader está rodando."}

@app.post("/baixar")
def baixar_video(dados: DownloadRequest):
    config = carregar_configuracoes()
    caminho = obter_caminho_destino()
    nome = dados.nome or obter_nome_arquivo(caminho)

    inicio = time.time()
    sucesso, titulo = iniciar_download(
        url=dados.url,
        tipo=dados.tipo,
        qualidade=dados.qualidade or config.get("qualidade", ""),
        caminho=caminho,
        nome=nome
    )
    fim = time.time()
    tempo = fim - inicio

    if sucesso:
        arquivo_final = os.path.join(caminho, nome + ".mp4")
    else:
        arquivo_final = None

    log_download(
        url=dados.url,
        titulo=titulo or "Sem título",
        tipo=dados.tipo,
        qualidade=dados.qualidade or config.get("qualidade", ""),
        caminho=caminho,
        sucesso=sucesso,
        arquivo_final=arquivo_final,
        tempo_download=tempo
    )

    return {
        "status": "✅ Concluído" if sucesso else "❌ Falhou",
        "titulo": titulo,
        "nome_arquivo": nome,
        "caminho": caminho
    }
