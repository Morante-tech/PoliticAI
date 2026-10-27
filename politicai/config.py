"""Rutas del proyecto y publicación opcional de gráficos en Chart Studio."""

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


def publicar_en_chart_studio(fig, nombre):
    """Sube una figura de Plotly a Chart Studio, si hay credenciales configuradas.

    Las credenciales se leen de las variables de entorno CHART_STUDIO_USERNAME y
    CHART_STUDIO_API_KEY; nunca deben escribirse en el código. Sin ellas, la
    función no hace nada.
    """
    usuario = os.environ.get("CHART_STUDIO_USERNAME")
    api_key = os.environ.get("CHART_STUDIO_API_KEY")
    if not (usuario and api_key):
        print(f"Chart Studio no configurado; no se publica '{nombre}'.")
        return None

    import chart_studio
    import chart_studio.plotly as py

    chart_studio.tools.set_credentials_file(username=usuario, api_key=api_key)
    return py.plot(fig, filename=nombre, auto_open=False)
