"""Lambda handler para hacer predicciones con modelos almacenados en S3."""

# Standard library imports
import json
import logging
from datetime import datetime

# Third-party imports
import boto3
import pandas as pd
from prophet import Prophet

# Configuración de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configuración de S3
s3_client = boto3.client("s3")

MODELS_PREFIX = "models/"
BUCKET_NAME = "s3://mis-acciones/models/"


def load_model_from_s3(ticker: str) -> Prophet:
    """Carga un modelo desde S3."""
    try:
        model_path = f"{MODELS_PREFIX}{ticker}_model.json"
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=model_path)
        model_json = json.loads(response["Body"].read().decode("utf-8"))

        model = Prophet()
        model.from_dict(model_json)
        return model
    except Exception as e:
        logger.error(f"Error cargando modelo para {ticker}: {str(e)}")
        raise


def get_prediction_dates(days_ahead: int = 30) -> pd.DataFrame:
    """Genera fechas para predicción."""
    last_date = datetime.now()
    future_dates = pd.DataFrame(
        {"ds": pd.date_range(start=last_date, periods=days_ahead, freq="D")}
    )
    return future_dates


def lambda_handler(event, context):
    """Manejador principal de la función Lambda."""
    try:
        # Obtener parámetros del evento
        ticker = event.get("ticker")
        days_ahead = event.get("days_ahead", 30)

        if not ticker:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Se requiere el parámetro ticker"}),
            }

        # Cargar modelo
        model = load_model_from_s3(ticker)

        # Generar fechas para predicción
        future_dates = get_prediction_dates(days_ahead)

        # Hacer predicción
        forecast = model.predict(future_dates)

        # Formatear resultado
        predictions = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(
            "records"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"ticker": ticker, "predictions": predictions}),
        }

    except Exception as e:
        logger.error(f"Error en la función Lambda: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
