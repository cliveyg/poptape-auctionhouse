from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from auction.views import AuctionDetail, AuctionListCreate
from auction.views import AuctionLotListCreate, AuctionTypes
from auction.views import ComboAuctionCreate, AuctionByItem

urlpatterns = [
    #url(r'^auctionhouse/auction/', include('rest_framework.urls', namespace='rest_framework')),
    #url('auctionhouse/auction/(?P<auction_id>[0-9a-f-]{36})/lot', AuctionLotListCreate.as_view(), name="createlot"),
    #url('auctionhouse/(?P<auction_id>[0-9a-f-]{36})', AuctionDetail.as_view(), name="detail"),

    url('auctionhouse/types', AuctionTypes.as_view(), name="auctiontypes"),

    url('auctionhouse/auction/(?P<auction_id>[0-9a-f-]{36})', AuctionDetail.as_view(), name="detail"),
    url('auctionhouse/auction', AuctionListCreate.as_view(), name="createauction"),
    url('auctionhouse/auction/lot', AuctionLotListCreate.as_view(), name="createlot"),

    url('auctionhouse/item/(?P<item_id>[0-9a-f-]{36})', AuctionByItem.as_view(), name="auctionbyitem"),
    url('auctionhouse/(?P<auction_type>[a-z]{4,5})/auction', ComboAuctionCreate.as_view(), name="combocreate"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
