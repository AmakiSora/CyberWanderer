"""CyberWanderer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', page_hello),
    path('youGet/', get_resource),
    path('twitter/', include('twitter.urls')),
    path('translate/', include('translate.urls')),
    path('bilibili/', include('bilibili.urls'))
    # path('test/<str:username>', page_test), #匹配string
    # path('test/<int:num>',page_test),  # 匹配int
    # path('test/<path:ph>', page_test),#匹配带/的string
    # path('test/<slug:sl>', page_test),#匹配任意ASCII码的短标签
]