"""farmbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from homepage import urls as api_urls
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'dataserver/',include('dataserver.urls')),
    url(r'manage/',include('management.urls')),
    url(r'zxserver/',include('zxserver.urls')),
    url(r'homepage/',include('homepage.urls')),
    url(r'api/',include(api_urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),

]
