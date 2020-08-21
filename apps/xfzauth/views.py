from django.shortcuts import render, HttpResponse, reverse, redirect
from django.views.decorators.http import require_POST
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from .models import User
from utils import restful
from django.views.decorators.csrf import csrf_exempt
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from ronglian_sms_sdk import SmsSDK
import random
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .forms import RegisterForm

User = get_user_model()


def test(request):
    User.objects.create_user(telephone='13588406767', username='jc2', password='qa123456')
    return HttpResponse('SUCCESS')


@require_POST
@csrf_exempt
def login_view(request):
    print('test')
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')

        user = authenticate(request, username=telephone, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unautherror(message="您的账号已被冻结！")
        else:
            return restful.paramserror(message="手机号或着密码错误")
    else:
        errors = form.get_errors()
        return restful.paramserror(message=errors)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@require_POST
def register(request):
    # 表单的数据校验
    form = RegisterForm(request.POST)
    # 表单校验成功，写数据库
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password1')
        username = form.cleaned_data.get('username')
        user = User.objects.create_user(telephone=telephone, password=password, username=username)
        login(request, user)
        return restful.ok()
    else:
        return restful.paramserror(message=form.get_errors())


def img_captcha(request):
    text, image = Captcha.gene_code()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()

    cache.set(text.lower(), text.lower(), 5 * 60)
    return response


def sms_captcha(request):
    # https://www.yuntongxun.com/member/main
    telephone = request.GET.get('telephone')
    accId = '8aaf0708732220a60173b317e2b24122'
    accToken = '0936dd93f55a4639a9a38fcdaaf439bf'
    appId = '8aaf0708732220a60173b317e39c4129'
    sdk = SmsSDK(accId, accToken, appId)
    # 模版,默认用1
    tid = '1'
    # 发送手机号
    mobile = telephone
    # 验证码
    code = str(random.randint(1000, 9999))
    datas = (code, 5)
    # result = sdk.sendMessage(tid, mobile, datas)
    print("短信验证码：", code)
    cache.set(telephone, code)

    return restful.ok()


def cache_test(request):
    cache.set('username', 'xxs211', 60)
    rs = cache.get('username')
    return HttpResponse(rs)
