"""transportation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from traffic import views
from traffic import routes

urlpatterns = [
    url(r'^$', views.index),
    url(r'^red$', views.red),
    url(r'^green$', views.green),
    url(r'^yellow$', views.yellow),
    url(r'^points$', views.get_points),
    url(r'^navigate$', views.navigate),
    url(r'^admin/', admin.site.urls),
    url(r'^edges/', views.get_edges),
    url(r'^image$', views.get_image),
    url(r'^test$', views.test),
    url(r'^shortest$', views.shorttest),
    url(r'^weeks$', views.weeks)
]
