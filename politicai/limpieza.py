"""Normalización de nombres de columnas y de países en las tablas de entrada."""

import unicodedata

import pandas as pd


def _quitar_tildes(texto):
    return unicodedata.normalize("NFKD", texto).encode("ascii", errors="ignore").decode("utf-8")


def clean_column_names(df):
    """Convierte las columnas a snake_case ASCII: 'Nombre de Provincia' -> 'nombre_de_provincia'.

    Pensada para los ficheros del Ministerio del Interior, cuyas cabeceras
    llevan tildes, espacios y signos de puntuación.
    """
    columnas = []
    for col in df.columns:
        col = _quitar_tildes(str(col)).strip().lower().replace(" ", "_")
        for caracter in ":().":
            col = col.replace(caracter, "")
        columnas.append(col.replace("-", "_"))
    df.columns = columnas
    return df


def clean_df_format(df):
    """Versión ligera de clean_column_names para las tablas internacionales (en inglés)."""
    df.columns = [
        x.lower().replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "").strip()
        for x in df.columns
    ]
    return df


# Nombres de país que cada fuente escribe de forma distinta, unificados al que
# usamos para cruzar tablas.
NOMBRES_PAISES = {
    "korea_north": "north_korea",
    "korea_dem_people’s_rep": "north_korea",
    "korea_dem_peoples_republic_of": "north_korea",
    "korea_south": "south_korea",
    "korea_rep": "south_korea",
    "korea_republic_of": "south_korea",
    "moldova_republic_of": "moldova",
    "cape_verde": "cabo_verde",
    "syrian_arab_republic": "syria",
    "venezuela_rb": "venezuela",
    "macedonia": "north_macedonia",
    "north_macedonia_republic_of_": "north_macedonia",
    "serbia_montenegro": "serbia",
    "slovak_republic": "slovakia",
    "dem_rep_of_congo": "congo_kinshasa",
    "congo_dem_rep": "congo_kinshasa",
    "congo_democratic_republic_of": "congo_kinshasa",
    "congo_rep": "congo_brazzaville",
    "republic_of_the_congo_brazzaville": "congo_brazzaville",
    "tanzania_united_republic_of": "tanzania",
    "egypt_arab_rep": "egypt",
    "gambia_the": "gambia",
    "the_gambia": "gambia",
    "russian_federation": "russia",
    "iran_islamic_rep": "iran",
    "iran_islamic_republic_of": "iran",
    "yemen_rep": "yemen",
    "kyrgyz_republic": "kyrgyzstan",
    "viet_nam": "vietnam",
    "lao_pdr": "laos",
    "lao_peoples_dem_republic": "laos",
    "bahamas_the": "bahamas",
    "brunei_darussalam": "brunei",
    "sudan_north": "sudan",
    "hong_kong_sar_china": "hong_kong",
}


def clean_country_names(df, column, new_country_col_name="country"):
    """Normaliza los nombres de país de `column` y renombra la columna a `new_country_col_name`.

    Pasa a minúsculas, elimina puntuación, cambia espacios por guiones bajos y
    aplica NOMBRES_PAISES para que las distintas fuentes se puedan cruzar.
    """
    nombres = df[column].str.lower()
    for caracter in ["(", ")", "&", ".", ",", "'"]:
        nombres = nombres.str.replace(caracter, "", regex=False)
    nombres = (
        nombres.str.replace("-", " ", regex=False)
        .str.replace(" ", "_", regex=False)
        .str.replace("__", "_", regex=False)
    )
    df = df.copy()
    df[column] = nombres.replace(NOMBRES_PAISES)
    return df.rename(columns={column: new_country_col_name})


def ultimo_valor_por_grupo(df, grupo, orden="year"):
    """Devuelve, para cada valor de `grupo`, la fila con el `orden` más reciente."""
    return df.sort_values([grupo, orden], ascending=False).groupby(grupo).head(1)


def melt_banco_mundial(df, nombre_valor):
    """Pasa una tabla del Banco Mundial (un año por columna) a formato largo.

    Devuelve las columnas country_name, code_wb, year y `nombre_valor`.
    """
    largo = pd.melt(df, id_vars=["country_name", "country_code"], value_vars=df.columns[4:])
    largo = largo.rename(columns={"country_code": "code_wb", "variable": "year", "value": nombre_valor})
    largo["year"] = largo["year"].astype(int)
    return largo[["country_name", "code_wb", "year", nombre_valor]]
