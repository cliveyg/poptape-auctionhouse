# auctionhouse/tests/test_api.py
# from django.test import SimpleTestCase
from django.test import TestCase
# from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from .test_setup import create_test, create_auction
import logging

logger = logging.getLogger(__name__)


# helper function to compare json objects
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


class TestAPIPaths(TestCase):

    auction_id = ""
    @classmethod
    def setUpTestData(cls):
        test_id = create_test(cls)
        logger.debug("Test id is [%s]", test_id)
        #auction_id = create_auction(cls)
        #logger.debug("Auction id is [%s]", auction_id)

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
