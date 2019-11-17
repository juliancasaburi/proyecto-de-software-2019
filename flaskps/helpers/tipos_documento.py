import requests


def tipos_documento():
    tipos_doc = requests.get(
        "https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento"
    )
    tipos_doc = tipos_doc.json()

    return tipos_doc


def tipo_documento(id_tipo):
    tipo_doc = requests.get(
        "https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento/%d"
        % id_tipo
    )
    tipo_do = tipo_doc.json()

    return tipo_do
