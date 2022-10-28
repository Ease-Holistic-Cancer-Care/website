
if ($(window).scrollTop() > 80) {
    $('#back_to_top').fadeIn();
}
else {
    $('#back_to_top').fadeOut();
}
$(window).scroll(function (event) {
    var scroll = $(window).scrollTop();
    if (scroll > 80) {
        $('#navbar_logo_top').addClass('navbar_top_logo_resize');
        $('#navbar_logo_bottom').addClass('navbar_top_logo_resize');
        $("#top_navbar").addClass('navbar_top_resize')
        $('#back_to_top').fadeIn();
    } else {
        $('#navbar_logo_top').removeClass('navbar_top_logo_resize');
        $('#navbar_logo_bottom').removeClass('navbar_top_logo_resize');
        $("#top_navbar").removeClass('navbar_top_resize');
        $('#back_to_top').fadeOut();
    }
});

// $(".specialty_navbar_dropdown").click(function () {
//     //if window width is less than 992px
//     if ($(window).width() < 992) {
//         // keep the parent's parent element open
//         $(this).parent().parent().addClass("show");
//         $(this).parent().parent().siblings('.nav-link').addClass("show");
//         // add class "show" to the sibling element having class submenu
//         $(this).addClass("show");
//         $(this).siblings(".submenu").toggleClass("show");
//     }
// });
