dataToModalEstudiante = function(response) {
    $('#modal_editar_id').val(response['id']);
    $('#modal_editar_apellido').attr("placeholder", response['apellido']);
    $('#modal_editar_apellido').val(response['apellido']);
    $('#modal_editar_nombre').attr("placeholder", response['nombre']);
    $('#modal_editar_nombre').val(response['nombre']);
    $('#modal_fecha_nacimiento').attr("placeholder", response['fecha_nac']);
    $('#modal_fecha_nacimiento').val(response['fecha_nac']);
    $("#modal_select_genero").val(response['genero_id']);
    $("#modal_select_localidad").val(response['localidad_id']);
    $('#modal_domicilio').attr("placeholder", response['domicilio']);
    $('#modal_domicilio').val(response['domicilio']);
    $("#modal_select_barrio").val(response['barrio_id']);
    $("#modal_select_tipo").val(response['tipo_doc_id']);
    $('#modal_documento_numero').attr("placeholder", response['numero']);
    $('#modal_documento_numero').val(response['numero']);
    $('#modal_telefono_numero').attr("placeholder", response['tel']);
    $('#modal_telefono_numero').val(response['tel']);
    $("#modal_select_escuela").val(response['escuela_id']);
    $("#modal_select_nivel").val(response['nivel_id']);
    $("#modal_select_responsable_tipo").val(response['responsable_tipo_id']);
    M.updateTextFields();
}