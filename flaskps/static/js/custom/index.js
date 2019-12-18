$(document).ready(function() {
    $('select').formSelect();
    new WOW({
        live: true
    }).init();
    $('.parallax').parallax();
    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
    });
});