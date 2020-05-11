import random
import string
import traceback
import uuid
import hashlib
import re

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from BaiZhiCMS import settings
from reception.captcha.image import ImageCaptcha
from reception.models import UsersTable


def encryption(pwd, salt):
    hl = hashlib.sha256()  # 创建加密对象
    hl.update((pwd + salt).encode())  # 进行加密
    return hl.hexdigest()  # 返回加密内容


def send_email(user_id, objective='active'):
    # 传入id和目的(视图函数地址) 发送邮件
    try:
        ser = Serializer(settings.SECRET_KEY, expires_in=600)  # 声明一个对象
        token = ser.dumps({'id': user_id}).decode()  # 加密后的令牌 返回值为bytes 转为字符串
        title = '百知后台课程管理系统邮件'
        content = 'http://127.0.0.1:8000/reception/'+objective+'/?token='+token
        send = settings.EMAIL_HOST_USER
        receive = ['994225582@qq.com', ]
        send_mail(title, content, send, receive, fail_silently=False)
        return True
    except Exception as e:
        print(e)
        traceback.print_exc()


def active(request):
    token = request.GET.get("token")
    try:
        ser = Serializer(settings.SECRET_KEY, expires_in=600)  # 声明对象
        user_id = ser.loads(token).get("id")  # 从字典中获取值
        with transaction.atomic():
            user = UsersTable.objects.get(pk=user_id)
            if user.activation:
                return HttpResponse(user.username + '账户已经激活了')
            else:
                user.activation = True
                user.save()
                return HttpResponse('恭喜' + user.username + '账户被成功激活')
    except SignatureExpired:
        return HttpResponse('不好意思，链接已经失效！')
    except Exception as e:
        print(e)
        traceback.print_exc()
    return HttpResponse("激活失败")


def reactive(request):
    username = request.GET.get('username')
    user = UsersTable.objects.filter(username=username)
    if user:
        if send_email(user[0].id):
            return HttpResponse('sent')
    return HttpResponse('failed')


def register(request):
    return render(request, 'reception/register.html')


def get_captcha(request):  # 获取验证码
    img = ImageCaptcha()  # 创建验证码图片对象
    code = ''.join(random.sample(string.ascii_letters + string.digits, 4))  # 创建验证码
    request.session['code'] = code  # 保存验证码，待提交验证
    return HttpResponse(img.generate(code), 'image/png')  # 将验证码生成图片并返回验证码图片


def check_captcha(request):  # 验证验证码
    captcha = request.GET.get('captcha') or ''  # 获取用户输入的验证码
    return HttpResponse(captcha.lower() == request.session.get('code').lower())  # 返回验证结果


def check_user_name(request):  # 检查用户名是否存在
    user_name = request.GET.get('user_name')  # 获取用户输入的用户名
    return HttpResponse(bool(UsersTable.objects.filter(username=user_name)))  # 返回检查结果


def register_logic(request):  # 注册业务
    user_name = request.POST.get('user_name')
    pwd = request.POST.get('pwd')
    user_rst = re.findall(r'^[\u4e00-\u9fa5]{2,10}$', user_name)
    pwd_rst = re.findall(r'^\w{6,18}$', pwd)
    if user_rst and pwd_rst:  # 验证用户名密码是否合法
        salt = str(uuid.uuid4())  # 生成盐
        pwd = encryption(pwd, salt)  # 加密
        email = request.POST.get('email')
        try:
            with transaction.atomic():
                # 添加用户
                rst = UsersTable.objects.create(username=user_name, password=pwd, email=email, salt=salt)
                if rst:  # 如果添加成功则发送激活邮件
                    if send_email(rst.id):
                        return HttpResponse('success')
                    return HttpResponse('Failed to send mail')
        except Exception as e:
            print(e)
    return HttpResponse('fail')


def login(request):
    if request.COOKIES.get('login'):
        name = request.session['username']
        pwd = request.session['pwd']
        rst = UsersTable.objects.filter(username=name, password=pwd)
        if rst:
            request.session['id'] = {}
            return redirect('content:home')
    return render(request, 'reception/login.html')


def login_logic(request):
    username = request.POST.get('username')  # 获取用户名
    user = UsersTable.objects.filter(username=username)  # 根据用户名查找用户
    if user:  # 如果用户存在：
        pwd = encryption(request.POST.get('pwd'), user[0].salt)  # 对用户输入的密码加密
        if user[0].password == pwd:  # 如果加密后的密码与用户密码一致：
            response = HttpResponse('success')  # 创建返回对象“成功”
            if user[0].activation:  # 判断用户是否激活
                response.set_cookie('login', 'true')  # 设置登录状态为已登录
                request.session['username'] = username
                request.session['pwd'] = pwd
                request.session['id'] = {}
                if request.POST.get('remember') == 'true':  # 判断是否自动登录
                    response.set_cookie('login', 'true', max_age=7 * 24 * 3600)
            else:  # 未激活
                response = HttpResponse('not active')
            return response
    return HttpResponse('fail')


def forget(request):
    return render(request, 'reception/forget_pwd.html')


def forget_logic(request):  # 忘记密码验证
    # 获取用户名和邮箱并验证
    username = request.POST.get('user_name')
    email = request.POST.get('email')
    user = UsersTable.objects.filter(username=username, email=email)
    if user:
        if send_email(user[0].id, objective='reset_pwd'):  # 如果输入正确则发送重置密码邮件
            return HttpResponse('sent')
        return HttpResponse('Failed to send mail')
    return HttpResponse('fail')


def reset_pwd(request):
    token = request.GET.get("token")
    try:
        ser = Serializer(settings.SECRET_KEY, expires_in=600)
        user_id = ser.loads(token).get("id")
        if UsersTable.objects.filter(pk=user_id):
            request.session['user_id'] = user_id
            return render(request, 'reception/reset_pwd.html')
        return HttpResponse('token无效！')
    except SignatureExpired:
        return HttpResponse('不好意思，链接已经失效！')


def reset_logic(request):
    user_id = request.session.get('user_id')
    try:
        with transaction.atomic():
            user = UsersTable.objects.get(pk=user_id)
            pwd = request.POST.get('user_pwd')
            user.password = encryption(pwd, user.salt)
            user.save()
            del request.session['user_id']
            return HttpResponse('success')
    except Exception as e:
        traceback.print_exc()
        print(e)
    return HttpResponse('fail')


def logout(request):
    render(request, 'reception/logout.html')
