var error_text;
var error_check;
var error_select;

var $text=$('[name="name"]');
var $radio=$(':radio');
var $select=$('[name="cate_sel"]');

function check_text() {
    if($text.val().length===0){
        $text.next().text('名称不能为空');
        error_text=false;
    }else {
        $text.next().text('');
        error_text=true;
    }
}
function check_radio() {
    if ($(':radio:checked').get(0)===undefined){
        $radio.siblings('span').text('请选择类型');
        error_check=false;
    }else {
        $radio.siblings('span').text('');
        error_check=true;
    }
}
function check_select() {
    if ($(':radio:last').prop('checked')){
        var $span=$select.siblings('span');
        // 获取被选择的元素
        if ($('[name="cate_sel"]  option:selected').val()==='default-cate'){
            $span.text('请选择课程名称');
            error_select=false;
        }else {
            $span.text('');
            error_select=true;
        }
    }else {
        error_select=true;
    }
}

$text.blur(function () {
    check_text();
});
$radio.click(function () {
    check_radio();
});
$select.change(function () {
    check_select();
});

function check_all() {
    check_text();
    check_radio();
    check_select();
    return (error_text&&error_check&&error_select);
}