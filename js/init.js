(function($){
  $(function(){

    $('.preloader-background').delay(500).fadeOut('slow');

    $('.sidenav').sidenav();
    $('.parallax').parallax();
    $('.fixed-action-btn').floatingActionButton();

  }); // end of document ready
})(jQuery); // end of jQuery name space
