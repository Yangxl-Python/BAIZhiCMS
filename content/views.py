import traceback

from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse  # , JsonResponse
from django.shortcuts import render, redirect
from content.models import CategoryTable, CurriculumTable, EssayTable


def home(request):
    try:
        order = request.GET.get('order') or 'id'
        page_num = request.GET.get('pge') or 1
        if request.GET.get('home') == 'home':
            request.session['id'] = {}
        gid = request.GET.get('gid') or request.session['id'].get('gid')
        cid = request.GET.get('cid') or request.session['id'].get('cid')
        if gid:
            paginator = Paginator(object_list=EssayTable.objects.filter(curriculum__category_id=gid).order_by(order),
                                  per_page=5)
            url = 'content/python.html'
            request.session['id'] = {'gid': gid}
        elif cid:
            paginator = Paginator(object_list=EssayTable.objects.filter(curriculum_id=cid).order_by(order),
                                  per_page=5)
            url = 'content/pythonBase.html'
            request.session['id'] = {'cid': cid}
        else:
            paginator = Paginator(object_list=EssayTable.objects.all().order_by(order),
                                  per_page=5)
            url = 'content/home.html'
        essay = paginator.page(page_num)
        cate = CategoryTable.objects.all()
        curr = CurriculumTable.objects.all()
        data = {'essay': essay, 'category': cate, 'curriculum': curr, 'order': order}
        return render(request, url, data)
    except Exception as e:
        traceback.print_exc()
        print(e)
    redirect('reception:login')


def add_article(request):
    cate = CategoryTable.objects.all()
    curr = CurriculumTable.objects.all()
    return render(request, 'content/addArticle.html', {'cate': cate, 'curr': curr})


def article_logic(request):
    name = request.POST.get('name')
    cate = request.POST.get('cate_sel')
    time = request.POST.get('time')
    text = request.POST.get('text')
    try:
        with transaction.atomic():
            rst = EssayTable.objects.create(name=name, curriculum_id=cate, submit_time=time, content=text)
            if rst:
                return HttpResponse('success')
    except Exception as e:
        traceback.print_exc()
        print(e)
    return HttpResponse('fail')


def add_course(request):
    cate = CategoryTable.objects.all()
    return render(request, 'content/addCourse.html', {'cate': cate})


def course_logic(request):
    try:
        name = request.GET.get('name')
        course = int(request.GET.get('course'))
        with transaction.atomic():
            if course:
                cate = int(request.GET.get('cate_sel'))
                rst = CurriculumTable.objects.create(name=name, category_id=cate)
            else:
                rst = CategoryTable.objects.create(name=name)
            if rst:
                return HttpResponse('success')
    except Exception as e:
        print(e)
        traceback.print_exc()
    return HttpResponse('fail')


def modify(request):
    eid = request.GET.get('id')
    essay = EssayTable.objects.filter(pk=eid)
    if essay:
        cate = CategoryTable.objects.all()
        curr = CurriculumTable.objects.all()
        return render(request, 'content/modify.html', {'essay': essay[0],
                                                       'cate': cate,
                                                       'curr': curr})
    return HttpResponse('文章不存在')


def modify_logic(request):
    eid = request.POST.get('id')
    name = request.POST.get('name')
    cate = request.POST.get('cate_sel')
    time = request.POST.get('time')
    content = request.POST.get('content')
    try:
        with transaction.atomic():
            essay = EssayTable.objects.get(pk=eid)
            essay.name = name
            essay.curriculum_id = cate
            essay.submit_time = time
            essay.content = content
            essay.save()
            return HttpResponse('success')
    except Exception as e:
        traceback.print_exc()
        print(e)
    return HttpResponse('fail')


def delete(request):
    eid = request.GET.get('id')
    try:
        with transaction.atomic():
            rst = EssayTable.objects.filter(pk=eid)
            if rst:
                rst[0].delete()
                return HttpResponse('success')
    except Exception as e:
        traceback.print_exc()
        print(e)
    return HttpResponse('fail')
