from django.urls import path

from reception import views

app_name = 'reception'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('check_user_name/', views.check_user_name, name='check_name'),
    path('get_captcha/', views.get_captcha, name='captcha'),
    path('check_captcha/', views.check_captcha, name='check'),
    path('register_logic/', views.register_logic, name='reg_logic'),
    path('login/', views.login, name='login'),
    path('login_logic/', views.login_logic, name='login_logic'),
    path('active/', views.active, name='active'),
    path('reactive/', views.reactive, name='reactive'),
    path('forget_pwd/', views.forget, name='forget'),
    path('forget_logic/', views.forget_logic, name='forget_logic'),
    path('reset_pwd/', views.reset_pwd, name='reset_pwd'),
    path('reset_logic/', views.reset_logic, name='reset_logic'),
    path('logout/', views.logout, name='logout'),
]
