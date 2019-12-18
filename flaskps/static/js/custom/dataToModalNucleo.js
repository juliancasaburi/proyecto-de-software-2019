dataToModalNucleo = function(response) {
    $('#modal_editar_id').val(response['id']);
    $('#modal_editar_nombre').attr("placeholder", response['nombre']);
    $('#modal_editar_nombre').val(response['nombre']);
    $('#modal_editar_direccion').attr("placeholder", response['direccion']);
    $('#modal_editar_direccion').val(response['direccion']);
    $('#modal_editar_telefono').attr("placeholder", response['telefono']);
    $('#modal_editar_telefono').val(response['telefono']);
    $('#modal_editar_lat').attr("placeholder", response['lat']);
    $('#modal_editar_lat').val(response['lat']);
    $('#modal_editar_lng').attr("placeholder", response['lng']);
    $('#modal_editar_lng').val(response['lng']);
    $('select').formSelect();
    M.updateTextFields();
};