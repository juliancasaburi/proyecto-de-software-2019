$(document).ready(function() {
// reiniciar input
    $('a.eraseFilter').on('click', function (e) {
        var input = $(this).parent().parent().find("input");
        input.val('');
        input.change();
    });

// reiniciar inputs
    $('a.resetFilters').on('click', function (e) {
        inputs = $('#modalFilters').find('input:text');
        inputs.val('');
        inputs.change();
    });
});