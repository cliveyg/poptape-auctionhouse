from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from auction.views import AuctionDetail, AuctionListCreate
from auction.views import AuctionLotListCreate, AuctionTypes
from auction.views import ComboAuctionCreate, AuctionByItem
from auction.views import AuctionValid

urlpatterns = [
    #path('auctionhouse/auction/', include('rest_framework.urls', namespace='rest_framework')),

    # returns auction types available
    path('auctionhouse/types/', AuctionTypes, name='auctiontypes'),

    # create auction - probably superceded by ComboAuctionCreate
    path('auctionhouse/auction/', AuctionListCreate.as_view(), name='createauction'),

    # returns auction and lot data on a key of item_id
    path('auctionhouse/auction/item/<uuid:item_id>/', AuctionByItem.as_view(), name='auctionbyitem'),

    # this url is for checking whether the auctioneer microservice has been sent the correct data
    path('auctionhouse/auction/<uuid:auction_id>/<uuid:lot_id>/',
                                                            AuctionValid.as_view(), name='validauction'),

    # read, edit, delete ops on auction
    path('auctionhouse/auction/<uuid:auction_id>/', AuctionDetail.as_view(), name='auctiondetail'),

    # create auction lot - probably superceded by ComboAuctionCreate
    path('auctionhouse/auction/lot', AuctionLotListCreate.as_view(), name='createlot'),

    # allows easier creation of auctions and lots - one http call instead of two or more
    path('auctionhouse/<str:auction_type>/auction/', ComboAuctionCreate.as_view(), name='combocreate'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
