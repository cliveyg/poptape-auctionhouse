from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from auction.views import AuctionDetail, AuctionListCreate, AuctionLotListCreate
#path('snippets/<int:pk>/', views.SnippetDetail.as_view()),

urlpatterns = [
    #url(r'^auctionhouse/auction/', include('rest_framework.urls', namespace='rest_framework')),
    url('auctionhouse/auction/(?P<auction_id>[0-9a-f-]{36})', AuctionDetail.as_view(), name="detail"),
    #url('auctionhouse/auction/(?P<auction_id>[0-9a-f-]{36})/', AuctionLotListCreate.as_view(), name="createlot"),
    url('auctionhouse/auction', AuctionListCreate.as_view(), name="createauction"),
    #url('auctionhouse/(?P<auction_id>[0-9a-f-]{36})', AuctionDetail.as_view(), name="detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
