"""Pruebas para el módulo de entrenamiento."""
import os
import shutil

import numpy as np
import pandas as pd
import pytest

from src.pipeline.train import cargar_datos, entrenar_prophet, guardar_modelo

TEMP_DIR = "temp_test_models"


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Fixture para crear y eliminar carpeta temporal."""
    # Crear carpeta temporal antes de los tests
    os.makedirs(TEMP_DIR, exist_ok=True)
    yield
    # Eliminar carpeta temporal después de los tests
    shutil.rmtree(TEMP_DIR, ignore_errors=True)


@pytest.fixture
def datos_prueba():
    """Fixture para crear datos de prueba."""
    fechas = pd.date_range(start="2020-01-01", end="2020-12-31", freq="D")
    np.random.seed(42)
    precios = np.random.normal(100, 10, len(fechas)).cumsum()
    df = pd.DataFrame({"fecha": fechas, "precio_cierre": precios})
    return df


def test_cargar_datos(datos_prueba):
    """Prueba para cargar datos."""
    df = cargar_datos("TSLA", "2020-01-01", "2020-12-31")
    assert isinstance(df, pd.DataFrame)
    assert "ds" in df.columns
    assert "y" in df.columns
    assert len(df) > 0


def test_cargar_datos_fecha_invalida(datos_prueba):
    """Prueba para cargar datos con fechas inválidas."""
    with pytest.raises(ValueError):
        cargar_datos("TSLA", "2020-12-31", "2020-01-01")


def test_entrenar_prophet(datos_prueba):
    """Prueba para entrenar un modelo Prophet."""
    df = datos_prueba.rename(columns={"fecha": "ds", "precio_cierre": "y"})
    modelo, metricas = entrenar_prophet(df)
    assert modelo is not None
    assert isinstance(metricas, dict)
    assert "mse" in metricas
    assert "rmse" in metricas
    assert "mae" in metricas
    assert "r2" in metricas


def test_guardar_modelo(datos_prueba):
    """Prueba para guardar un modelo Prophet."""
    df = datos_prueba.rename(columns={"fecha": "ds", "precio_cierre": "y"})
    modelo, metricas = entrenar_prophet(df)
    guardar_modelo(modelo, "TSLA", metricas, TEMP_DIR)
    assert os.path.exists(os.path.join(TEMP_DIR, "prophet_TSLA.joblib"))
    assert os.path.exists(os.path.join(TEMP_DIR, "metricas_TSLA.json"))
