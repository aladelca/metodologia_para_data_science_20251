"""API para entrenar y predecir con el modelo Prophet."""
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.pipeline.inference import cargar_modelo, realizar_prediccion
from src.pipeline.train import cargar_datos, entrenar_prophet, guardar_modelo

# Crear directorio de logs si no existe
os.makedirs("logs", exist_ok=True)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/api.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="Prophet Stock Predictor API",
    description="API para entrenar y predecir precios de acciones usando Prophet",
    version="1.0.0",
)


class TrainRequest(BaseModel):
    """Modelo para la solicitud de entrenamiento."""

    tick: str = Field(..., description="Símbolo de la acción")
    fecha_inicio: str = Field(..., description="Fecha de inicio (YYYY-MM-DD)")
    fecha_corte: str = Field(..., description="Fecha de corte (YYYY-MM-DD)")


class PredictRequest(BaseModel):
    """Modelo para la solicitud de predicción."""

    tick: str = Field(..., description="Símbolo de la acción")
    fecha_inicio: str = Field(
        ..., description="Fecha de inicio de la predicción (YYYY-MM-DD)"
    )
    fecha_fin: str = Field(
        ..., description="Fecha de fin de la predicción (YYYY-MM-DD)"
    )
    batch: bool = Field(
        False, description="Si es True, guarda las predicciones en formato parquet"
    )
    ruta: str = Field(
        None,
        description="Ruta de predicciones en formato parquet (requerido si batch=True)",
    )


class TrainResponse(BaseModel):
    """Modelo para la respuesta del entrenamiento."""

    tick: str
    metricas: Dict[str, float]
    mensaje: str


class PredictResponse(BaseModel):
    """Modelo para la respuesta de la predicción."""

    tick: str
    predicciones: Dict[str, Any]
    mensaje: str
    ruta_archivo: Optional[str]


@app.post("/train", response_model=TrainResponse)
async def train_model(request: TrainRequest) -> TrainResponse:
    """Endpoint para entrenar el modelo Prophet.

    Parameters
    ----------
    request : TrainRequest
        Datos de la solicitud de entrenamiento.

    Returns
    -------
    TrainResponse
        Respuesta con las métricas del entrenamiento.
    """
    logger.info(f"Recibida solicitud de entrenamiento para {request.tick}")

    try:
        # Validar fechas
        fecha_inicio = datetime.strptime(request.fecha_inicio, "%Y-%m-%d")
        fecha_corte = datetime.strptime(request.fecha_corte, "%Y-%m-%d")

        if fecha_inicio >= fecha_corte:
            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio debe ser anterior a la fecha de corte",
            )

        # Cargar datos
        logger.info(f"Cargando datos para {request.tick}")
        df = cargar_datos(request.tick, request.fecha_inicio, request.fecha_corte)

        # Entrenar modelo
        logger.info("Entrenando modelo")
        modelo, metricas = entrenar_prophet(df)

        # Guardar modelo
        logger.info("Guardando modelo")
        guardar_modelo(modelo, request.tick, metricas)

        return TrainResponse(
            tick=request.tick,
            metricas=metricas,
            mensaje="Modelo entrenado exitosamente",
        )

    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error durante el entrenamiento: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest) -> PredictResponse:
    """Endpoint para realizar predicciones con el modelo Prophet.

    Parameters
    ----------
    request : PredictRequest
        Datos de la solicitud de predicción.

    Returns
    -------
    PredictResponse
        Respuesta con las predicciones.
    """
    logger.info(f"Recibida solicitud de predicción para {request.tick}")

    try:
        # Validar fechas
        fecha_inicio = datetime.strptime(request.fecha_inicio, "%Y-%m-%d")
        fecha_fin = datetime.strptime(request.fecha_fin, "%Y-%m-%d")

        if fecha_inicio >= fecha_fin:
            raise HTTPException(
                status_code=400,
                detail="La fecha de inicio debe ser anterior a la fecha de fin",
            )

        # Validar parámetros de batch
        if request.batch and not request.ruta:
            raise HTTPException(
                status_code=400, detail="La ruta es requerida cuando batch=True"
            )

        # Cargar modelo
        logger.info(f"Cargando modelo para {request.tick}")
        modelo = cargar_modelo(request.tick)

        # Realizar predicción
        logger.info("Realizando predicción")
        predicciones = realizar_prediccion(
            modelo, request.fecha_inicio, request.fecha_fin
        )

        # Preparar respuesta según el modo batch
        if request.batch:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(request.ruta), exist_ok=True)

            fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = (
                f"predicciones_{request.tick}_{request.fecha_inicio}_"
                f"{request.fecha_fin}_{fecha_actual}.parquet"
            )
            # Guardar en formato parquet
            predicciones.to_parquet(os.path.join(request.ruta, file_name))
            logger.info(f"Predicciones guardadas en: {request.ruta}")

            return PredictResponse(
                tick=request.tick,
                predicciones={},
                mensaje="Predicción realizada y guardada exitosamente",
                ruta_archivo=request.ruta,
            )
        else:
            # Preparar diccionario de predicciones
            predicciones_dict = dict(
                zip(
                    predicciones["ds"].dt.strftime("%Y-%m-%d"),
                    predicciones["yhat"].round(2),
                )
            )

            return PredictResponse(
                tick=request.tick,
                predicciones=predicciones_dict,
                mensaje="Predicción realizada exitosamente",
                ruta_archivo=None,
            )

    except ValueError as e:
        logger.error(f"Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        logger.error(f"Modelo no encontrado: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error durante la predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Iniciar servidor
    uvicorn.run(app, host="0.0.0.0", port=8000)
