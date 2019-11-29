dataToModalInstrumento = function(response) {
    $('#modal_editar_id').val(response['id']);
    $('#modal_editar_nombre').attr("placeholder", response['nombre']);
    $('#modal_editar_nombre').val(response['nombre']);
    $("#modal_editar_tipo_id").val(response['tipo_id']);
    $('#modal_editar_num_inventario').attr("placeholder", response['num_inventario']);
    $('#modal_editar_num_inventario').val(response['num_inventario']);
    $('select').formSelect();
    M.updateTextFields();
};