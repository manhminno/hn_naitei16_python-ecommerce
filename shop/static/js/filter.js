$(document).ready(function () {
    let select_filter = $('#Idfilter select');
    select_filter.on("change", function() {
        $('#Idfilter')[0].submit()
    });
});
