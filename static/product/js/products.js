$(document).ready(function () {
    var select = $('select');
    // Add cookie if it is not defined.
    if ($.cookie('sort') == undefined) {
        $.cookie('sort', select.val(), {path: '/'});
    }
    // If cookie is defined, set value in select.
    else {
        select.val($.cookie('sort'));
    }
    // Change cookie and reload page if user change sort mode.
    select.change(function () {
        $.cookie('sort', $(this).val(), {path: '/'});
        location.reload()
    })
});
