"""Script principal para ejecutar la API de Prophet."""
import os
import sys

import uvicorn

from src.pipeline.api import app

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    # Crear directorio de logs si no existe
    os.makedirs("logs", exist_ok=True)

    # Iniciar servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)
