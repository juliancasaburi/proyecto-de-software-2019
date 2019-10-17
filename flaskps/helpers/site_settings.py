import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('flaskps/config') / '.env'
load_dotenv(verbose=True, dotenv_path=env_path)


def email():
    return os.getenv("EMAIL_CONTACTO")


def titulo():
    return os.getenv("TITULO")


def descripcion():
    return os.getenv("DESCRIPCION")


def maintenance_mode():
    return os.getenv("MODO_MANTENIMIENTO")


def items_per_page():
    return os.getenv("ITEMS_POR_PAGINA")
