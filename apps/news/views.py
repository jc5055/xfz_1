from django.shortcuts import render
from .models import News, NewsCategory, Comment, Banner
from django.conf import settings
from utils import restful
from .serializers import NewsSerializer, NewsCommentSerializer
from django.http import Http404
from .forms import CommentForm
from apps.xfzauth.decorators import xfz_login_required
from django.db.models import Q


def index(request):
    newses = News.objects.select_related('category', 'author').order_by('-pub_time')[0: settings.ONE_PAGE_NEWS_COUNT]
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories,
        'banners': Banner.objects.all(),
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    p = int(request.GET.get('p', 1))
    category_id = int(request.GET.get('category_id', 0))
    start_index = (p - 1) * settings.ONE_PAGE_NEWS_COUNT
    end_index = start_index + settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        newses = News.objects.all()[start_index: end_index]
    else:
        newses = News.objects.select_related('category', 'author').filter(category_id=category_id)[
                 start_index: end_index]
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        news = News.objects.select_related('category', 'author').prefetch_related("comments__author").get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404


@xfz_login_required
def add_news_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
    try:
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        serializer = NewsCommentSerializer(comment)
        return restful.result(data=serializer.data)
    except:
        return restful.paramserror(message='新闻不存在')

    return restful.paramserror(message='请求参数异常')


def search(request):
    q = request.GET.get('q')
    if q:
        newses = News.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
        context = {'newses': newses, 'q': q}
        return render(request, 'search/search.html', context=context)
    else:
        return render(request, 'search/search.html')
