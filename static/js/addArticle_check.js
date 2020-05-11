var error_name;
var error_cate;
var error_time;

var $name=$('[name="name"]');
var $cate=$('[name="cate_sel"]');
var $time=$('[name="time"]');

function check_name() {
    if ($name.val().length===0){
        $name.next().text('文章名称不能为空');
        error_name=false;
    }else {
        $name.next().text('');
        error_name=true;
    }
}
function check_cate() {
    var span=$cate.siblings('span');
    if ($('[name="cate_sel"] option:selected').val()==='default-cate'){
        span.text('请选择所属类别');
        error_cate=false;
    }else {
        span.text('');
        error_cate=true;
    }
}
function check_time() {
    if ($time.val().length===0){
        $time.next().text('发布时间不能为空或不完整');
        error_time=false;
    }else {
        $time.next().text('');
        error_time=true;
    }
}

$name.blur(function () {
    check_name();
});
$cate.change(function () {
    check_cate();
});
$time.blur(function () {
    check_time();
});

function check_all() {
    check_name();
    check_cate();
    check_time();
    return (error_name&&error_cate&&error_time)
}
