"""Funciones de preprocesamiento para datos del BCRP."""
from datetime import datetime

import pandas as pd
import requests

from .config import EQUIVALENCIAS_MESES, SERIE_AFP, SERIE_BONO, URL_BCRP


def obtener_datos_afp() -> pd.DataFrame:
    """Descarga datos de rendimientos de AFP del BCRP.

    Returns
    -------
    pd.DataFrame
        DataFrame con:
        * ``periodo`` – Identificador del período (por ejemplo, ``'Mar.2023'``).
        * ``valor`` – Rendimiento mensual como string (porcentaje).

    Raises
    ------
    requests.HTTPError
        Si la petición a la API devuelve un código de estado distinto de 200.

    Examples
    --------
    >>> df = obtener_datos_afp()
    >>> df.head()
        periodo  valor
    0  Mar.2023  -10.9709
    """
    return obtener_datos_bcrp(SERIE_AFP)


def obtener_datos_bono() -> pd.DataFrame:
    """Descarga datos de tasas de bonos del BCRP.

    Returns
    -------
    pd.DataFrame
        DataFrame con:
        * ``periodo`` – Identificador del período (por ejemplo, ``'05.Mar.25'``).
        * ``valor`` – Tasa de interés como string.

    Raises
    ------
    requests.HTTPError
        Si la petición a la API devuelve un código de estado distinto de 200.

    Examples
    --------
    >>> df = obtener_datos_bono()
    >>> df.head()
        periodo  valor
    0  05.Mar.25  5.563
    """
    return obtener_datos_bcrp(SERIE_BONO)


def obtener_datos_bcrp(serie: str) -> pd.DataFrame:
    """Descarga datos del BCRP.

    Convierte la respuesta de la API en un ``pandas.DataFrame`` con las
    columnas ``periodo`` y ``valor``.

    Parameters
    ----------
    serie : str
        Código de la serie del BCRP.

    Returns
    -------
    pd.DataFrame
        DataFrame con:
        * ``periodo`` – Identificador del período.
        * ``valor`` – Valor de la serie como string.

    Raises
    ------
    requests.HTTPError
        Si la petición a la API devuelve un código de estado distinto de 200.
    """
    # Realizar la petición
    url = URL_BCRP + serie
    response = requests.get(url)
    response.raise_for_status()  # <‑‑ lanza HTTPError si falla

    # Convertir la respuesta JSON en diccionario de Python
    data = response.json()

    # Extraer períodos y valores
    periodos = [period["name"] for period in data["periods"]]
    valores = [period["values"][0] for period in data["periods"]]

    # Crear DataFrame y devolver
    df = pd.DataFrame({"periodo": periodos, "valor": valores})
    return df


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
        mes_es = fecha_str[:3].upper()
        anio = fecha_str[4:]
        mes_en = EQUIVALENCIAS_MESES[mes_es]  # KeyError si no existe
        return datetime.strptime(f"{mes_en} {anio}", "%b %Y")
    except (KeyError, ValueError, IndexError) as exc:
        raise ValueError(f"Formato de fecha mensual no válido: {fecha_str}") from exc


def limpiar_datos_bcrp(
    df: pd.DataFrame,
    porcentual: bool = True,
    diaria: bool = False,
    ruta: str | None = None,
) -> pd.DataFrame:
    """Limpia y estandariza los datos descargados del BCRP.

    La función valida el `DataFrame`, convierte la columna ``periodo`` a
    ``datetime`` (diaria o mensual) y normaliza ``valor``:
    - Si `porcentual=True`, el valor se divide entre 100 → proporción.
    - Si `porcentual=False`, se asume que ya está en unidades deseadas.

    Finalmente, si `ruta` es distinta de ``None`` se exportan las columnas
    limpias a CSV.

    Parameters
    ----------
    df : pd.DataFrame
        Datos crudos con las columnas ``periodo`` y ``valor``.
    porcentual : bool, default ``True``
        Indica si los valores de ``valor`` vienen como porcentaje.
        - ``True`` para datos de AFP (rendimientos en porcentaje)
        - ``False`` para datos de bonos (tasas directas)
    diaria : bool, default ``False``
        `True` → la fecha es diaria («dd Mmm.aa»), usado para bonos
        `False` → la fecha es mensual («Mmm.aaaa»), usado para AFP
    ruta : str | None, default ``None``
        Ruta del archivo CSV a generar.  Si es ``None`` no se guarda.

    Returns
    -------
    pd.DataFrame
        El mismo `DataFrame` con dos columnas nuevas:
        * ``periodo_limpio`` – objeto ``datetime``.
        * ``valor_limpio`` – número ``float`` limpio.

    Raises
    ------
    ValueError
        Si faltan columnas requeridas o el formato es inválido.

    Examples
    --------
    >>> # Para datos de AFP
    >>> df_afp = obtener_datos_afp()
    >>> df_limpio = limpiar_datos_bcrp(df_afp, porcentual=True, diaria=False)
    >>> df_limpio.head()
        periodo  valor  periodo_limpio  valor_limpio
    0  Mar.2023  -10.9709  2023-03-01  -0.109709

    >>> # Para datos de bonos
    >>> df_bono = obtener_datos_bono()
    >>> df_limpio = limpiar_datos_bcrp(df_bono, porcentual=False, diaria=True)
    >>> df_limpio.head()
        periodo  valor  periodo_limpio  valor_limpio
    0  05.Mar.25  5.563  2025-03-05  5.563
    """
    columnas_requeridas = {"periodo", "valor"}
    if not columnas_requeridas.issubset(df.columns):
        raise ValueError(f"Se requieren las columnas {columnas_requeridas}")

    # Conversión de fechas
    convertir = _fecha_diaria if diaria else _fecha_mensual
    df = df.copy()  # evita modificar el original
    df["periodo_limpio"] = df["periodo"].apply(convertir)

    # Limpieza de valores
    valores = pd.to_numeric(df["valor"], errors="coerce")
    df["valor_limpio"] = (valores / 100 if porcentual else valores).round(6)

    # Exportar si se solicita
    if ruta:
        df[["periodo_limpio", "valor_limpio"]].to_csv(ruta, index=False)

    return df
