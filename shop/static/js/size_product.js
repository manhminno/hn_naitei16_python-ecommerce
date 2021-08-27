$(document).ready(function () {
    const size = $('#size');
    size.on("change", function() {
        let data = size[0].value
        let options = $('#size option')
        options = [...options]
        options.forEach(option => {
            if (option.value === data){
                let span = $("#quantity_left span")
                span[0].innerHTML = option.getAttribute('size-amount')
                let number_size = $("#number_size")
                number_size[0].max = option.getAttribute('size-amount')
            }
        });
    });
    $('.btn-num-product-up').on('click', function(){
        $("#number_size")[0].value = parseInt($("#number_size")[0].value) + 1
    })
    $('.btn-num-product-down').on('click', function(){
        $("#number_size")[0].value = parseInt($("#number_size")[0].value) - 1
    })
});
