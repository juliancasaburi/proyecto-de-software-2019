import requests


def localidades():
    loc = requests.get(
        "https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad"
    )
    loc = loc.json()

    return loc
