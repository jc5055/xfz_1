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
from . import views
app_name = 'payInfo'
urlpatterns = [
    path('', views.payinfo_index, name="index"),
    path('payinfo_order/', views.payinfo_order, name="payinfo_order"),
    path('notify_url/', views.notify_view, name="notify_view"),
    path('download/', views.download, name="download"),
]
