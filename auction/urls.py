from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^auctionhouse/auction/', include('rest_framework.urls', namespace='rest_framework')),
]


