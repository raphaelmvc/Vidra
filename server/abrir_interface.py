import sys
import os
import uvicorn
import threading
import webbrowser
import time

# Adiciona a raiz ao sys.path para encontrar src/, configs/, etc.
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Importa normalmente
from server.api.app import app

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Inicia o servidor em thread separada
threading.Thread(target=start_server, daemon=True).start()
time.sleep(2)

# Abre o navegador
webbrowser.open("http://127.0.0.1:8000")

# Mantém o programa ativo
while True:
    time.sleep(1)
