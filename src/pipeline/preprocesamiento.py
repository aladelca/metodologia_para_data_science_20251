"""Funciones de preprocesamiento."""
from datetime import datetime
from typing import Optional

import pandas as pd
import requests
import yfinance as yf

from .config import EQUIVALENCIAS_MESES, URL_BCRP


def obtener_datos_bcrp(serie: str) -> pd.DataFrame:
    """Descarga datos del BCRP.

    Convierte la respuesta de la API en un ``pandas.DataFrame`` con las
    columnas ``periodo`` y ``rendimiento``.

    Parameters
    ----------
    url : str, optional
        URL de la API que expone los rendimientos mensuales por período.
        Se usa la url base URL_BCRP.

    Returns
    -------
    pd.DataFrame
        DataFrame con:

        * ``periodo`` – Identificador del período (por ejemplo, ``'ENE2024'``).
        * ``rendimiento`` – Rendimiento mensual como *float* (porcentaje).

    Raises
    ------
    requests.HTTPError
        Si la petición a la API devuelve un código de estado distinto de 200.

    Examples
    --------
    >>> df = obtener_datos_afp()
    >>> df.head()
        periodo  valor
    0  ENE2024       0.0123
    """
    # Realizar la petición
    url = URL_BCRP + serie
    response = requests.get(url)
    response.raise_for_status()  # <‑‑ lanza HTTPError si falla

    # Convertir la respuesta JSON en diccionario de Python
    data = response.json()

    # Extraer períodos y rendimientos
    periodos = [period["name"] for period in data["periods"]]
    valores = [period["values"][0] for period in data["periods"]]

    # Crear DataFrame y devolver
    df_afp = pd.DataFrame({"periodo": periodos, "valor": valores})
    return df_afp


def _fecha_diaria(fecha_str: str) -> datetime:
    """Convierte «dd Mmm.aa» (p. ej. ``'05 Mar.25'``) a ``datetime``."""
    try:
        dia = fecha_str[0:2]
        mes_es = fecha_str[3:6].upper()
        anio = fecha_str[7:]
        mes_en = EQUIVALENCIAS_MESES[mes_es]  # KeyError si no existe
        return datetime.strptime(f"{dia} {mes_en} {anio}", "%d %b %y")
    except (KeyError, ValueError, IndexError) as exc:
        raise ValueError(f"Formato de fecha diaria no válido: {fecha_str}") from exc


def _fecha_mensual(fecha_str: str) -> datetime:
    """Convierte «Mmm.aaaa» (p. ej. ``'Mar.2025'``) a ``datetime``."""
    try:
        try:
            mes_es = fecha_str[:3].upper()
            anio = fecha_str[4:]
            mes_en = EQUIVALENCIAS_MESES[mes_es]  # KeyError si no existe
            return datetime.strptime(f"{mes_en} {anio}", "%b %Y")
        except ValueError:
            mes_es = fecha_str[:3].upper()
            anio = fecha_str[3:]
            mes_en = EQUIVALENCIAS_MESES[mes_es]  # KeyError si no existe
            return datetime.strptime(f"{mes_en}{anio}", "%b%y")
    except (KeyError, ValueError, IndexError) as exc:
        raise ValueError(f"Formato de fecha mensual no válido: {fecha_str}") from exc


# función pública ──────────────────────────────────────────────────────────────
def limpiar_datos_bcrp(
    df: pd.DataFrame,
    porcentual: bool = True,
    diaria: bool = False,
    ruta: Optional[str] = None,  # Cambiado a Optional[str]
) -> pd.DataFrame:
    """Limpia y estandariza los datos descargados del BCRP.

    La función valida el `DataFrame`, convierte la columna ``periodo`` a
    ``datetime`` (diaria o mensual) y normaliza ``rendimiento``:
    - Si `porcentual=True`, el rendimiento se divide entre 100 → proporción.
    - Si `porcentual=False`, se asume que ya está en unidades deseadas.

    Finalmente, si `ruta` es distinta de ``None`` se exportan las columnas
    limpias a CSV.

    Parameters
    ----------
    df : pd.DataFrame
        Datos crudos con las columnas ``periodo`` y ``valor``.
    porcentual : bool, default ``True``
        Indica si los valores de ``valor`` vienen como porcentaje.
    diaria : bool, default ``False``
        `True` → la fecha es diaria («dd Mmm.aa»),
        `False` → la fecha es mensual («Mmm.aaaa»).
    ruta : str | None, default ``None``
        Ruta del archivo CSV a generar.  Si es ``None`` no se guarda.

    Returns
    -------
    pd.DataFrame
        El mismo `DataFrame` con dos columnas nuevas:

        * ``periodo`` – objeto ``datetime``.
        * ``valor`` – número ``float`` limpio.

    Raises
    ------
    ValueError
        Si faltan columnas requeridas o el formato es inválido.
    """
    columnas_requeridas = {"periodo", "valor"}
    if not columnas_requeridas.issubset(df.columns):
        raise ValueError(f"Se requieren las columnas {columnas_requeridas}")

    # Conversión de fechas
    convertir = _fecha_diaria if diaria else _fecha_mensual
    df = df.copy()  # evita modificar el original
    df["periodo_limpio"] = df["periodo"].apply(convertir)

    # Limpieza de rendimiento
    rend = pd.to_numeric(df["valor"], errors="coerce")
    df["valor_limpio"] = round(rend / 100, 6) if porcentual else round(rend, 6)

    # Exportar si se solicita
    if ruta:
        df[["periodo_limpio", "valor_limpio"]].to_csv(ruta, index=False)

    return df


def obtener_datos_yfinance(
    ticker: list[str], fecha_inicio: str, fecha_fin: str
) -> pd.DataFrame:
    """Obtiene los datos de los tickers de yfinance.

    Parameters
    ----------
    ticker : list[str]
        Lista de tickers de yfinance.

    Returns
    -------
    pd.DataFrame
        DataFrame con los datos de los tickers de yfinance.
    """
    df = yf.download(ticker, start=fecha_inicio, end=fecha_fin)

    # Seleccionar solamente los precios al cierre del día
    df = df.Close

    return df
