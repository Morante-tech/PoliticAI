"""Carga de resultados electorales del Ministerio del Interior y reparto de escaños."""

import glob
import os

import pandas as pd

from politicai.limpieza import clean_column_names

# Columnas descriptivas de los ficheros de resultados por municipio; el resto
# son partidos (votos por candidatura).
COLUMNAS_CLAVE_MUNICIPIO = [
    "nombre_de_comunidad", "codigo_de_provincia", "nombre_de_provincia",
    "codigo_de_municipio", "nombre_de_municipio", "poblacion",
    "numero_de_mesas", "total_censo_electoral", "total_votantes",
    "votos_validos", "votos_a_candidaturas", "votos_en_blanco", "votos_nulos",
    "year", "month", "yearmonth", "CODIGOINE",
]

# Columnas descriptivas de los ficheros de resultados por provincia.
COLUMNAS_CLAVE_PROVINCIA = [
    "nombre_de_comunidad", "codigo_de_provincia", "nombre_de_provincia",
    "poblacion", "numero_de_mesas", "censo_electoral_sin_cera", "censo_cera",
    "total_censo_electoral", "solicitudes_voto_cera_aceptadas", "total_votantes_cer",
    "total_votantes_cera", "total_votantes", "votos_validos", "votos_a_candidaturas",
    "votos_en_blanco", "votos_nulos",
]

# La misma formación aparece con nombres distintos según la elección.
NOMBRES_PARTIDOS = {
    "cs": "ciudadanos",
    "c's": "ciudadanos",
    "psoe_progr": "psoe",
}

# Colores por partido para los gráficos (claves = nombres de columna normalizados).
COLORES_PARTIDOS = {
    "ucd": "#FFA07A",
    "psoe": "#E52B50",
    "pp": "#1E90FF",
    "ap": "#FFFF00",
    "ap_pdp": "#FFFF00",
    "ap_pdp_pl": "#FFFF00",
    "pce": "#FF0000",
    "uce": "#FF0000",
    "pcoe": "#FF0000",
    "pst": "#FF0000",
    "cds": "#66CDAA",
    "iu": "#32CD32",
    "fe": "#000000",
    "ciudadanos": "#FFA500",
    "podemos": "#9370DB",
    "podemos_iu": "#9370DB",
    "podemos_iu_equo": "#9370DB",
    "vox": "#00FF00",
}


def cargar_elecciones_municipio(carpeta):
    """Une todos los Excel de resultados por municipio de `carpeta` en una única tabla.

    Los ficheros son los de infoelectoral.interior.gob.es, cuyo nombre lleva la
    fecha de la elección (p. ej. ``02_201911_1.xlsx`` -> noviembre de 2019). Se
    añaden las columnas year, month, yearmonth y CODIGOINE (código INE de 5
    dígitos: provincia + municipio).
    """
    from tqdm.auto import tqdm

    tablas = []
    for fichero in tqdm(sorted(glob.glob(os.path.join(carpeta, "*.xlsx")))):
        nombre = os.path.splitext(os.path.basename(fichero))[0]
        year, month = nombre[3:7], nombre[7:9]
        df = pd.read_excel(fichero, header=1, skiprows=4)
        df["year"] = int(year)
        df["month"] = int(month)
        df["yearmonth"] = year + month
        df = clean_column_names(df).rename(columns=NOMBRES_PARTIDOS)
        tablas.append(df)

    df = pd.concat(tablas, axis=0, ignore_index=True, sort=False)
    df = df[[c for c in df.columns if "unnamed" not in c]].fillna(0)
    df["CODIGOINE"] = (
        df["codigo_de_provincia"].astype(int).astype(str).str.zfill(2)
        + df["codigo_de_municipio"].astype(int).astype(str).str.zfill(3)
    )
    return df


def columnas_partidos(df, columnas_clave=COLUMNAS_CLAVE_MUNICIPIO):
    """Devuelve las columnas de `df` que corresponden a partidos."""
    return [c for c in df.columns if c not in columnas_clave]


def calculate_dhondt(df_row_votes, party_columns, n_seats, min_per=0.03):
    """Reparte `n_seats` escaños entre partidos con la ley d'Hondt.

    Parámetros
    ----------
    df_row_votes : DataFrame de una sola fila con los votos de cada partido.
    party_columns : columnas de `df_row_votes` que son partidos.
    n_seats : escaños que se reparten en la circunscripción.
    min_per : umbral mínimo de votos para entrar en el reparto (3 % en el
        Congreso). Se calcula sobre los votos a candidaturas, no sobre los votos
        válidos (que incluyen el voto en blanco), así que es una aproximación.

    Devuelve
    --------
    tabla : DataFrame con una fila ``votos`` y una fila ``escaño_i`` por cada
        escaño, con el cociente de cada partido en el momento de asignar ese
        escaño. La última fila sirve para ver lo cerca que se quedó cada partido
        del último escaño.
    escanios : DataFrame con la columna ``acumulado`` = escaños por partido.
    """
    votos = df_row_votes[party_columns].T
    votos = votos.rename(columns={votos.columns[0]: "votos"})
    total_votos = int(votos["votos"].sum())
    votos = votos[votos["votos"] > min_per * total_votos]
    tabla = votos.sort_values(by="votos", ascending=False)

    # divisor = escaños obtenidos hasta ahora + 1
    divisor = pd.Series(1, index=tabla.index)
    for idx in range(1, n_seats + 1):
        cocientes = (tabla["votos"] / divisor).astype(int)
        tabla[f"escaño_{idx}"] = cocientes
        divisor[cocientes.idxmax()] += 1

    escanios = (divisor - 1).to_frame("acumulado")
    return tabla.T, escanios
