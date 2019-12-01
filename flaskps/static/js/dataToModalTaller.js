dataToModalTaller = function(response) {
    $('#editar_id').val(response['id']);
    $('#nombre').attr("placeholder", response['nombre']);
    $('#nombre').val(response['nombre']);
    $('#nombre_corto').attr("placeholder", response['apellido']);
    $('#nombre_corto').val(response['nombre_corto']);
    M.updateTextFields();
}