# Datos de entrada

Los notebooks leen sus datos de esta carpeta, pero los ficheros no se versionan: son grandes y cada fuente tiene sus propias condiciones de uso. Descárgalos de las fuentes indicadas y colócalos con esta estructura (o apunta `POLITICAI_DATA_DIR` a otra carpeta que la siga):

```
data/
├── raw/
│   ├── resultados_electorales/
│   │   ├── congreso_por_municipio/   02_AAAAMM_1.xlsx, uno por elección       (notebooks 01, 02)
│   │   └── congreso_por_provincia/   PROV_02_201911_1.xlsx                    (notebook 02)
│   ├── escaños/escaños_2019.xlsx     codigo_de_provincia, nombre_de_provincia, escaños  (notebook 02)
│   └── mapas/
│       ├── madrid_municipios.geojson    propiedad CODIGOINE                   (notebook 01)
│       ├── zaragoza_municipios.geojson  propiedad CODIGOINE                   (notebook 02)
│       ├── mapa_provincias.json         propiedad Codigo (código INE, 2 dígitos)  (notebook 02)
│       └── countries.geojson            id = código ISO3 del país             (notebooks 04, 05)
└── staging/
    ├── elecciones_generales_completas.csv   la genera el notebook 01          (notebook 02)
    ├── programas_electorales/201910/        <partido>.txt                     (notebook 03)
    └── mundial/                                                               (notebooks 04, 05)
        ├── fragilidad.xls
        ├── freedom_house.xlsx
        ├── gini_mundial.xls
        ├── esperanza_vida.xls
        ├── poblacion.xls
        ├── años_escolarizacion_medios.csv
        ├── sistemas_electorales.xls
        ├── constituciones.xlsx              (o constituciones_reducido.csv, que genera el notebook 04)
        └── cow_country_codes.csv
```

## Fuentes

| Fichero | Fuente |
|---|---|
| Resultados al Congreso por municipio y por provincia | Ministerio del Interior, [infoelectoral.interior.gob.es](https://infoelectoral.interior.gob.es/) (área de descargas) |
| Escaños por provincia | Real Decreto de convocatoria de las elecciones de noviembre de 2019 (BOE) |
| Contornos de municipios y provincias | Instituto Geográfico Nacional, [Centro de Descargas del CNIG](https://centrodedescargas.cnig.es/) (límites municipales), recortados por provincia y convertidos a GeoJSON |
| Contornos de países | GeoJSON de países con el código ISO3 como `id` (por ejemplo, el de [datasets/geo-countries](https://github.com/datasets/geo-countries)) |
| Programas electorales | PDF publicados por cada partido para las elecciones de noviembre de 2019, convertidos a texto plano |
| Problemas de los españoles | CIS, barómetro de noviembre de 2019 (ya incluido en [`resultados/cis_nov_19.csv`](../resultados/cis_nov_19.csv)) |
| `fragilidad.xls` | Center for Systemic Peace, *State Fragility Index* |
| `freedom_house.xlsx` | Freedom House, *Freedom in the World* (puntuaciones por país y edición) |
| `gini_mundial.xls`, `esperanza_vida.xls`, `poblacion.xls` | Banco Mundial, indicadores SI.POV.GINI, SP.DYN.LE00.IN y SP.POP.TOTL |
| `años_escolarizacion_medios.csv` | Our World in Data, años medios de escolarización de la población adulta |
| `sistemas_electorales.xls` | International IDEA, *Electoral System Design Database* |
| `constituciones.xlsx` | Comparative Constitutions Project |
| `cow_country_codes.csv` | Correlates of War Project, *State System Membership* (códigos de país) |
