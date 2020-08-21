from django import forms
from apps.forms import FormsMixin
from apps.news.models import News, Banner
from apps.course.models import Course


class NewsEditForm(forms.Form):
    pk = forms.IntegerField(error_messages={'required': '必须传入分类的id'})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm, FormsMixin):
    category = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']

class EditNewsForm(forms.ModelForm, FormsMixin):
    pk = forms.IntegerField()
    category = forms.IntegerField()
    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class BannerForm(forms.ModelForm, FormsMixin):
    class Meta:
        model = Banner
        fields = ['link_to', 'image_url', 'priority']


class EditBannerForm(forms.ModelForm, FormsMixin):
    pk = forms.IntegerField()

    class Meta:
        model = Banner
        fields = ['link_to', 'image_url', 'priority']


class CourseForm(forms.ModelForm, FormsMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ['category', 'teacher', 'pub_time']