from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from reception.models import UsersTable


class MyMiddleware(MiddlewareMixin):  # 自定义的中间件
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)

    # view处理请求前执行
    def process_request(self, request):  # 某一个view
        if 'reception/' not in request.path:
            if request.COOKIES.get('login'):
                name = request.session['username']
                pwd = request.session['pwd']
                rst = UsersTable.objects.filter(username=name, password=pwd)
                if rst:
                    return
            return redirect('reception:login')
