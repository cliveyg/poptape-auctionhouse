from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from auction.views import AuctionDetail, AuctionListCreate
from auction.views import AuctionLotListCreate, AuctionTypes
from auction.views import ComboAuctionCreate, AuctionByItem
from auction.views import AuctionValid

urlpatterns = [
    #url(r'^auctionhouse/auction/', include('rest_framework.urls', namespace='rest_framework')),

    # returns auction types available
    url('auctionhouse/types', AuctionTypes.as_view(), name="auctiontypes"),

    # read, edit, delete ops on auction
    url('auctionhouse/auction/(?P<auction_id>[0-9a-f-]{36})', AuctionDetail.as_view(), name="detail"),

    # create auction - probably superceded by ComboAuctionCreate
    url('auctionhouse/auction', AuctionListCreate.as_view(), name="createauction"),

    # create auction lot - probably superceded by ComboAuctionCreate
    url('auctionhouse/auction/lot', AuctionLotListCreate.as_view(), name="createlot"),

    # returns auction and lot data on a key of item_id
    url('auctionhouse/item/(?P<item_id>[0-9a-f-]{36})', AuctionByItem.as_view(), name="auctionbyitem"),

    # allows easier creation of auctions and lots - one http call instead of two or more
    url('auctionhouse/(?P<auction_type>[a-z]{4,5})/auction', ComboAuctionCreate.as_view(), name="combocreate"),

    # this url is for checking whether the auctioneer microservice has been sent the correct data
    url('auctionhouse/auction/(?P<auction_id>[0-9a-f-]{36})/(?P<lot_id>[0-9a-f-]{36})', 
                                                            AuctionValid.as_view(), name="validauction"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
