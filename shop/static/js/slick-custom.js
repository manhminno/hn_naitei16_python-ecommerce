

(function ($) {
    var itemSlick1 = $('.slick1').find('.item-slick1');
    var action1 = [];
    var action2 = [];
    var action3 = [];
    var cap1Slide1 = [];
    var cap2Slide1 = [];
    var btnSlide1 = [];
    for (var i = 0; i < itemSlick1.length; i++) {
        cap1Slide1[i] = $(itemSlick1[i]).find('.caption1-slide1');
        cap2Slide1[i] = $(itemSlick1[i]).find('.caption2-slide1');
        btnSlide1[i] = $(itemSlick1[i]).find('.wrap-btn-slide1');
    }
    $('.slick1').on('init', function () {
        action1[0] = setTimeout(function () {
            $(cap1Slide1[0]).addClass($(cap1Slide1[0]).data('appear') + ' visible-true');
        }, 200);
        action2[0] = setTimeout(function () {
            $(cap2Slide1[0]).addClass($(cap2Slide1[0]).data('appear') + ' visible-true');
        }, 1000);
        action3[0] = setTimeout(function () {
            $(btnSlide1[0]).addClass($(btnSlide1)[0].data('appear') + ' visible-true');
        }, 1800);
    });
    $('.slick1').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        fade: true,
        dots: false,
        appendDots: $('.wrap-slick1-dots'),
        dotsClass: 'slick1-dots',
        infinite: true,
        autoplay: true,
        autoplaySpeed: 6000,
        arrows: true,
        appendArrows: $('.wrap-slick1'),
        prevArrow: '<button class="arrow-slick1 prev-slick1"><i class="fa  fa-angle-left" aria-hidden="true"></i></button>',
        nextArrow: '<button class="arrow-slick1 next-slick1"><i class="fa  fa-angle-right" aria-hidden="true"></i></button>',
    });
    $('.slick1').on('afterChange', function (event, slick, currentSlide) {
        for (var i = 0; i < itemSlick1.length; i++) {
            clearTimeout(action1[i]);
            clearTimeout(action2[i]);
            clearTimeout(action3[i]);
            $(cap1Slide1[i]).removeClass($(cap1Slide1[i]).data('appear') + ' visible-true');
            $(cap2Slide1[i]).removeClass($(cap2Slide1[i]).data('appear') + ' visible-true');
            $(btnSlide1[i]).removeClass($(btnSlide1[i]).data('appear') + ' visible-true');
        }
        action1[currentSlide] = setTimeout(function () {
            $(cap1Slide1[currentSlide]).addClass($(cap1Slide1[currentSlide]).data('appear') + ' visible-true');
        }, 200);

        action2[currentSlide] = setTimeout(function () {
            $(cap2Slide1[currentSlide]).addClass($(cap2Slide1[currentSlide]).data('appear') + ' visible-true');
        }, 1000);
        action3[currentSlide] = setTimeout(function () {
            $(btnSlide1[currentSlide]).addClass($(btnSlide1)[currentSlide].data('appear') + ' visible-true');
        }, 1800);
    });
    $('.wrap-hot').slick({
        slidesToShow: 4,
        dots: false,
        centerMode: true,
        prevArrow: '<button class="slick-prev slick-arrow"><i class="fa  fa-angle-left" aria-hidden="true"></i></button>',
        nextArrow: '<button class="slick-next slick-arrow"><i class="fa  fa-angle-right" aria-hidden="true"></i></button>',
    });
})(jQuery);
