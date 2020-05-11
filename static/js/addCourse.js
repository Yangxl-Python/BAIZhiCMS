$(function () {
    var $tr=$('.option_tr');
    $(':radio:last').click(function () {
        $tr.show();
    });
    $(':radio:first').click(function () {
        $tr.hide();
    });
});
