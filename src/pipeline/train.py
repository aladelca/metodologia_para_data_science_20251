"""Script de entrenamiento para el modelo Prophet."""
import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Tuple

import joblib
import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from pipeline.config import RUTA_DATOS, RUTA_SP500

# Crear directorio de logs si no existe
os.makedirs("logs", exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/train.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def cargar_datos(tick: str, fecha_inicio: str, fecha_corte: str) -> pd.DataFrame:
    """Carga y prepara los datos para el modelo Prophet.

    Parameters
    ----------
    tick : str
        Símbolo de la acción.
    fecha_inicio : str
        Fecha de inicio en formato 'YYYY-MM-DD'.
    fecha_corte : str
        Fecha de corte en formato 'YYYY-MM-DD'.

    Returns
    -------
    pd.DataFrame
        DataFrame con los datos preparados para Prophet.
    """
    logger.info(f"Cargando datos para {tick} desde {fecha_inicio} hasta {fecha_corte}")

    # Cargar datos
    if tick == "S&P500":
        ruta_archivo = os.path.join(RUTA_SP500)
        df = pd.read_csv(ruta_archivo)
        df["fecha"] = pd.to_datetime(df["Date"])
        df = df.drop(columns=["Date"])
        df = df.rename(columns={"S&P500": "y"})
        df = df[["fecha", "y"]]

    else:
        ruta_archivo = os.path.join(RUTA_DATOS)
        df = pd.read_csv(ruta_archivo)
        try:
            df = df[df["Symbol"] == tick][["Date", "Symbol", "Close"]]
        except KeyError:
            raise ValueError(f"El símbolo {tick} no existe en el archivo de datos")

        # Convertir columna de fecha a datetime
        df["fecha"] = pd.to_datetime(df["Date"])
        df = df.dropna(inplace=False)
        df = df.rename(columns={"Close": "y"})

    # Filtrar por rango de fechas
    fecha_min = df["fecha"].min()
    fecha_max = df["fecha"].max()

    if pd.Timestamp(fecha_inicio) < pd.Timestamp(fecha_min):
        logger.error(
            f"Fecha de inicio {fecha_inicio} anterior a fecha disponible ({fecha_min})"
        )
        raise ValueError(
            f"La fecha de inicio ({fecha_inicio}) es anterior a la fecha  ({fecha_min})"
        )
    if pd.Timestamp(fecha_corte) > pd.Timestamp(fecha_max):
        logger.error(
            f"Fecha de corte ({fecha_corte}) posterior a fecha máxima ({fecha_max})"
        )
        raise ValueError(
            f"La fecha de corte ({fecha_corte}) es posterior a la fecha ({fecha_max})"
        )
    if pd.Timestamp(fecha_inicio) > pd.Timestamp(fecha_corte):
        logger.error(
            f"Fecha inicio ({fecha_inicio}) posterior a fecha corte ({fecha_corte})"
        )
        raise ValueError(
            f"fecha inicio ({fecha_inicio}) posterior a la fecha corte ({fecha_corte})"
        )
    df = df[
        (df["fecha"] >= pd.Timestamp(fecha_inicio))
        & (df["fecha"] <= pd.Timestamp(fecha_corte))
    ]

    # Preparar datos para Prophet
    df_prophet = df.rename(columns={"fecha": "ds"})

    logger.info(f"Datos cargados: {len(df)} registros")

    return df_prophet


def entrenar_prophet(
    df: pd.DataFrame,
    estacionalidad_anual: bool = True,
    estacionalidad_semanal: bool = True,
    estacionalidad_diaria: bool = False,
    cambio_punto: float = 0.05,
) -> Tuple[Prophet, Dict[str, float]]:
    """Entrena un modelo Prophet.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con datos preparados para Prophet.
    estacionalidad_anual : bool, optional
        Si se debe considerar estacionalidad anual, por defecto True.
    estacionalidad_semanal : bool, optional
        Si se debe considerar estacionalidad semanal, por defecto True.
    estacionalidad_diaria : bool, optional
        Si se debe considerar estacionalidad diaria, por defecto False.
    cambio_punto : float, optional
        Parámetro de cambio de tendencia, por defecto 0.05.

    Returns
    -------
    Tuple[Prophet, Dict[str, float]]
        Modelo Prophet entrenado y métricas de rendimiento.
    """
    logger.info("Iniciando entrenamiento del modelo")
    logger.debug(
        f"Parámetros: estacionalidad_anual={estacionalidad_anual}, "
        f"estacionalidad_semanal={estacionalidad_semanal}, "
        f"estacionalidad_diaria={estacionalidad_diaria}, "
        f"cambio_punto={cambio_punto}"
    )

    # Configurar modelo
    modelo = Prophet(
        yearly_seasonality=estacionalidad_anual,
        weekly_seasonality=estacionalidad_semanal,
        daily_seasonality=estacionalidad_diaria,
        changepoint_prior_scale=cambio_punto,
    )

    # Ajustar modelo
    logger.info("Ajustando modelo...")
    modelo.fit(df)

    # Realizar predicciones en el conjunto de entrenamiento
    logger.info("Calculando métricas...")
    futuro = modelo.make_future_dataframe(periods=0)
    predicciones = modelo.predict(futuro)

    # Calcular métricas
    metricas = {
        "mse": mean_squared_error(df["y"], predicciones["yhat"][: len(df)]),
        "rmse": np.sqrt(mean_squared_error(df["y"], predicciones["yhat"][: len(df)])),
        "mae": mean_absolute_error(df["y"], predicciones["yhat"][: len(df)]),
        "r2": r2_score(df["y"], predicciones["yhat"][: len(df)]),
    }

    logger.info(f"Métricas calculadas: {metricas}")
    return modelo, metricas


def guardar_modelo(modelo, tick, metricas, directorio=None):
    """
    Guarda el modelo Prophet y las métricas en el directorio especificado.

    Args
    ----
        modelo: Modelo Prophet entrenado.
        tick: Ticker de la acción (str).
        metricas: Diccionario de métricas.
        directorio: Carpeta donde guardar los archivos. Si es None, usa RUTA_MODELOS.
    """
    from src.pipeline.config import RUTA_MODELOS

    if directorio is None:
        directorio = RUTA_MODELOS
    os.makedirs(directorio, exist_ok=True)
    modelo_path = os.path.join(directorio, f"prophet_{tick}.joblib")
    metricas_path = os.path.join(directorio, f"metricas_{tick}.json")
    joblib.dump(modelo, modelo_path)
    with open(metricas_path, "w") as f:
        json.dump(metricas, f)


def main():
    """Función principal del script."""
    # Crear directorio de logs si no existe
    os.makedirs("logs", exist_ok=True)

    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description="Entrenar modelo Prophet para series temporales."
    )
    parser.add_argument("--tick", type=str, required=True, help="Símbolo de la acción")
    parser.add_argument(
        "--fecha_inicio", type=str, required=True, help="Fecha de inicio (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--fecha_corte", type=str, required=True, help="Fecha de corte (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--estacionalidad_anual",
        type=bool,
        default=True,
        help="Considerar estacionalidad anual",
    )
    parser.add_argument(
        "--estacionalidad_semanal",
        type=bool,
        default=True,
        help="Considerar estacionalidad semanal",
    )
    parser.add_argument(
        "--estacionalidad_diaria",
        type=bool,
        default=False,
        help="Considerar estacionalidad diaria",
    )
    parser.add_argument(
        "--cambio_punto",
        type=float,
        default=0.05,
        help="Parámetro de cambio de tendencia",
    )

    # Parsear argumentos
    args = parser.parse_args()

    # Validar fechas
    try:
        fecha_inicio = datetime.strptime(args.fecha_inicio, "%Y-%m-%d")
        fecha_corte = datetime.strptime(args.fecha_corte, "%Y-%m-%d")
    except ValueError:
        logger.error("Formato de fecha inválido")
        raise ValueError("Las fechas deben estar en formato YYYY-MM-DD")

    if fecha_inicio >= fecha_corte:
        logger.error("Fecha de inicio posterior o igual a fecha de corte")
        raise ValueError("La fecha de inicio debe ser anterior a la fecha de corte")

    try:
        # Cargar datos
        logger.info(f"Cargando datos para {args.tick}...")
        df = cargar_datos(args.tick, args.fecha_inicio, args.fecha_corte)

        # Entrenar modelo
        logger.info("Entrenando modelo Prophet...")
        modelo, metricas = entrenar_prophet(
            df,
            args.estacionalidad_anual,
            args.estacionalidad_semanal,
            args.estacionalidad_diaria,
            args.cambio_punto,
        )

        # Guardar modelo y métricas
        logger.info("Guardando modelo y métricas...")
        guardar_modelo(modelo, args.tick, metricas)

        # Mostrar métricas
        logger.info("\nMétricas de rendimiento:")
        for metrica, valor in metricas.items():
            logger.info(f"{metrica}: {valor:.4f}")

    except Exception as e:
        logger.error(f"Error durante el entrenamiento: {str(e)}")
        raise


if __name__ == "__main__":
    main()
