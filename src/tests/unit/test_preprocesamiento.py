"""Tests para las funciones de preprocesamiento."""
from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest


from pipeline.config import RUTA_AFP, RUTA_ORO, RUTA_TC, SERIE_AFP, SERIE_ORO, SERIE_TC

from pipeline.config import RUTA_AFP, RUTA_TC, RUTA_BONO, SERIE_AFP, SERIE_TC, SERIE_BONO


from pipeline.preprocesamiento import limpiar_datos_bcrp, obtener_datos_bcrp


@pytest.fixture
def mock_response_data_afp():
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
def sample_dataframe_afp():
    """Fixture con DataFrame de ejemplo para limpiar_datos_afp."""
    return pd.DataFrame(
        {
            "periodo": ["Mar.2023", "Abr.2023", "May.2023"],
            "valor": ["-10.9709", "-8.1139", "-6.0815"],
        }
    )


@pytest.fixture
def mock_response_data_tc():
    """Fixture con datos de ejemplo de la API de TC."""
    return {
        "config": {
            "title": "Tipo de cambio",
            "series": [
                {
                    "name": (
                        "Tipo de cambio - "
                        "TC Sistema bancario SBS (S/ por US$) - Compra"
                    ),
                    "dec": "3",
                }
            ],
        },
        "periods": [
            {"name": "05.Mar.25", "values": ["3.563"]},
            {"name": "06.Mar.25", "values": ["3.675"]},
            {"name": "07.Mar.25", "values": ["3.876"]},
        ],
    }


@pytest.fixture
def sample_dataframe_tc():
    """Fixture con DataFrame de ejemplo para limpiar_datos_tc."""
    return pd.DataFrame(
        {
            "periodo": ["05.Mar.25", "06.Mar.25", "07.Mar.25"],
            "valor": ["3.563", "3.675", "3.876"],
        }
    )


@pytest.fixture
def mock_response_data_oro():
    """Fixture con datos de ejemplo de la API de ARO."""
    return {
        "config": {
            "title": "Cotizaciones de productos (promedio del periodo)",
            "series": [
                {
                    "name": (
                        "Cotizaciones de productos (promedio del periodo) - "
                        "Oro - LME (US$ por onzas troy)"
                    ),
                    "dec": "0",
                }
            ],
        },
        "periods": [
            {"name": "Abr.2023", "values": ["2001.641"]},
            {"name": "May.2023", "values": ["1991.18"]},
            {"name": "Jun.2023", "values": ["1941.1"]},
        ],
    }

@pytest.fixture
def mock_response_data_bono():
    """Fixture con datos de ejemplo de la API de bonos."""
    return {
        "config": {
            "title": "Bonos del Tesoro",
            "series": [
                {
                    "name": "Tasa de interés de bonos del tesoro",
                    "dec": "3"
                }
            ],
        },
        "periods": [
            {"name": "Abr.2023", "values": ["2001.641"]},
            {"name": "May.2023", "values": ["1991.18"]},
            {"name": "Jun.2023", "values": ["1941.1"]},

            {"name": "05.Mar.25", "values": ["5.563"]},
            {"name": "06.Mar.25", "values": ["5.675"]},
            {"name": "07.Mar.25", "values": ["5.876"]},

            {"name": "05.Mar.25", "values": ["5.563"]},
            {"name": "06.Mar.25", "values": ["5.675"]},
            {"name": "07.Mar.25", "values": ["5.876"]},
        ]
    }


@pytest.fixture
def sample_dataframe_oro():
    """Fixture con DataFrame de ejemplo para limpiar_datos_oro."""
    return pd.DataFrame(
        {
            "periodo": ["Abr.2023", "May.2023", "Jun.2023"],
            "valor": ["2001.641", "1991.18", "941.1"],
    }
    )

def sample_dataframe_bono():
    """Fixture con DataFrame de ejemplo para limpiar_datos_bono."""
    return pd.DataFrame(
        {
            "periodo": ["05.Mar.25", "06.Mar.25", "07.Mar.25"],
            "valor": ["5.563", "5.675", "5.876"]
        }
    )


def test_obtener_datos_afp_success(mock_response_data_afp):
    """Test para obtener_datos_afp con respuesta exitosa."""
    # Mock de la respuesta HTTP
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data_afp
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        df = obtener_datos_bcrp(SERIE_AFP)

    # Verificar estructura del DataFrame
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["periodo", "valor"]
    assert len(df) == 3

    # Verificar datos
    assert df["periodo"].tolist() == ["Mar.2023", "Abr.2023", "May.2023"]
    assert df["valor"].tolist() == ["-10.9709", "-8.1139", "-6.0815"]


def test_obtener_datos_oro_success(mock_response_data_oro):
    """Test para obtener_datos_oro con respuesta exitosa."""
    # Mock de la respuesta HTTP
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data_oro
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        df = obtener_datos_bcrp(SERIE_ORO)

    # Verificar estructura del DataFrame
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["periodo", "valor"]
    assert len(df) == 3

    # Verificar datos
    assert df["periodo"].tolist() == ["Abr.2023", "May.2023", "Jun.2023"]
    assert df["valor"].tolist() == ["2001.641", "1991.18", "1941.1"]


def test_obtener_datos_tc_success(mock_response_data_tc):
    """Test para obtener_datos_tc con respuesta exitosa."""
    # Mock de la respuesta HTTP
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data_tc
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        df = obtener_datos_bcrp(SERIE_AFP)
        df = obtener_datos_bcrp(SERIE_TC)

    # Verificar estructura del DataFrame
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["periodo", "valor"]
    assert len(df) == 3

    # Verificar datos
    assert df["periodo"].tolist() == ["05.Mar.25", "06.Mar.25", "07.Mar.25"]
    assert df["valor"].tolist() == ["3.563", "3.675", "3.876"]


def test_obtener_datos_afp_http_error():
    """Test para obtener_datos_afp con error HTTP."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP Error"):
            obtener_datos_bcrp(SERIE_AFP)


def test_obtener_datos_tc_http_error():
    """Test para obtener_datos_tc con error HTTP."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP Error"):
            obtener_datos_bcrp(SERIE_TC)


def test_obtener_datos_oro_http_error():
    """Test para obtener_datos_oro con error HTTP."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP Error"):
            obtener_datos_bcrp(SERIE_ORO)


def test_limpiar_datos_afp(sample_dataframe_afp):
    """Test para limpiar_datos_afp con datos de ejemplo."""
    df_clean = limpiar_datos_bcrp(sample_dataframe_afp, True, False, RUTA_AFP)

    # Verificar estructura del DataFrame resultante
    assert isinstance(df_clean, pd.DataFrame)
    assert list(df_clean.columns) == [
        "periodo",
        "valor",
        "periodo_limpio",
        "valor_limpio",
    ]

    # Verificar tipos de datos
    assert df_clean["periodo_limpio"].dtype == "datetime64[ns]"
    assert df_clean["valor_limpio"].dtype == "float64"

    # Verificar transformaciones
    assert df_clean["valor_limpio"].tolist() == [-0.109709, -0.081139, -0.060815]

    # Verificar fechas
    expected_dates = [datetime(2023, 3, 1), datetime(2023, 4, 1), datetime(2023, 5, 1)]
    assert df_clean["periodo_limpio"].tolist() == expected_dates


def test_limpiar_datos_tc(sample_dataframe_tc):
    """Test para limpiar_datos_afp con datos de ejemplo."""
    df_clean = limpiar_datos_bcrp(sample_dataframe_tc, False, True, RUTA_TC)

    # Verificar estructura del DataFrame resultante
    assert isinstance(df_clean, pd.DataFrame)
    assert list(df_clean.columns) == [
        "periodo",
        "valor",
        "periodo_limpio",
        "valor_limpio",
    ]

    # Verificar tipos de datos
    assert df_clean["periodo_limpio"].dtype == "datetime64[ns]"
    assert df_clean["valor_limpio"].dtype == "float64"

    # Verificar transformaciones
    assert df_clean["valor_limpio"].tolist() == [3.563, 3.675, 3.876]

    # Verificar fechas
    expected_dates = [datetime(2025, 3, 5), datetime(2025, 3, 6), datetime(2025, 3, 7)]
    assert df_clean["periodo_limpio"].tolist() == expected_dates


def test_limpiar_datos_oro(sample_dataframe_oro):
    """Test para limpiar_datos_oro con datos de ejemplo."""
    df_clean = limpiar_datos_bcrp(sample_dataframe_oro, False, False, RUTA_ORO)

    # Verificar estructura del DataFrame resultante
    assert isinstance(df_clean, pd.DataFrame)
    assert list(df_clean.columns) == [
        "periodo",
        "valor",
        "periodo_limpio",
        "valor_limpio",
    ]

    # Verificar tipos de datos
    assert df_clean["periodo_limpio"].dtype == "datetime64[ns]"
    assert df_clean["valor_limpio"].dtype == "float64"

    # Verificar transformaciones
    assert df_clean["valor_limpio"].tolist() == [2001.641, 1991.18, 941.1]

    # Verificar fechas
    expected_dates = [datetime(2023, 4, 1), datetime(2023, 5, 1), datetime(2023, 6, 1)]
    assert df_clean["periodo_limpio"].tolist() == expected_dates


def test_limpiar_datos_afp_invalid_data():
    """Test para limpiar_datos_afp con datos inválidos."""
    invalid_df = pd.DataFrame(
        {
            "periodo": ["Invalid.2023", "Abr.2023"],
            "valor": ["not_a_number", "-8.1139"],
        }
    )

    with pytest.raises(ValueError):
        limpiar_datos_bcrp(invalid_df, True, False, RUTA_AFP)


def test_limpiar_datos_oro_invalid_data():
    """Test para limpiar_datos_oro con datos inválidos."""
    invalid_df = pd.DataFrame(
        {
            "periodo": ["Invalid.2023", "Abr.2023"],
            "valor": ["not_a_number", "2001.641"],
        }
    )

    with pytest.raises(ValueError):
        limpiar_datos_bcrp(invalid_df, False, False, RUTA_ORO)


def test_limpiar_datos_tc_invalid_data():
    """Test para limpiar_datos_tc con datos inválidos."""
    invalid_df = pd.DataFrame(
        {
            "periodo": ["05.Invalid.23", "06.Abr.23"],
            "valor": ["not_a_number", "3.113"],
        }
    )

    with pytest.raises(ValueError):
        limpiar_datos_bcrp(invalid_df, False, True, RUTA_TC)



def test_limpiar_datos_bcrp_missing_columns():
    """Test para limpiar_datos_bcrp con columnas faltantes."""
    invalid_df = pd.DataFrame(
        {
            "fecha": ["Abr.2023", "May.2023"],  # Falta la columna "periodo"
            "dato": ["2001.641", "1991.18"],  # Falta la columna "valor"
        }
    )

    with pytest.raises(
        ValueError,
        match=r"Se requieren las columnas" " {'periodo', 'valor'}|{'valor', 'periodo'}",
    ):
        limpiar_datos_bcrp(invalid_df, False, False)

def test_obtener_datos_bono_success(mock_response_data_bono):
    """Test para obtener_datos_bono con respuesta exitosa."""
    # Mock de la respuesta HTTP
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data_bono
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        df = obtener_datos_bcrp(SERIE_BONO)

    # Verificar estructura del DataFrame
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["periodo", "valor"]
    assert len(df) == 3

    # Verificar datos
    assert df["periodo"].tolist() == ["05.Mar.25", "06.Mar.25", "07.Mar.25"]
    assert df["valor"].tolist() == ["5.563", "5.675", "5.876"]


def test_obtener_datos_bono_http_error():
    """Test para obtener_datos_bono con error HTTP."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception, match="HTTP Error"):
            obtener_datos_bcrp(SERIE_BONO)


def test_limpiar_datos_bono(sample_dataframe_bono):
    """Test para limpiar_datos_bono con datos de ejemplo."""
    df_clean = limpiar_datos_bcrp(sample_dataframe_bono, False, True, RUTA_BONO)

    # Verificar estructura del DataFrame resultante
    assert isinstance(df_clean, pd.DataFrame)
    assert list(df_clean.columns) == [
        "periodo",
        "valor",
        "periodo_limpio",
        "valor_limpio",
    ]

    # Verificar tipos de datos
    assert df_clean["periodo_limpio"].dtype == "datetime64[ns]"
    assert df_clean["valor_limpio"].dtype == "float64"

    # Verificar transformaciones
    assert df_clean["valor_limpio"].tolist() == [5.563, 5.675, 5.876]

    # Verificar fechas
    expected_dates = [datetime(2025, 3, 5), datetime(2025, 3, 6), datetime(2025, 3, 7)]
    assert df_clean["periodo_limpio"].tolist() == expected_dates


def test_limpiar_datos_bono_invalid_data():
    """Test para limpiar_datos_bono con datos inválidos."""
    invalid_df = pd.DataFrame(
        {
            "periodo": ["05.Invalid.23", "06.Abr.23"],
            "valor": ["not_a_number", "5.113"],
        }
    )

    with pytest.raises(ValueError):
        limpiar_datos_bcrp(invalid_df, False, True, RUTA_BONO)
