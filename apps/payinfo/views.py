from django.shortcuts import render, reverse
from .models import PayInfo, PayInfoOrder
from apps.xfzauth.decorators import xfz_login_required
from utils import restful
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.http import Http404, FileResponse


def payinfo_index(request):
    payinfos = PayInfo.objects.all()
    context = {
        'payInfos': payinfos
    }
    return render(request, 'payinfo/payinfo.html', context=context)


@xfz_login_required
def payinfo_order(request):
    payinfo_id = request.GET.get('payinfo_id')
    payInfo = PayInfo.objects.get(pk=payinfo_id)
    order = PayInfoOrder.objects.create(payinfo=payInfo, buyer=request.user, amount=payInfo.price)
    context = {
        'goods': {
            'cover_url': 'http://xfz.cn/static/build/images/web-bp-pc.png',
            'title': payInfo.title,
            'price': payInfo.price,
        },
        'order': order,
        'notify_url': request.build_absolute_uri(reverse('payInfo:notify_view')),
        'return_url': request.build_absolute_uri(reverse('payInfo:index')),
    }

    return render(request, 'course/course_order.html', context=context)


@csrf_exempt
def notify_view(request):
    order_id = request.POST.get('order_id')
    PayInfoOrder.objects.filter(pk=order_id).update(status=2)
    return restful.ok()


@xfz_login_required
def download(request):
    payinfo_id = request.GET.get('payinfo_id')
    order = PayInfoOrder.objects.filter(payinfo_id=payinfo_id, buyer=request.user, status=2).first()
    if order:
        payinfo = order.payinfo
        path = payinfo.path
        fp = open(os.path.join(settings.MEDIA_ROOT, path), 'rb')
        response = FileResponse(fp)
        response['Content-Type'] = 'image/jpeg'
        response['Content-Disposition'] = 'attachment;filename="%s"' % path.split("/")[-1]
        return response
    else:
        return Http404
