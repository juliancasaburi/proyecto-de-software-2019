import requests


def localidades():
    locs = requests.get(
        "https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad"
    )
    locs = locs.json()

    return locs


def localidad(id_localidad):
    loc = requests.get(
        "https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad/%d" % id_localidad
    )
    loc = loc.json()

    return loc
