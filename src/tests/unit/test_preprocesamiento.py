"""Tests para las funciones de preprocesamiento."""
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from pipeline.preprocesamiento import limpiar_datos_afp, obtener_datos_afp


@pytest.fixture
def mock_response_data():
    """Fixture con datos de ejemplo de la API de AFP."""
    return {
        "config": {
            "title": "Sistema privado de pensiones",
            "series": [
                {
                    "name": (
                        "Sistema privado de pensiones - "
                        "Rentabilidad Real Últimos 12 meses"
                    ),
                    "dec": "1",
                }
            ],
        },
        "periods": [
            {"name": "Mar.2023", "values": ["-10.9709"]},
            {"name": "Abr.2023", "values": ["-8.1139"]},
            {"name": "May.2023", "values": ["-6.0815"]},
        ],
    }


@pytest.fixture
def sample_dataframe():
    """Fixture con DataFrame de ejemplo para limpiar_datos_afp."""
    return pd.DataFrame(
        {
            "periodo": ["Mar.2023", "Abr.2023", "May.2023"],
            "rendimiento": ["-10.9709", "-8.1139", "-6.0815"],
        }
    )


def test_obtener_datos_afp_success(mock_response_data):
    """Test para obtener_datos_afp con respuesta exitosa."""
    # Mock de la respuesta HTTP
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        df = obtener_datos_afp()

    # Verificar estructura del DataFrame
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["periodo", "rendimiento"]
    assert len(df) == 3

    # Verificar datos
    assert df["periodo"].tolist() == ["Mar.2023", "Abr.2023", "May.2023"]
    assert df["rendimiento"].tolist() == ["-10.9709", "-8.1139", "-6.0815"]


def test_obtener_datos_afp_http_error():
    """Test para obtener_datos_afp con error HTTP."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP Error"):
            obtener_datos_afp()


def test_limpiar_datos_afp(sample_dataframe):
    """Test para limpiar_datos_afp con datos de ejemplo."""
    df_clean = limpiar_datos_afp(sample_dataframe)

    # Verificar estructura del DataFrame resultante
    assert isinstance(df_clean, pd.DataFrame)
    assert list(df_clean.columns) == [
        "periodo",
        "rendimiento",
        "periodo_limpio",
        "rendimiento_limpio",
    ]

    # Verificar tipos de datos
    assert df_clean["periodo_limpio"].dtype == "datetime64[ns]"
    assert df_clean["rendimiento_limpio"].dtype == "float64"

    # Verificar transformaciones
    assert df_clean["rendimiento_limpio"].tolist() == [-0.109709, -0.081139, -0.060815]

    # Verificar fechas
    expected_dates = [datetime(2023, 3, 1), datetime(2023, 4, 1), datetime(2023, 5, 1)]
    assert df_clean["periodo_limpio"].tolist() == expected_dates


def test_limpiar_datos_afp_invalid_data():
    """Test para limpiar_datos_afp con datos inválidos."""
    invalid_df = pd.DataFrame(
        {
            "periodo": ["Invalid.2023", "Abr.2023"],
            "rendimiento": ["not_a_number", "-8.1139"],
        }
    )

    with pytest.raises(ValueError):
        limpiar_datos_afp(invalid_df)
