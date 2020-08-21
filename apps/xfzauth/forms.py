from django import forms
from apps.forms import FormsMixin
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form, FormsMixin):
    telephone = forms.CharField(max_length=11)
    password = forms.CharField(max_length=20, min_length=6,
                               error_messages={
                                   "max_length": "密码不能超过20个字符",
                                   "min_length": "密码最少不能小于6个字符"
                               })
    remember = forms.IntegerField(required=False)


class RegisterForm(forms.Form, FormsMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=20, min_length=6,
                                error_messages={
                                    "max_length": "密码不能超过20个字符",
                                    "min_length": "密码最少不能小于6个字符"
                                })
    password2 = forms.CharField(max_length=20, min_length=6,
                                error_messages={
                                    "max_length": "密码不能超过20个字符",
                                    "min_length": "密码最少不能小于6个字符"
                                })

    img_captcha = forms.CharField(max_length=4, min_length=4)
    sms_captcha = forms.CharField(max_length=4, min_length=4)

    def clean(self):
        clean_data = super(RegisterForm, self).clean()
        password1 = clean_data.get('password1')
        password2 = clean_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('前后两次密码不一致')

        img_captcha = clean_data.get('img_captcha')
        if not img_captcha:
            raise forms.ValidationError('请先输入图形验证码')

        # cache_img_captcha = cache.get(img_captcha.lower())
        # if not cache_img_captcha or img_captcha != cache_img_captcha:
        #     raise forms.ValidationError('图形验证码错误')

        telephone = clean_data.get('telephone')
        cache_sms_captcha = cache.get(telephone)
        sms_captcha = clean_data.get('sms_captcha')
        if not cache_sms_captcha or cache_sms_captcha != sms_captcha:
            raise forms.ValidationError('短信验证码错误')

        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('手机号已经被注册')
