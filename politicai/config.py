"""Rutas del proyecto."""

import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Los datos de entrada no se versionan (ver data/README.md). Se puede apuntar a
# otra carpeta con la variable de entorno POLITICAI_DATA_DIR.
DATA_DIR = Path(os.environ.get("POLITICAI_DATA_DIR", RAIZ / "data"))
RAW_DIR = DATA_DIR / "raw"
STAGING_DIR = DATA_DIR / "staging"

DOCS_DIR = RAIZ / "docs"
RESULTADOS_DIR = RAIZ / "resultados"
