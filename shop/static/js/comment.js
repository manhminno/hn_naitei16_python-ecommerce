$(document).ready(function () {
    $("#comment_form").submit(function (e) {
        e.preventDefault();
        var formData = $(this).serializeArray();
        var product_id = $('div#product-detail').attr('product-id');
        $.ajax({
            type: 'POST',
            url: `/add_comment/${product_id}`,
            data: formData,
            success: function(res) {
                var urlt = `/delete_comment/${res.id}`;
                var rate = ""
                let result = [1,2,3,4,5].map(value=>{
                    let status = ( res.rate < value ) ?  'fa fa-star-o empty' :  'fa fa-star'
                    rate += `<i class="${status}"> </i>`
                })
                var _html=
                `<div class="single-review">
                    <div class="review-heading">
                        <div><strong>${res.user}</strong> <i class="fa fa-clock-o"></i> ${res.create_at}</div>
                        <div class="review-rating pull-right">
                        ${rate}
                        </div>
                    </div>
                    <div class="review-body">
                        ${res.content}
                        <div class="review-rating pull-right">
                            <a href=${urlt}><i class="fa fa-trash-o" aria-hidden="true"></i></a>
                        </div>
                    </div>
                </div>
                <hr>`;
                if (res.id)
                    $(".comment-wrapper").prepend(_html);
                $('input[type=text], textarea').val('');
                $('input[type=radio]').prop("checked", false);
                let comment_span = $('#comment_span')
                comment_span[0].innerHTML = parseInt(comment_span[0].innerHTML) + 1
            }
        })
    })
})
