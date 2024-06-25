# auctionhouse/tests/test_api.py
import uuid

from django.test import TransactionTestCase
from rest_framework.test import RequestsClient
from .test_setup import create_auction_and_lots
import logging
import json
from requests.models import Response
from unittest.mock import Mock
from unittest import mock
from auction.models import Auction
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def mocked_auth_success(*args, **kwargs):
    r = Mock(spec=Response)
    r.status_code = 200
    r.headers = {'Content-Type': 'application/json'}
    r.json.return_value = {'public_id': 'Yarp'}
    return r


def mocked_auth_fail_403(*args, **kwargs):
    r = Mock(spec=Response)
    r.status_code = 200
    r.headers = {'Content-Type': 'application/json'}
    r.json.return_value = {'public_id': 'Yarp'}
    return r


# helper function to compare json objects
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


class TestAPIPaths(TransactionTestCase):

    @classmethod
    def setUp(cls):
        cls.auction = Auction()
        cls.lots = []
        cls.auction, cls.lots = create_auction_and_lots(cls)

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_validate_auction_ok(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        with mock.patch('rest_framework.request.user.get_username') as mock_get:
            mock_user = User(username=self.auction.public_id, first_name='Blinky')
            mock_get.return_value = mock_user.username
        r = c.get('http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/'+self.lots[1].lot_id+'/', headers=header)
        logger.info("MEEP status code is %s", r.status_code)
        assert r.status_code == 200
        assert r.headers.get('Content-Type') == 'application/json'

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_get_auction_list(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r = c.get('http://localhost/auctionhouse/auction/', headers=header)
        returned_data = r.json()
        assert returned_data[0]['auction_id'] == self.auction.auction_id
        assert r.status_code == 200
        assert r.headers.get('Content-Type') == 'application/json'

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_get_auction_by_item_id(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r = c.get('http://localhost/auctionhouse/auction/item/'+self.lots[0].item_id+'/', headers=header)
        returned_data = r.json()
        assert returned_data['auction']['auction_id'] == self.auction.auction_id
        assert returned_data['auction']['public_id'] == self.auction.public_id
        assert returned_data['auction']['lots'][0]['lot_id'] == self.lots[0].lot_id
        assert returned_data['auction']['lots'][1]['lot_id'] == self.lots[1].lot_id
        assert returned_data['auction']['delivery_options']['collection'] == True
        assert returned_data['auction']['payment_options']['mastercard'] == True
        assert r.url == 'http://localhost/auctionhouse/auction/item/'+self.lots[0].item_id+'/'
        assert r.status_code == 200
        assert r.headers.get('Content-Type') == 'application/json'

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_create_auction_fail(self, mock_get):
        c = RequestsClient()
        headers = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g',
                   'Content-Type': 'application/json'}
        public_id = str(uuid.uuid4())
        input = {"public_id": public_id,
                 "lots": [self.lots[0].lot_id],
                 "type": "EN",
                 "name": "Test Auction",
                 "multiple": False,
                 "start_time": "2024-06-23 20:18:21.910326",
                 "end_time": "2024-06-24 20:18:21.910326",
                 "status": "created",
                 "active": "yarp",
                 "currency": "GBP",
                 "start_price": "iffy",
                 "reserve_price": 550.00,
                 "min_increment": 10.00}
        r = c.post('http://localhost/auctionhouse/auction/', data=json.dumps(input), headers=headers)
        assert r.status_code == 400

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_create_auction(self, mock_get):
        c = RequestsClient()
        headers = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g',
                   'Content-Type': 'application/json'}
        public_id = str(uuid.uuid4())
        input = {"public_id": public_id,
                 "lots": [self.lots[0].lot_id],
                 "type": "EN",
                 "name": "Test Auction",
                 "multiple": False,
                 "start_time": "2024-06-23 20:18:21.910326",
                 "end_time": "2024-06-24 20:18:21.910326",
                 "status": "created",
                 "active": True,
                 "currency": "GBP",
                 "start_price": 200.00,
                 "reserve_price": 550.00,
                 "min_increment": 10.00}
        r = c.post('http://localhost/auctionhouse/auction/', data=json.dumps(input), headers=headers)
        returned_data = r.json()
        assert r.status_code == 201
        assert returned_data['public_id'] == public_id

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_edit_auction_by_id_fail(self, mock_get):
        c = RequestsClient()
        headers = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g',
                   'Content-Type': 'application/json'}

        dicky = self.auction.__dict__
        # have to remove and change some stuff to make this work
        del dicky['_state']
        del dicky['created']
        del dicky['modified']
        dicky['currency'] = 'BRL'
        td1 = dicky['start_time']
        dicky['start_time'] = str(td1)
        td2 = dicky['end_time']
        dicky['end_time'] = str(td2)
        dicky['random'] = 'Yarp'
        dicky['active'] = 'Beep'

        r = c.put('http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/', data=json.dumps(dicky), headers=headers)

        assert r.url == 'http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/'
        assert r.status_code == 400
        assert r.headers.get('Content-Type') == 'application/json'

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_delete_auction_by_id(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r1 = c.delete('http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/', headers=header)
        assert r1.status_code == 410

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_edit_auction_by_id(self, mock_get):
        c = RequestsClient()
        headers = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g',
                   'Content-Type': 'application/json'}

        assert self.auction.currency == 'GBP'

        dicky = self.auction.__dict__
        # have to remove and change some stuff to make this work
        del dicky['_state']
        del dicky['created']
        del dicky['modified']
        dicky['currency'] = 'BRL'
        td1 = dicky['start_time']
        dicky['start_time'] = str(td1)
        td2 = dicky['end_time']
        dicky['end_time'] = str(td2)

        r = c.put('http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/', data=json.dumps(dicky), headers=headers)
        returned_data = r.json()

        assert returned_data['currency'] == 'BRL'
        assert returned_data['auction_id'] == self.auction.auction_id
        assert returned_data['public_id'] == self.auction.public_id
        assert returned_data['lots'][0]== self.lots[0].lot_id
        assert returned_data['lots'][1] == self.lots[1].lot_id
        assert r.url == 'http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/'
        assert r.status_code == 202
        assert r.headers.get('Content-Type') == 'application/json'


    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_fail_get_auction_by_id_not_valid_uuid(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r = c.get('http://localhost/auctionhouse/auction/notvaliduuid', headers=header)
        assert r.status_code == 404
        assert r.headers.get('Content-Type') == 'application/json'

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_get_auction_by_id(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r = c.get('http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/', headers=header)
        returned_data = r.json()
        assert returned_data['auction']['auction_id'] == self.auction.auction_id
        assert returned_data['auction']['public_id'] == self.auction.public_id
        assert returned_data['auction']['lots'][0]['lot_id'] == self.lots[0].lot_id
        assert returned_data['auction']['lots'][1]['lot_id'] == self.lots[1].lot_id
        assert r.url == 'http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/'
        assert r.status_code == 200
        assert r.headers.get('Content-Type') == 'application/json'

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_get_by_lot_id(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r = c.get('http://localhost/auctionhouse/auction/lot/'+self.lots[0].lot_id+'/', headers=header)
        returned_data = r.json()

        assert r.url == 'http://localhost/auctionhouse/auction/lot/'+self.lots[0].lot_id+'/'
        assert r.status_code == 200
        assert r.headers.get('Content-Type') == 'application/json'
        assert returned_data['lot_id'] == self.lots[0].lot_id
        assert returned_data['auction_id'] == self.auction.auction_id
        assert returned_data['public_id'] == self.auction.public_id
        assert returned_data['start_price'] == self.lots[0].start_price
        assert returned_data['min_increment'] == self.lots[0].min_increment
        assert returned_data['reserve_price'] == self.lots[0].reserve_price

    def test_fail_get_auction_no_auth(self):
        c = RequestsClient()
        r = c.get('http://localhost/auctionhouse/auction/'+self.auction.auction_id+'/')
        assert r.status_code == 403
        assert r.headers.get('Content-Type') == 'application/json'

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_fail_get_auction_by_id_404(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r = c.get('http://localhost/auctionhouse/auction/'+str(uuid.uuid4())+'/', headers=header)
        assert r.status_code == 404
        assert r.headers.get('Content-Type') == 'application/json'

    def test_status_ok_no_auth(self):
        c = RequestsClient()
        r = c.get('http://localhost/auctionhouse/status')
        assert r.status_code == 200
        assert r.headers.get('Content-Type') == 'application/json'

    def test_return_404(self):
        c = RequestsClient()
        r = c.get('http://localhost/auctionhouse/some404')
        assert r.status_code == 404
        assert r.headers.get('Content-Type') == 'application/json'

    def test_delete_non_existent_resource(self):
        c = RequestsClient()
        r = c.delete('http://localhost/auctionhouse/blinky')
        assert r.status_code == 404
        assert r.headers.get('Content-Type') == 'application/json'

    def test_edit_non_existent_resource(self):
        c = RequestsClient()
        r = c.put('http://localhost/auctionhouse/blinky', data={'moo': 'cow'})
        assert r.status_code == 404
        assert r.headers.get('Content-Type') == 'application/json'

    def test_return_status_when_content_type_incorrect(self):
        c = RequestsClient()
        header = {'Content-Type': 'text/html'}
        r = c.get('http://localhost/auctionhouse/status', headers=header)
        assert r.headers.get('Content-Type') == 'application/json'
        assert r.status_code == 200

    def test_get_auction_types(self):
        c = RequestsClient()
        r = c.get('http://localhost/auctionhouse/auction/types')
        expected = {'valid_types': [{'key': 'EN', 'label': 'English'},
                                    {'key': 'BN', 'label': 'Buy Now'},
                                    {'key': 'DU', 'label': 'Dutch'}]}
        returned_data = r.json()
        assert r.status_code == 200
        assert ordered(expected) == ordered(returned_data)

    def test_try_to_delete_auction_types(self):
        c = RequestsClient()
        r = c.delete('http://localhost/auctionhouse/auction/types')
        assert r.status_code == 405

    def test_try_to_edit_auction_types(self):
        c = RequestsClient()
        r = c.put('http://localhost/auctionhouse/auction/types', data={'blah': 'yarp'})
        assert r.status_code == 405
