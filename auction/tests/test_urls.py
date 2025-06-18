from django.test import SimpleTestCase
from django.urls import resolve, reverse
from auction.urls import AuctionTypes, AuctionListCreate, AuctionJanitor
from auction.urls import AuctionByItem, AuctionLotDetail, AuctionValid, Return404
from auction.urls import AuctionDetail, AuctionLotListCreate, ComboAuctionCreate
import uuid


class TestURLSResolve(SimpleTestCase):

    def test_api_auction_types_is_resolved(self):
        url = reverse('auctiontypes')
        self.assertEqual(resolve(url).url_name, 'auctiontypes')
        self.assertEqual(resolve(url).func.view_class, AuctionTypes)
        self.assertEqual(resolve(url).route, '^auctionhouse/auction/types/')

    def test_api_createauction_is_resolved(self):
        url = reverse('createauction')
        self.assertEqual(resolve(url).url_name, 'createauction')
        self.assertEqual(resolve(url).func.view_class, AuctionListCreate)
        self.assertEqual(resolve(url).route, '^auctionhouse/auction/')

    def test_api_janitor_is_resolved(self):
        url = reverse('janitor')
        self.assertEqual(resolve(url).url_name, 'janitor')
        self.assertEqual(resolve(url).func.view_class, AuctionJanitor)
        self.assertEqual(resolve(url).route, '^auctionhouse/janitor/')

    def test_api_auctionbyitem_is_resolved(self):
        test_uuid = str(uuid.uuid4())
        url = reverse('auctionbyitem', args=[test_uuid])
        self.assertEqual(resolve(url).url_name, 'auctionbyitem')
        self.assertEqual(resolve(url).func.view_class, AuctionByItem)
        self.assertEqual(resolve(url).route, '^auctionhouse/auction/item/<uuid:item_id>/')
        self.assertEqual(str(resolve(url).captured_kwargs['item_id']), test_uuid)

    def test_api_auctionlotdetail_is_resolved(self):
        test_uuid = str(uuid.uuid4())
        url = reverse('auctionlotdetail', args=[test_uuid])
        self.assertEqual(resolve(url).url_name, 'auctionlotdetail')
        self.assertEqual(resolve(url).func.view_class, AuctionLotDetail)
        self.assertEqual(resolve(url).route, '^auctionhouse/auction/lot/<uuid:lot_uuid>/')
        self.assertEqual(str(resolve(url).captured_kwargs['lot_uuid']), test_uuid)

    def test_api_validauction_is_resolved(self):
        auc_uuid = str(uuid.uuid4())
        lot_uuid = str(uuid.uuid4())
        url = reverse('validauction', args=[auc_uuid, lot_uuid])
        self.assertEqual(resolve(url).url_name, 'validauction')
        self.assertEqual(resolve(url).func.view_class, AuctionValid)
        self.assertEqual(resolve(url).route, '^auctionhouse/auction/<uuid:auction_id>/<uuid:lot_id>/')
        self.assertEqual(str(resolve(url).captured_kwargs['auction_id']), auc_uuid)
        self.assertEqual(str(resolve(url).captured_kwargs['lot_id']), lot_uuid)

    def test_api_auctiondetail_is_resolved(self):
        auc_uuid = str(uuid.uuid4())
        url = reverse('auctiondetail', args=[auc_uuid])
        self.assertEqual(resolve(url).url_name, 'auctiondetail')
        self.assertEqual(resolve(url).func.view_class, AuctionDetail)
        self.assertEqual(resolve(url).route, '^auctionhouse/auction/<uuid:auction_id>/')
        self.assertEqual(str(resolve(url).captured_kwargs['auction_id']), auc_uuid)

    def test_api_createlot_is_resolved(self):
        url = reverse('createlot')
        self.assertEqual(resolve(url).url_name, 'createlot')
        self.assertEqual(resolve(url).func.view_class, AuctionLotListCreate)
        self.assertEqual(resolve(url).route, '^auctionhouse/auction/lot/')

    def test_api_combocreate_is_resolved(self):
        url = reverse('combocreate', args=['dutch'])
        self.assertEqual(resolve(url).url_name, 'combocreate')
        self.assertEqual(resolve(url).func.view_class, ComboAuctionCreate)
        self.assertEqual(resolve(url).route, '^auctionhouse/<str:auction_type>/auction/')
        self.assertEqual(resolve(url).captured_kwargs['auction_type'], 'dutch')
