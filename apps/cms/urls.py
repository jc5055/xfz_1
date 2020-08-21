"""xfz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views, course_views, staff_views

app_name = 'cms'

urlpatterns = [
    path('index/', views.index_view, name='index'),
    path('write_news/', views.WriteNewsView.as_view(), name='write_news'),
    path('edit_news/', views.EditNewsView.as_view(), name='edit_news'),
    path('del_news/', views.del_news, name='edit_news'),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('news_category/', views.news_category, name='news_category'),
    path('add_category/', views.add_news_category, name='add_category'),
    path('edit_category/', views.edit_news_category, name='edit_category'),
    path('del_category/', views.del_news_category, name='del_category'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('qntoken/', views.qntoekn, name='qn_token'),
    path('banners/', views.news_banners, name='news_banners'),
    path('add_banner/', views.add_banner, name='add_banner'),
    path('del_banner/', views.del_banner, name='del_banner'),
    path('edit_banner/', views.edit_banner, name='edit_banner'),
    path('banner_list/', views.banner_list, name='banner_list'),

]
urlpatterns += [
    path('course/', course_views.PubCourse.as_view(), name='pub_course'),
]

urlpatterns += {
    path('staffs/', staff_views.index, name='staffs'),
    path('add_staff/', staff_views.AddStaffView.as_view(), name='add_staff'),
}