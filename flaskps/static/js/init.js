(function($){
  $(function(){

    $('.preloader-background').delay(500).fadeOut('slow');

    $('.sidenav').sidenav();
    $(".dropdown-trigger").dropdown();

    $('#modalConfiguracion').modal();

    $("#switchMantenimientoNav").on("change", function(){
      $.ajax({
        type: "POST",
        url : '/mantenimiento',
        success: function (response) {
          var checked;
          if(response['modo_mantenimiento'] == 1)
          {
            M.toast({html: 'El sitio ahora se encuentra en mantenimiento', classes: 'orange darken-4'});
            checked = true;
          }
          else
          {
            M.toast({html: 'El sitio ya no se encuentra en mantenimiento', classes: 'grey darken-2'});
            checked = false;
          }
          if ( $("#switchMantenimiento").length ) {
            $("#switchMantenimiento").prop("checked",checked);
          }
        },
      });
    });

  }); // end of document ready
})(jQuery); // end of jQuery name space
