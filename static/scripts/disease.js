$('#button1').click(function () {
    if ($('#button1').hasClass('inactive_button')) {
        $('#button1').removeClass('inactive_button');
        $('#button1').addClass('active_button');
        $('#button2').removeClass('active_button');
        $('#button2').addClass('inactive_button');
        $('#content_1').show();
        $('#content_2').hide();
    }
});
$('#button2').click(function () {
    if ($('#button2').hasClass('inactive_button')) {
        $('#button2').removeClass('inactive_button');
        $('#button2').addClass('active_button');
        $('#button1').removeClass('active_button');
        $('#button1').addClass('inactive_button');
        $('#content_2').show();
        $('#content_1').hide();
    }
});
$('#button3').click(function () {
    if ($('#button3').hasClass('inactive_button')) {
        $('#button3').removeClass('inactive_button');
        $('#button3').addClass('active_button');
        $('#button4').removeClass('active_button');
        $('#button4').addClass('inactive_button');
        $('#severity_3').show();
        $('#severity_4').hide();
    }
});
$('#button4').click(function () {
    if ($('#button4').hasClass('inactive_button')) {
        $('#button4').removeClass('inactive_button');
        $('#button4').addClass('active_button');
        $('#button3').removeClass('active_button');
        $('#button3').addClass('inactive_button');
        $('#severity_4').show();
        $('#severity_3').hide();
    }
});
$('#button5').click(function () {
    if ($('#button5').hasClass('inactive_button')) {
        $('#button5').removeClass('inactive_button');
        $('#button5').addClass('active_button');
        $('#button6').removeClass('active_button');
        $('#button6').addClass('inactive_button');
        $('#treatment_5').show();
        $('#treatment_6').hide();
    }
});
$('#button6').click(function () {
    if ($('#button6').hasClass('inactive_button')) {
        $('#button6').removeClass('inactive_button');
        $('#button6').addClass('active_button');
        $('#button5').removeClass('active_button');
        $('#button5').addClass('inactive_button');
        $('#treatment_6').show();
        $('#treatment_5').hide();
    }
});

$(".doctor_carousel").slick({
    prevArrow:
        "<img class='a-left control-c prev slick-prev' src='../../static/images/elements/carousel_arrow_left.png'>",
    nextArrow:
        "<img class='a-right control-c next slick-next' src='../../static/images/elements/carousel_arrow_right.png'>",

    dots: true,
    infinite: true,
    speed: 800,
    slidesToShow: 3,
    slidesToScroll: 3,
    arrows: true,
    responsive: [
        {
            breakpoint: 992,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2,
                infinite: true,
                dots: true,
            },
        },
        {
            breakpoint: 768,
            settings: {
                slidesToShow: 2,
                slidesToScroll: 2,
            },
        },
        {
            breakpoint: 767.5,
            settings: {
                slidesToShow: 1,
                slidesToScroll: 1,
            },
        },
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
    ],
});

let faq = document.getElementsByClassName('faq_page');
for (let i = 0; i < faq.length; i++) {
    faq[i].addEventListener("click", function () {
        this.classList.toggle("active_faq");
        var body = this.nextElementSibling;
        if (body.style.display === "block") {
            body.style.display = "none";
        } else {
            body.style.display = "block";
        }
    });
}
