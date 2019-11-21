dataToModalUsuario = function(response) {
    for (var key in response['roles']){
        $("#select_roles option[value='" + response['roles'][key]['id'] + "']").prop("selected", true);
    }
    $('#modal_editar_id').val(response['id']);
    $('#modal_editar_activo').prop('checked', response['activo']);
    $('#modal_editar_nombre').attr("placeholder", response['first_name']);
    $('#modal_editar_nombre').attr("value", response['first_name']);
    $('#modal_editar_apellido').attr("placeholder", response['last_name']);
    $('#modal_editar_apellido').attr("value", response['last_name']);
    $('#modal_editar_email').attr("placeholder", response['email']);
    $('#modal_editar_email').attr("value", response['email']);
    $('#modal_editar_username').attr("placeholder", response['username']);
    $('#modal_editar_username').attr("value", response['username']);
    M.updateTextFields();
    $('#select_roles').formSelect();
};