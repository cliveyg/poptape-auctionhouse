# auctionhouse/tests/test_api.py
import uuid

from django.test import TransactionTestCase
from rest_framework.test import RequestsClient
from .test_setup import create_auction_and_lots
import logging
from requests.models import Response
from unittest.mock import Mock
from unittest import mock

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

    auction_id = ""

    @classmethod
    def setUpTestData(self):
        self.auction_id = create_auction_and_lots(self)


#    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
#    def test_fail_get_auction_by_id_not_valid_uuid(self, mock_get):
#        c = RequestsClient()
#        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
#        r = c.get('http://localhost/auctionhouse/auction/notvaliduuid', headers=header)
#        assert r.status_code == 404
#        assert r.headers.get('Content-Type') == 'application/json'


    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_get_auction_by_id(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r = c.get('http://localhost/auctionhouse/auction/'+self.auction_id, headers=header)
        returned_data = r.json()
        logger.info("XOX Returned data is [%s]", returned_data)
        assert r.url == "http://localhost/auctionhouse/auction/"+self.auction_id
        assert r.status_code == 200
        assert r.headers.get('Content-Type') == 'application/json'

'''
    def test_fail_get_auction_no_auth(self):
        c = RequestsClient()
        r = c.get('http://localhost/auctionhouse/auction/'+self.auction_id)
        assert r.status_code == 403
        assert r.headers.get('Content-Type') == 'application/json'

    @mock.patch('auctionhouse.authentication.requests.get', side_effect=mocked_auth_success)
    def test_fail_get_auction_by_id_404(self, mock_get):
        c = RequestsClient()
        header = {'x-access-token': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTcxOTAxNDMxNX0.-qkVpCAZvwng-Suf55EPLAd4r-PHgVqqYFywjDtjnrUNL8hsdYyFMgFFPdE1wOhYYjI9izftfyY43pUayEQ57g'}
        r = c.get('http://localhost/auctionhouse/auction/'+str(uuid.uuid4()), headers=header)
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
        logger.debug("Content-Type is %s", r.headers.get('Content-Type'))
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
        logger.debug("Content-Type is %s", r.headers.get('Content-Type'))
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
'''
