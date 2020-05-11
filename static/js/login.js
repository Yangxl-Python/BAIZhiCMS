$(function () {
    var check_username=false;
    var check_pwd=false;

    var $username=$(':text');
    var $pwd=$(':password');
    var $submit=$(':submit');

    check_all();

    function ck_un() {
        var len=$username.val().length;
        var re=/^[\u4e00-\u9fa5]{2,10}$/;
        if (re.test($username.val())){
            $username.next().hide();
            check_username=true;
        }else {

            if (len===0){
                $('.user_error').text('用户名不能为空');
            }else {
                $('.user_error').text('用户名必须为2到10位中文名称');
            }
            check_username=false;
            $username.next().show();
        }
    }
    function ck_pwd() {
        var len=$pwd.val().length;
        var re=/^\w{6,18}$/;
        if (re.test($pwd.val())){
            check_pwd=true;
            $pwd.next().hide();
        }else {
            if (len===0){
                $('.pwd_error').text('密码不能为空');
            }else {
                $('.pwd_error').text('密码必须为6到18位字母、数字或下划线');
            }
            check_pwd=false;
            $pwd.next().show();
        }
    }
    function check_all() {
        $(":submit").attr("disabled",!(check_username&&check_pwd));
    }

    $username.blur(function () {
        ck_un();
        check_all();
    });
    $pwd.blur(function () {
        ck_pwd();
        check_all();
    });
});