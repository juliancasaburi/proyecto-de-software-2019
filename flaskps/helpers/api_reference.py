import requests


def get_localidades():
    loc = requests.get('https://api-referencias.proyecto2019.linti.unlp.edu.ar/localidad')
    return loc.json()


def get_tipos_doc():
    tipo_doc = requests.get('https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento')
    return tipo_doc.json()