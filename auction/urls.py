from django.contrib import admin
#from django.conf.urls import url, include
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from auction.views import AuctionDetail, AuctionListCreate
from auction.views import AuctionLotListCreate, AuctionTypes
from auction.views import ComboAuctionCreate, AuctionByItem
from auction.views import AuctionValid, AuctionLotDetail
from auction.views import AuctionJanitor, Return404
from auction.views import custom404

urlpatterns = [
    #path('auctionhouse/auction/', include('rest_framework.urls', namespace='rest_framework')),

    # returns auction types available
    path('auctionhouse/auction/types/', AuctionTypes.as_view(), name='auctiontypes'),

    # create auction - probably superceded by ComboAuctionCreate
    path('auctionhouse/auction/', AuctionListCreate.as_view(), name='createauction'),

    # create auction - probably superceded by ComboAuctionCreate
    path('auctionhouse/janitor/', AuctionJanitor.as_view(), name='janitor'),

    # returns auction and lot data on a key of item_id
    path('auctionhouse/auction/item/<uuid:item_id>/', AuctionByItem.as_view(), name='auctionbyitem'),

    # returns an auction lot's details including bid history
    path('auctionhouse/auction/lot/<uuid:lot_uuid>/', AuctionLotDetail.as_view(), name="auctionlotdetail"),

    # this url is for checking whether the auctioneer microservice has been sent the correct data
    path('auctionhouse/auction/<uuid:auction_id>/<uuid:lot_id>/', AuctionValid.as_view(), name='validauction'),

    # read, edit, delete ops on auction
    path('auctionhouse/auction/<uuid:auction_id>/', AuctionDetail.as_view(), name='auctiondetail'),

    # create auction lot - probably superceded by ComboAuctionCreate
    path('auctionhouse/auction/lot/', AuctionLotListCreate.as_view(), name='createlot'),

    # allows easier creation of auctions and lots - one http call instead of two or more
    path('auctionhouse/<str:auction_type>/auction/', ComboAuctionCreate.as_view(), name='combocreate'),

    re_path(r'^auctionhouse/$', Return404.as_view(), name='404'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

handler404 = custom404
