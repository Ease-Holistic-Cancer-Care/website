//close fixed_carousel by default
$('#fixed_carousel').hide();

//open fixed_carousel on click of image_1

function openCarousel(id) {
    $('.active').removeClass('active');
    $('#carousel_' + String(id)).addClass('active');
    $('#fixed_carousel').fadeIn();
}

//close fixed_carousel on click of close button
$('#cross_icon').click(function () {
    $('#fixed_carousel').fadeOut();
});
