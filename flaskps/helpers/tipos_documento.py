import requests


def tipos_documento():
    tipo_doc = requests.get(
        "https://api-referencias.proyecto2019.linti.unlp.edu.ar/tipo-documento"
    )
    tipo_doc = tipo_doc.json()

    return tipo_doc
