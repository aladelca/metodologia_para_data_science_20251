"""Script de inferencia para el modelo Prophet."""
import argparse
import os
from datetime import datetime

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet

from src.pipeline.config import RUTA_MODELOS


def cargar_modelo(tick: str) -> Prophet:
    """Carga un modelo Prophet guardado."""
    ruta_modelo = os.path.join(RUTA_MODELOS, f"prophet_{tick}.joblib")
    if not os.path.exists(ruta_modelo):
        raise FileNotFoundError(
            f"No se encontró el modelo para {tick} en {ruta_modelo}"
        )

    return joblib.load(ruta_modelo)


def realizar_prediccion(
    modelo: Prophet, fecha_inicio: str, fecha_fin: str
) -> pd.DataFrame:
    """Realiza la predicción para el período especificado.

    Parameters
    ----------
    modelo : Prophet
        Modelo Prophet cargado.
    df_historico : pd.DataFrame
        DataFrame con datos históricos.
    fecha_inicio : str
        Fecha de inicio de la predicción.
    fecha_fin : str
        Fecha de fin de la predicción.

    Returns
    -------
    pd.DataFrame
        DataFrame con las predicciones.
    """
    # Calcular el número de días entre fecha_inicio y fecha_fin
    dias = (pd.Timestamp(fecha_fin) - pd.Timestamp(fecha_inicio)).days

    # Crear DataFrame para predicción usando make_future_dataframe
    # freq='B' indica que solo se consideran días hábiles (business days)
    df_futuro = modelo.make_future_dataframe(
        periods=dias,
        freq="B",  # Business days (excluye fines de semana y feriados)
        include_history=False,
    )

    # Filtrar solo las fechas dentro del rango deseado
    df_futuro = df_futuro[
        (df_futuro["ds"] >= pd.Timestamp(fecha_inicio))
        & (df_futuro["ds"] <= pd.Timestamp(fecha_fin))
    ]

    # Realizar predicción
    predicciones = modelo.predict(df_futuro)

    return predicciones


def visualizar_prediccion(predicciones, tick, fecha_inicio, fecha_fin, directorio=None):
    """
    Guarda la visualización de la predicción en el directorio especificado.

    Args
    ----
        predicciones: DataFrame con las predicciones.
        tick: Ticker de la acción.
        fecha_inicio: Fecha de inicio (str).
        fecha_fin: Fecha de fin (str).
        directorio: Carpeta para la imagen. Si es None, directorio actual.
    """
    if directorio is None:
        directorio = os.getcwd()
    os.makedirs(directorio, exist_ok=True)
    nombre_archivo = f"prediccion_{tick}_{fecha_inicio}_{fecha_fin}.png"
    ruta = os.path.join(directorio, nombre_archivo)

    plt.figure(figsize=(10, 5))
    plt.plot(predicciones["ds"], predicciones["yhat"], label="Predicción")
    plt.fill_between(
        predicciones["ds"],
        predicciones["yhat_lower"],
        predicciones["yhat_upper"],
        alpha=0.2,
        label="Intervalo de confianza",
    )
    plt.title(f"Predicción para {tick}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio")
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()


def guardar_prediccion(predicciones, tick, fecha_inicio, fecha_fin, directorio=None):
    """
    Guarda las predicciones en un archivo CSV en el directorio especificado.

    Args
    ----
        predicciones: DataFrame con las predicciones.
        tick: Ticker de la acción.
        fecha_inicio: Fecha de inicio (str).
        fecha_fin: Fecha de fin (str).
        directorio: Carpeta del archivo. Si es None, directorio actual.
    """
    if directorio is None:
        directorio = os.getcwd()
    os.makedirs(directorio, exist_ok=True)
    nombre_archivo = f"prediccion_{tick}_{fecha_inicio}_{fecha_fin}.parquet"
    ruta = os.path.join(directorio, nombre_archivo)
    predicciones.to_parquet(ruta)


def main():
    """Función principal del script."""
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description="Realizar predicciones con el modelo Prophet."
    )
    parser.add_argument("--tick", type=str, required=True, help="Símbolo de la acción")
    parser.add_argument(
        "--fecha_inicio",
        type=str,
        required=True,
        help="Fecha de inicio de la predicción (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--fecha_fin",
        type=str,
        required=True,
        help="Fecha de fin de la predicción (YYYY-MM-DD)",
    )

    # Parsear argumentos
    args = parser.parse_args()

    # Validar fechas
    try:
        fecha_inicio = datetime.strptime(args.fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(args.fecha_fin, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Las fechas deben estar en formato YYYY-MM-DD")

    if fecha_inicio >= fecha_fin:
        raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin")

    # Cargar modelo
    print(f"Cargando modelo para {args.tick}...")
    modelo = cargar_modelo(args.tick)

    # Realizar predicción
    print("Realizando predicción...")
    predicciones = realizar_prediccion(modelo, args.fecha_inicio, args.fecha_fin)

    # Visualizar predicción
    print("Generando visualización...")
    visualizar_prediccion(predicciones, args.tick, args.fecha_inicio, args.fecha_fin)

    # Guardar predicción
    print("Guardando predicciones...")
    guardar_prediccion(predicciones, args.tick, args.fecha_inicio, args.fecha_fin)

    print("\nPredicción final. Resultados se han guardado en la carpeta 'outputs'.")


if __name__ == "__main__":
    main()
