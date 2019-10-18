"""auctionhouse URL Configuration

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
from django.urls import path, re_path
from django.conf.urls import url, include
from django.views.generic import RedirectView
from auctionhouse.views import StatusView

urlpatterns = [
    path('auctionhouse/admin/', admin.site.urls),
    path('auctionhouse/status/', StatusView.as_view(), name="status"),
    #path('auctionhouse', RedirectView.as_view(url='/auctionhouse/status')),
    #url(r'^', include('auction.urls')),
    re_path(r'^', include('auction.urls')),
]


