$(document).ready(function () {
    const imgs = $('.wrap-slick3-dots li a');
    const imgBtns = [...imgs];
    let imgId = 1;
    const imgshow = $('.preview-pic div');
    imgshow[0].classList.add('active');
    imgBtns.forEach((imgItem) => {
        imgItem.addEventListener('click', (event) => {
            event.preventDefault();
            imgId = imgItem.dataset.target;
            $('.preview-pic div').attr('class', 'tab-pane')
            $(`#${imgId}`).attr('class', 'tab-pane active');
        });
    });
    $('.carousel-inner div')[0].classList.add('active');
    $('#itemslider').carousel({ interval: 10000 });

    $('.carousel-showmanymoveone .item').each(function(){
    var itemToClone = $(this);

        for (var i=1;i<4;i++) {
            itemToClone = itemToClone.next();
            if (!itemToClone.length) {
                itemToClone = $(this).siblings(':first');
            }
            itemToClone.children(':first-child').clone().addClass("cloneditem-"+(i)).appendTo($(this));
        }
    });
});
