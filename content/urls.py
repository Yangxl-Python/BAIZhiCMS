from django.urls import path

from content import views

app_name = 'content'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('add_article/', views.add_article, name='add_article'),
    path('article_logic/', views.article_logic, name='article_logic'),
    path('add_course/', views.add_course, name='add_course'),
    path('course_logic/', views.course_logic, name='course_logic'),
    path('modify/', views.modify, name='modify'),
    path('modify_logic/', views.modify_logic, name='modify_logic'),
    path('delete/', views.delete, name='delete'),
]
