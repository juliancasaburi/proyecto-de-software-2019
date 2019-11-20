dataToModalDocente = function(response) {
    $('#editar_id').val(response['id']);
    $('#editar_activo').prop('checked', response['activo']);
    $('#editar_nombre').attr("placeholder", response['nombre']);
    $('#editar_nombre').val(response['nombre']);
    $('#editar_apellido').attr("placeholder", response['apellido']);
    $('#editar_apellido').val(response['apellido']);

    $('#editar_fecha_nacimiento').attr("placeholder", response['fecha_nac']);
    $('#editar_fecha_nacimiento').val(response['fecha_nac']);

    $('#editar_domicilio').attr("placeholder", response['domicilio']);
    $('#editar_domicilio').val(response['domicilio']);

    $('#editar_documento_numero').attr("placeholder", response['numero']);
    $('#editar_documento_numero').val(response['numero']);

    if ((response['tel'] != "") && (response['tel'] != null)){
        $('#editar_telefono_numero').attr("placeholder", response['tel']);
        $('#editar_telefono_numero').val(response['tel']);
    }
    else{
        $('#editar_telefono_numero').attr("placeholder", null);
        $('#editar_telefono_numero').val(null);
    }

    $("#editar_select_genero").val(response['genero_id']);
    $("#editar_select_localidad").val(response['localidad_id']);
    $("#editar_select_tipo").val(response['tipo_doc_id']);

    $('select').formSelect();
    M.updateTextFields();
}