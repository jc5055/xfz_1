from django import forms
from apps.forms import FormsMixin
from .models import Banner


class CommentForm(forms.Form, FormsMixin):
    content = forms.CharField()
    news_id = forms.IntegerField()
