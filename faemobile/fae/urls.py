"""fae URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from userinfo import views
import xadmin 
xadmin.autodiscover()
# version模块自动注册需要版本控制的 Model
# from xadmin.plugins import xversion
# xversion.register_models()

urlpatterns = [
    # path('admin/', admin.site.urls),
    url('boss', xadmin.site.urls),
    url(r'^userinfo/', include('userinfo.urls')),
    url(r'^$', views.index),
    url(r'^forminfo/', include('forminfo.urls')),
    url(r'^welcome$',views.wel),
    url(r'^welcome_1$',views.wel_1),
    url(r'^welcome_2$',views.wel_2),
    url(r'^homepage',views.homepage),
    url(r'^index',views.index_),
    url(r'^sellinfo/',include('sellinfo.urls')),
    url(r'^serviceinfo/',include('serviceinfo.urls'))
]
