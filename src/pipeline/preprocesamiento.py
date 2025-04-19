"""Funciones de preprocesamiento."""
from datetime import datetime

import pandas as pd
import requests

from .config import EQUIVALENCIAS_MESES, RUTA_AFP, URL_AFP


def obtener_datos_afp(url: str = URL_AFP) -> pd.DataFrame:
    """Descarga rendimientos mensuales de fondos de pensiones (AFP).

    Convierte la respuesta de la API en un ``pandas.DataFrame`` con las
    columnas ``periodo`` y ``rendimiento``.

    Parameters
    ----------
    url : str, optional
        URL de la API que expone los rendimientos mensuales por período.
        De forma predeterminada se usa la constante ``URL_AFP``.

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
        periodo  rendimiento
    0  ENE2024       0.0123
    """
    # Realizar la petición
    response = requests.get(url)
    response.raise_for_status()  # <‑‑ lanza HTTPError si falla

    # Convertir la respuesta JSON en diccionario de Python
    data = response.json()

    # Extraer períodos y rendimientos
    periodos = [period["name"] for period in data["periods"]]
    rendimientos = [period["values"][0] for period in data["periods"]]

    # Crear DataFrame y devolver
    df_afp = pd.DataFrame({"periodo": periodos, "rendimiento": rendimientos})
    return df_afp


def limpiar_datos_afp(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia y transforma los datos de AFP.

    Convierte el período a ``datetime``, pasa el rendimiento de
    porcentaje a proporción decimal y guarda las columnas limpias
    como CSV en ``RUTA_AFP``.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con las columnas ``periodo`` y ``rendimiento`` tal como
        las devuelve :func:`obtener_datos_afp`.

    Returns
    -------
    pd.DataFrame
        El mismo DataFrame de entrada, pero con dos columnas adicionales:

        * ``periodo_limpio`` – objeto ``datetime`` con el primer día del mes.
        * ``rendimiento_limpio`` – rendimiento mensual en proporción decimal.

    Raises
    ------
    ValueError
        Si el DataFrame no tiene las columnas requeridas o si los datos son inválidos.
    KeyError
        Si el formato del período no es válido.

    Examples
    --------
    >>> df_raw = obtener_datos_afp()
    >>> df_clean = limpiar_datos_afp(df_raw)
    >>> df_clean.dtypes
    periodo                      object
    rendimiento                  object
    periodo_limpio       datetime64[ns]
    rendimiento_limpio          float64
    dtype: object
    """
    # Verificar que el DataFrame tiene las columnas requeridas
    required_columns = ["periodo", "rendimiento"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"El DataFrame debe tener las columnas {required_columns}")

    def convertir_fecha(fecha_str: str) -> datetime:
        """Convierte una fecha en formato 'Mmm.YYYY' a datetime."""
        try:
            # Extraer mes y año
            mes_espanol = fecha_str[:3].upper()  # Primeros 3 caracteres en mayúsculas
            anio = fecha_str[4:]  # Todo después del punto

            # Verificar que el mes existe en el diccionario
            if mes_espanol not in EQUIVALENCIAS_MESES:
                raise KeyError(f"Mes no válido: {mes_espanol}")

            mes_ingles = EQUIVALENCIAS_MESES[mes_espanol]
            fecha_ingles = f"{mes_ingles} {anio}"
            return datetime.strptime(fecha_ingles, "%b %Y")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Formato de fecha no válido: {fecha_str}") from e

    try:
        # Transformación de columnas
        df["periodo_limpio"] = df["periodo"].apply(convertir_fecha)
        df["rendimiento_limpio"] = (
            pd.to_numeric(df["rendimiento"], errors="coerce") / 100
        )

        df["rendimiento_limpio"] = df["rendimiento_limpio"].round(6)

        # Verificar si hay valores nulos después de la conversión
        if df["rendimiento_limpio"].isnull().any():
            raise ValueError(
                "Algunos valores de rendimiento no pudieron ser convertidos a números"
            )

        # Guardar CSV con las columnas limpias
        df[["periodo_limpio", "rendimiento_limpio"]].to_csv(RUTA_AFP, index=False)

        return df
    except Exception as e:
        raise ValueError(f"Error al limpiar los datos: {str(e)}") from e
