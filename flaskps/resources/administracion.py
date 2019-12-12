from flask import request, session, abort, make_response, jsonify, render_template, flash

from flaskps.helpers.permission import has_permission
from flaskps.helpers.role import has_role
from flaskps.models.administracion import Administracion
from flaskps.models.ciclo_lectivo import CicloLectivo
from flaskps.models.dia import Dia
from flaskps.models.docente import Docente
from flaskps.models.estudiante import Estudiante
from flaskps.models import siteconfig
from flaskps.models.nucleo import Nucleo


def administracion():

    ciclos = CicloLectivo.all()

    docentes = Docente.all()

    estudiantes = Estudiante.all()

    nucleos = Nucleo.all()

    dias = Dia.all()

    for ciclo in ciclos:
        ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
        ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

    return render_template(
        "user/moduloadministrativo.html",
        ciclos=ciclos,
        docentes=docentes,
        estudiantes=estudiantes,
        nucleos=nucleos,
        dias=dias
        # username=user["username"],
    )


def docente_talleres():
    s_config = siteconfig.get_config()
    if not has_permission("horariodocente_index", session) or not has_permission("horariodocente_show", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    d_id = request.args.get("d_id")

    if d_id:
        talleres = Administracion.talleres_docente(d_id)

        if talleres is not None:
            data = jsonify(talleres)
            return make_response(data, 200)
        else:
            abort(422)
    else:
        abort(400)


def ciclos_taller_docente():
    s_config = siteconfig.get_config()
    if not has_permission("horariodocente_index", session) or not has_permission("horariodocente_show", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    d_id = request.args.get("d_id")
    t_id = request.args.get("t_id")

    if d_id and t_id:
        ciclos = Administracion.ciclos_taller_docente(d_id, t_id)

        for ciclo in ciclos:
            ciclo["fecha_ini"] = ciclo["fecha_ini"].strftime("%d-%m-%Y")
            ciclo["fecha_fin"] = ciclo["fecha_fin"].strftime("%d-%m-%Y")

        if ciclos is not None:
            data = jsonify(ciclos)
            return make_response(data, 200)
        else:
            abort(422)
    else:
        abort(400)


def dias_nucleo_ciclo_taller_docente():
    s_config = siteconfig.get_config()
    if not has_permission("horariodocente_index", session) or not has_permission("horariodocente_show", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):
        abort(401)

    d_id = request.args.get("d_id")
    t_id = request.args.get("t_id")
    c_id = request.args.get("c_id")
    n_id = request.args.get("n_id")

    if d_id and t_id and c_id and n_id:
        dias = Administracion.dias_nucleo_ciclo_taller_docente(d_id, t_id, c_id, n_id)

        if dias is not None:
            data = jsonify(dias)
            return make_response(data, 200)
        else:
            abort(422)
    else:
        abort(400)


def docente_set_horario():
    s_config = siteconfig.get_config()
    if not has_permission("horariodocente_new", session) or not has_permission("horariodocente_new", session) or not has_permission("horariodocente_update", session) or not has_permission("horariodocente_destroy", session) or (
            s_config["modo_mantenimiento"] == 1 and not has_role("administrador", session)
    ):

        abort(401)

    # Validación - (queda pendiente)

    op_response = dict()

    # suplantar True por form.validate_on_submit cuando haya validación
    if True:
        params = request.form.to_dict()
        d_id = params['docente_id']
        c_id = params['ciclo_id']
        t_id = params['taller_id']

        docente_responsable_taller_id = Administracion.docente_responsable_taller_id(d_id, c_id, t_id)

        if docente_responsable_taller_id:
            n_id = params['nucleo_id']
            dias_id = request.form.getlist('dias_id')
            horario_set = Administracion.docente_set_horario(docente_responsable_taller_id['id'], n_id, dias_id)

            if horario_set:
                msg = 'asignado' if dias_id else 'desasignado'
                op_response["msg"] = "Se ha " + msg + " el horario del docente con éxito"
                op_response["type"] = "success"
            else:
                op_response["msg"] = "Ha ocurrido un error al asignar el horario"
                op_response["type"] = "error"
                abort(make_response(jsonify(op_response), 422))

        else:
            abort(make_response(jsonify(op_response), 400))

    return make_response(jsonify(op_response), 200)
