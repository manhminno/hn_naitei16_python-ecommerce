$(document).ready(function () {
    let select_filter = $('#Idfilter select')[0];
    select_filter.on("change", function() {
        $('#Idfilter')[0].submit()
    });
});
