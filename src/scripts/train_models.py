"""Script para entrenar los modelos."""

import logging
import os
import sys

import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from src.pipeline.config import MAX_DATE, MIN_DATE, RUTA_DATOS  # noqa
from src.pipeline.train import cargar_datos, entrenar_prophet  # noqa

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/train.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main_train_models():
    """Entrenar los modelos para todos los tickers."""

    def _get_all_tickers():
        return list(pd.read_csv(RUTA_DATOS)["Symbol"].unique()) + [
            "S&P500",
            "INTEGRA",
            "PRIMA",
            "HABITAT",
            "PROFUTURO",
        ]

    tickers = _get_all_tickers()
    for ticker in tickers:
        logger.info(f"Entrenando modelo para {ticker}")
        df = cargar_datos(ticker, MIN_DATE, MAX_DATE)
        df = df.dropna()
        if df.empty:
            logger.error(f"No hay datos para {ticker}")
            continue

        modelo, metricas = entrenar_prophet(df)
        logger.info(f"Datos cargados para {ticker}")


if __name__ == "__main__":
    main_train_models()
