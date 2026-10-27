# PoliticAI

Análisis de datos políticos y electorales de España y del mundo, con el código en notebooks de Jupyter y los mapas interactivos publicados en GitHub Pages.

## Análisis

| Notebook | Pregunta |
|---|---|
| [01 · Elecciones en Madrid](notebooks/01_resultados_elecciones_madrid.ipynb) | ¿Qué partido ganó en cada municipio de la Comunidad de Madrid en cada elección general desde 1977? |
| [02 · Región influyente](notebooks/02_region_influyente.ipynb) | ¿En qué provincias se quedó un partido a pocos votos del último escaño en noviembre de 2019? ¿Lo habría ganado con los votos que perdió desde abril? |
| [03 · Programas electorales](notebooks/03_programas_electorales.ipynb) | ¿Cuánto hablan los programas de 2019 de los problemas que más preocupan según el CIS? |
| [04 · Gobierno mundial](notebooks/04_gobierno_mundial.ipynb) | ¿Qué países son más prósperos según un índice propio (IPR) y cuántos parlamentarios necesitaría un gobierno mundial? |
| [05 · Gobiernos autoritarios](notebooks/05_gobiernos_autoritarios.ipynb) | ¿Cómo han cambiado los derechos políticos y las libertades civiles entre 2013 y 2020? |

## Resultados publicados

- **Mapas de ganadores por municipio en Madrid (1977-2019)**: [`docs/elecciones_madrid/`](docs/elecciones_madrid/). Se generan con el notebook 01.
- **Nubes de palabras de los programas electorales**: [`docs/img/nubes_palabras/`](docs/img/nubes_palabras/).
- **Tablas** en [`resultados/`](resultados/):
  - [`dhondt_last_line.csv`](resultados/dhondt_last_line.csv): votos que le faltaron al bloque contrario a la investidura para el último escaño de cada provincia (notebook 02).
  - [`cis_nov_19.csv`](resultados/cis_nov_19.csv): diez principales problemas de los españoles según el CIS de noviembre de 2019 (notebook 03).
  - [`top_10_ipr.csv`](resultados/top_10_ipr.csv): diez países más prósperos según el Índice de Prosperidad Relativa (notebook 04).

## Estructura

```
├── notebooks/     análisis, uno por artículo
├── politicai/     funciones compartidas (limpieza de datos, ley d'Hondt, texto)
├── data/          datos de entrada (no se versionan; ver data/README.md)
├── resultados/    tablas generadas por los análisis
└── docs/          web estática para GitHub Pages (mapas e imágenes)
```

## Cómo ejecutarlo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/
```

Los datos de entrada son públicos, pero no se incluyen en el repositorio. En [`data/README.md`](data/README.md) se explica de dónde descargar cada fichero y dónde colocarlo. Si los tienes en otra carpeta, indícala con la variable de entorno `POLITICAI_DATA_DIR`.

Para subir los gráficos a [Chart Studio](https://chart-studio.plotly.com/), define `CHART_STUDIO_USERNAME` y `CHART_STUDIO_API_KEY` y descomenta las llamadas a `publicar_en_chart_studio`. No es necesario para ejecutar los análisis.

## Licencia

[MIT](LICENSE).
