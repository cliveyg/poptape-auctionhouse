from django.test import SimpleTestCase
from django.urls import resolve, reverse
from auction.urls import AuctionTypes, AuctionListCreate, AuctionJanitor
from auction.urls import AuctionByItem, AuctionLotDetail
import uuid


class TestURLS(SimpleTestCase):

    def test_api_auction_types_is_resolved(self):
        url = reverse('auctiontypes')
        self.assertEquals(resolve(url).url_name, 'auctiontypes')
        self.assertEquals(resolve(url).func.view_class, AuctionTypes)
        self.assertEquals(resolve(url).route, '^auctionhouse/auction/types/')

    def test_api_createauction_is_resolved(self):
        url = reverse('createauction')
        self.assertEquals(resolve(url).url_name, 'createauction')
        self.assertEquals(resolve(url).func.view_class, AuctionListCreate)
        self.assertEquals(resolve(url).route, '^auctionhouse/auction/')

    def test_api_janitor_is_resolved(self):
        url = reverse('janitor')
        self.assertEquals(resolve(url).url_name, 'janitor')
        self.assertEquals(resolve(url).func.view_class, AuctionJanitor)
        self.assertEquals(resolve(url).route, '^auctionhouse/janitor/')

    def test_api_auctionbyitem_is_resolved(self):
        test_uuid = str(uuid.uuid4())
        url = reverse('auctionbyitem', args=[test_uuid])
        self.assertEquals(resolve(url).url_name, 'auctionbyitem')
        self.assertEquals(resolve(url).func.view_class, AuctionByItem)
        self.assertEquals(resolve(url).route, '^auctionhouse/auction/item/<uuid:item_id>/')
        self.assertEquals(str(resolve(url).captured_kwargs['item_id']), test_uuid)

    def test_api_auctionlotdetail_is_resolved(self):
        test_uuid = str(uuid.uuid4())
        url = reverse('auctionlotdetail', args=[test_uuid])
        self.assertEquals(resolve(url).url_name, 'auctionlotdetail')
        self.assertEquals(resolve(url).func.view_class, AuctionLotDetail)
        self.assertEquals(resolve(url).route, '^auctionhouse/auction/lot/<uuid:lot_uuid>/')
        self.assertEquals(str(resolve(url).captured_kwargs['lot_uuid']), test_uuid)