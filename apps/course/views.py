from django.shortcuts import render, redirect, reverse
from .models import Course, CourseOrder
from django.http import Http404
from django.conf import settings
import time, os, hmac, hashlib
from utils import restful
from apps.xfzauth.decorators import xfz_login_required
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import reverse
from django.utils.timezone import make_aware
from datetime import datetime


def course_list(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'course/course_index.html', context=context)


def course_detail(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        cover_url = course.cover_url
        buyed = CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists()
        context = {
            'course': course,
            'buyed': buyed,
        }
        return render(request, 'course/course_detail.html', context=context)
    except Course.DoesNotExist:
        raise Http404


def course_token(request):
    file = request.GET.get('video')

    course_id = request.GET.get('course_id')
    if not CourseOrder.objects.filter(course_id=course_id, buyer=request.user, status=2).exists():
        return restful.paramserror(message='请先购买')

    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})


@xfz_login_required
def course_order(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        if CourseOrder.objects.filter(course=course, buyer=request.user, status=2).exists():
            return redirect(reverse('course:course_detail', kwargs={'course_id': 6}))
        order = CourseOrder.objects.create(course=course, buyer=request.user, status=1, amount=course.price,
                                           pub_time=make_aware(datetime.now()))
        context = {
            'goods': course,
            'order': order,
            'notify_url': request.build_absolute_uri(reverse('course:notify_view')),
            'return_url': request.build_absolute_uri(reverse('course:course_detail', kwargs={'course_id': course.pk}))
        }
        return render(request, 'course/course_order.html', context=context)
    except Course.DoesNotExist:
        raise Http404


@xfz_login_required
def course_order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")
    uid = '82abeee6c74dd324d735aebb'
    token = 'f1081ec9f8ad3814f7579fc2317c4024'
    orderuid = str(request.user.pk)

    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    print('key:', key)
    return restful.result(data={"key": key})


@csrf_exempt
def notify_view(request):
    orderid = request.POST.get('orderid')
    print('=' * 10)
    print(orderid)
    print('=' * 10)
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()
