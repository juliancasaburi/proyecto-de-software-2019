from flaskps.db import get_db
from flaskps.helpers.localidades import localidades
from flaskps.helpers.tipos_documento import tipos_documento
from flaskps.models.barrio import Barrio
from flaskps.models.escuela import Escuela
from flaskps.models.genero import Genero
from flaskps.models.nivel import Nivel
from flaskps.models.responsable_tipo import Responsable_tipo


def pasarChoices(form):
    db = get_db()
    locs = localidades()
    Barrio.db = db
    barrios = Barrio.all()
    Genero.db = db
    generos = Genero.all()
    tipos_doc = tipos_documento()
    Escuela.db = db
    escuelas = Escuela.all()
    Nivel.db = db
    niveles = Nivel.all()
    Responsable_tipo.db = db
    responsables_tipos = Responsable_tipo.all()

    # choices de los selects
    form.select_localidad.choices = [
        (localidad["id"], localidad["nombre"]) for localidad in locs
    ]
    form.select_barrio.choices = [
        (barrio["id"], barrio["nombre"]) for barrio in barrios
    ]
    form.select_genero.choices = [
        (genero["id"], genero["nombre"]) for genero in generos
    ]
    form.select_tipo.choices = [(tipo["id"], tipo["nombre"]) for tipo in tipos_doc]
    form.select_escuela.choices = [
        (escuela["id"], escuela["nombre"]) for escuela in escuelas
    ]
    form.select_nivel.choices = [(nivel["id"], nivel["nombre"]) for nivel in niveles]
    form.select_responsable_tipo.choices = [(responsable_tipo["id"], responsable_tipo["nombre"]) for responsable_tipo in responsables_tipos]

    return form
