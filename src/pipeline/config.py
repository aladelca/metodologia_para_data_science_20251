"""Config file para el preprocesamiento."""
from pathlib import Path

# Obtener la ruta absoluta del directorio del proyecto
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "src" / "data" / "raw"

# Asegurar que el directorio existe
DATA_DIR.mkdir(parents=True, exist_ok=True)

URL_BCRP = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
SERIE_AFP = "PN01178MM/json"
SERIE_TC = "PD04639PD/json"
SERIE_ORO = "PN01654XM/json"
# Diccionario de equivalencias de meses (en mayúsculas)
EQUIVALENCIAS_MESES = {
    "ENE": "Jan",
    "FEB": "Feb",
    "MAR": "Mar",
    "ABR": "Apr",
    "MAY": "May",
    "JUN": "Jun",
    "JUL": "Jul",
    "AGO": "Aug",
    "SEP": "Sep",
    "OCT": "Oct",
    "NOV": "Nov",
    "DIC": "Dec",
}

# Ruta absoluta para el archivo AFP
RUTA_AFP = str(DATA_DIR / "afp.csv")
RUTA_TC = str(DATA_DIR / "tc.csv")
RUTA_ORO = str(DATA_DIR / "oro.csv")
