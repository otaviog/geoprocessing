#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from statistics import mean

import geopandas
import matplotlib.pyplot as plt
import numpy as np
from fire import Fire


def add_ruler(latlons, geod, bottom_lon, ax):
    min_lat = latlons[:, 0].min()
    max_lat = latlons[:, 0].max()
    mean_lon = latlons[:, 1].mean()

    scale_km = int(geod.line_length(
        [min_lat, max_lat], [mean_lon, mean_lon]) / 1000)

    ax.plot([min_lat, max_lat], [bottom_lon, bottom_lon], color='k')
    ax.text(mean([min_lat, max_lat]), bottom_lon, f"{scale_km} Km",
            horizontalalignment='center', verticalalignment='bottom')


def cps_mesoregion():
    shape = geopandas.read_file("MEEBRASIL.shp")

    cps = 94

    geometry = shape.loc[94]['geometry']

    latlons = np.array(geometry.exterior.coords)
    geo_cps = geopandas.GeoDataFrame(geometry=[geometry], crs=shape.crs)

    fig, ax = plt.subplots(1, 1)
    ax.axis('off')
    geo_cps.boundary.plot(ax=ax)

    min_lat = latlons[:, 0].min()
    max_lat = latlons[:, 0].max()
    mean_lon = latlons[:, 1].mean()

    scale_km = round(geo_cps.crs.get_geod().line_length(
        [min_lat, max_lat], [mean_lon, mean_lon]) / 1000, 2)

    bottom_lon = -23.5
    plt.plot([min_lat, max_lat], [bottom_lon, bottom_lon], color='k')
    ax.text(mean([min_lat, max_lat]), bottom_lon, f"{scale_km} km",
            horizontalalignment='center', verticalalignment='bottom')

    plt.show()


Pirassununga = {
    "Aguaí": 3500303,
    "Pirassununga": 3539301,
    "Porto Ferreira": 3540705,
    "Santa Cruz das Palmeiras": 3546306
}

Sao_Joao_da_Boa_Vista = {
    "Águas da Prata": 3500402,
    "Caconde": 3508702,
    "Casa Branca": 3510807,
    "Divinolândia": 3513900,
    "Espírito Santo do Pinhal": 3515186,
    "Itobi": 3523800,
    "Mococa": 3530508,
    "Santo Antônio do Jardim": 3548104,
    "São João da Boa Vista": 3549102,
    "São José do Rio Pardo": 3549706,
    "São Sebastião da Grama": 3550803,
    "Tambaú": 3553302,
    "Tapiratiba": 3553609,
    "Vargem Grande do Sul": 3556404
}

Mogi_Mirim = {
    "Artur Nogueira": 3503802,
    "Engenheiro Coelho": 3515152,
    "Estiva Gerbi": 3557303,
    "Itapira": 3522604,
    "Mogi Guaçu": 3530706,
    "Mogi Mirim": 3530805,
    "Santo Antônio de Posse": 3548005
}

Campinas = {
    "Americana": 3501608,
    "Campinas": 3509502,
    "Cosmópolis": 3512803,
    "Elias Fausto": 3514908,
    "Holambra": 3519055,
    "Hortolândia": 3519071,
    "Indaiatuba": 3520509,
    "Jaguariúna": 3524709,
    "Monte Mor": 3531803,
    "Nova Odessa": 3533403,
    "Paulínia": 3536505,
    "Pedreira": 3537107,
    "Santa Bárbara d'Oeste": 3545803,
    "Sumaré": 3552403,
    "Valinhos": 3556206,
    "Vinhedo": 3556701
}

Amparo = {
    "Águas de Lindóia": 3500501,
    "Amparo": 3501905,
    "Lindoia": 3527009,
    "Monte Alegre do Sul": 3531209,
    "Pedra Bela": 3536802,
    "Pinhalzinho": 3538204,
    "Serra Negra": 3551603,
    "Socorro": 3552106
}


def cps_microregions():
    munsp = geopandas.read_file("35MUE250GC_SIR.shp")

    cps_mesoregion = {**Pirassununga, **Sao_Joao_da_Boa_Vista,
                      **Mogi_Mirim, **Campinas, **Amparo}
    mun_geoms = {}

    for name, cod in cps_mesoregion.items():
        loc = munsp.loc[munsp["CD_GEOCODM"] == str(cod)]
        mun_geoms[name] = loc["geometry"].item()

    df = geopandas.GeoDataFrame(
        crs=munsp.crs, geometry=list(mun_geoms.values()))

    fig, ax = plt.subplots(1, 1)
    ax.axis('off')
    df.boundary.plot(ax=ax)
    plt.show()


def cps_microregions2(output=None):
    munsp = geopandas.read_file("35MUE250GC_SIR.shp")

    cps_mesoregion = {
        'Pirassununga': Pirassununga,
        'São João da Boa Vista': Sao_Joao_da_Boa_Vista,
        "Mogi Mirim": Mogi_Mirim,
        "Campinas": Campinas,
        "Amparo": Amparo
    }

    latlons = []
    region_dfs = {}
    for micro_name, microregion in cps_mesoregion.items():
        mun_geoms = {}
        for name, cod in microregion.items():
            loc = munsp.loc[munsp["CD_GEOCODM"] == str(cod)]
            geometry = loc["geometry"].item()
            latlons.append(np.array(geometry.exterior.coords))
            mun_geoms[name] = geometry

        region_dfs[micro_name] = geopandas.GeoDataFrame(
            crs=munsp.crs, geometry=list(mun_geoms.values()))

    latlons = np.vstack(latlons)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(8.5, 6.5, forward=True)
    ax.axis('off')
    cmap = plt.get_cmap("tab20")
    for i, (name, df) in enumerate(region_dfs.items()):
        df.boundary.plot(ax=ax, color=cmap(i), label=name)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    add_ruler(latlons, munsp.crs.get_geod(), -23.35, ax)
    plt.title("Mesorregião de Campinas no Estado de São Paulo")
    if output is None:
        plt.show()
    else:
        fig.savefig(output)


if __name__ == '__main__':
    Fire({'cps_mesoregion': cps_mesoregion,
          'cps_microregions': cps_microregions,
          'cps_microregions2': cps_microregions2})
