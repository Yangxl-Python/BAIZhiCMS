$(function(){

	var $username = $('#user_name');
	var $pwd = $('#pwd');
	var $cpwd = $('#cpwd');
	var $email = $('#email');
	var $allow = $('#allow');

	var error_name = $username.get(0) !== undefined;
	var error_password = $pwd.get(0) !== undefined;
	var error_check_password = $cpwd.get(0) !== undefined;
	var error_email = $email.get(0) !== undefined;
	var error_check = $allow.get(0) !== undefined;

	check_all();

	if (error_check){
		check_allow();
	}

	$username.change(function() {
		check_user_name();
		check_all();
	});

	$pwd.blur(function() {
		check_pwd();
		check_all();
	});

	$cpwd.blur(function() {
		check_cpwd();
		check_all();
	});

	$email.blur(function() {
		check_email();
		check_all();
	});

	$allow.click(function() {
		check_allow();
		check_all();
	});

	function check_allow() {
		if($allow.is(':checked'))
		{
			error_check = false;
			$allow.siblings('span').hide();
		}
		else
		{
			error_check = true;
			$allow.siblings('span').html('请勾选同意');
			$allow.siblings('span').show();
		}
	}

	function check_user_name(){
		var re=/^[\u4e00-\u9fa5]{2,10}$/;
		var len = $username.val().length;
		if(!re.test($username.val()))
		{
			if(len===0){
				$username.next().html('用户名不能为空');
			}else {
				$username.next().html('请输入2-10位的中文名称');
			}
			$username.next().show();
			error_name = true;
		}
		else
		{
			$username.next().hide();
			$username.next().html('ok');
			error_name = false;
		}
	}

	function check_pwd(){
		var re=/^\w{6,18}$/;
		var len = $pwd.val().length;
		if(!re.test($pwd.val()))
		{
			if (len===0){
				$pwd.next().html('密码不能为空');
			}else {
				$pwd.next().html('密码必须为6到18位字母、数字或下划线');
			}
			$pwd.next().show();
			error_password = true;
		}
		else
		{
			$pwd.next().hide();
			error_password = false;
		}		
	}


	function check_cpwd(){
		var pass = $pwd.val();
		var cpass = $cpwd.val();

		if(pass!==cpass)
		{
			$cpwd.next().html('两次输入的密码不一致');
			$cpwd.next().show();
			error_check_password = true;
		}
		else
		{
			$cpwd.next().hide();
			error_check_password = false;
		}		
		
	}

	function check_email(){
		var re = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
		var len = $email.val().length;
		if(re.test($email.val()))
		{
			$email.next().hide();
			error_email = false;
		}
		else
		{
			if (len===0){
				$email.next().html('邮箱不能为空');
			}else {
				$email.next().html('你输入的邮箱格式不正确');
			}
			$email.next().show();
			error_check_password = true;
		}
	}

	function check_all(){
		$(":submit").attr("disabled",(error_name || error_password || error_check_password || error_email || error_check));
	}

});