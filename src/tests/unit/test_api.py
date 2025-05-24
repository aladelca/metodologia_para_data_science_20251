"""Pruebas para el módulo de API."""
import os
import shutil

import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from prophet import Prophet

from pipeline.api import app
from pipeline.train import guardar_modelo


@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba."""
    return TestClient(app)


@pytest.fixture
def datos_prueba():
    """Fixture para crear datos de prueba."""
    # Crear fechas
    fechas = pd.date_range(start="2020-01-01", end="2020-12-31", freq="D")

    # Crear datos sintéticos
    np.random.seed(42)
    precios = np.random.normal(100, 10, len(fechas)).cumsum()

    # Crear DataFrame
    df = pd.DataFrame({"fecha": fechas, "precio_cierre": precios})

    return df


@pytest.fixture
def modelo_prueba():
    """Fixture para crear un modelo de prueba."""
    # Crear datos sintéticos
    fechas = pd.date_range(start="2020-01-01", end="2020-12-31", freq="D")
    np.random.seed(42)
    valores = np.random.normal(100, 10, len(fechas)).cumsum()

    # Crear DataFrame para Prophet
    df = pd.DataFrame({"ds": fechas, "y": valores})

    # Entrenar modelo simple
    modelo = Prophet()
    modelo.fit(df)

    return modelo


@pytest.fixture
def directorio_temporal():
    """Fixture para crear un directorio temporal para pruebas."""
    # Crear directorio temporal
    temp_dir = "temp_test"
    os.makedirs(temp_dir, exist_ok=True)

    yield temp_dir

    # Limpiar después de las pruebas
    shutil.rmtree(temp_dir)


def test_train_endpoint(client, datos_prueba, directorio_temporal):
    """Prueba el endpoint de entrenamiento."""
    # Preparar datos de prueba
    ruta_archivo = os.path.join(directorio_temporal, "AAPL.csv")
    datos_prueba.to_csv(ruta_archivo, index=False)

    # Realizar solicitud de entrenamiento
    response = client.post(
        "/train",
        json={
            "tick": "TSLA",
            "fecha_inicio": "2020-01-01",
            "fecha_corte": "2020-12-31",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["tick"] == "TSLA"
    assert "metricas" in data
    assert "mensaje" in data


def test_train_endpoint_fechas_invalidas(client):
    """Prueba el endpoint de entrenamiento con fechas inválidas."""
    response = client.post(
        "/train",
        json={
            "tick": "TSLA",
            "fecha_inicio": "2020-12-31",
            "fecha_corte": "2020-01-01",
        },
    )

    assert response.status_code == 500


def test_predict_endpoint(client, modelo_prueba, directorio_temporal):
    """Prueba el endpoint de predicción."""
    # Guardar modelo de prueba
    metricas = {"mse": 0.0, "rmse": 0.0, "mae": 0.0, "r2": 1.0}
    guardar_modelo(modelo_prueba, "TSLA", metricas)

    # Realizar solicitud de predicción
    response = client.post(
        "/predict",
        json={
            "tick": "TSLA",
            "fecha_inicio": "2021-01-01",
            "fecha_fin": "2021-01-31",
            "batch": False,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["tick"] == "TSLA"
    assert "predicciones" in data
    assert "mensaje" in data
    assert data["ruta_archivo"] is None


def test_predict_endpoint_modelo_no_existe(client):
    """Prueba el endpoint de predicción con un modelo que no existe."""
    response = client.post(
        "/predict",
        json={
            "tick": "MODELO_INEXISTENTE",
            "fecha_inicio": "2021-01-01",
            "fecha_fin": "2021-01-31",
            "batch": False,
        },
    )

    assert response.status_code == 404
