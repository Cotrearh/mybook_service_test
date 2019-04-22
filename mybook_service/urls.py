"""cotrearh_blog_site URL Configuration

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
from django.urls import path, include, re_path
from . import views
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from mybook_site import settings

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'login', views.login, name='login'),
    re_path(r'logout', views.logout, name='logout'),
    # re_path(r'^.+', views.custom_redirect_to_index, name='custom_redirect_to_index')
]
