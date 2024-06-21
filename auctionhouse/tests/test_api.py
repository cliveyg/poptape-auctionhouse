# auctionhouse/tests/test_api.py
# from django.test import SimpleTestCase
import uuid

from django.test import TestCase
# from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from .test_setup import create_auction
import logging
# from httmock import all_requests, HTTMock, response
# import uuid
from unittest import mock
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def mocked_auth_success(*args, **kwargs):

    user = User(username=str(uuid.uuid4()), first_name="Yarp")
    return user, None

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    logger.info("_+_+_+_+_+__++_+_+_+_+_+_+_+_+_+_+_+_")
    logger.info("URL is [%s]", args[0])

    for x in args:
        logger.info("ARGS ARE: [%s]", str(x))
    for arg in kwargs:
        logger.info("KWARG ARG IS: [%s]", str(arg))
    logger.info("_+_+_+_+_+__++_+_+_+_+_+_+_+_+_+_+_+_")

    return MockResponse({"public_id": "blah"}, 200)
    #if args[0] == 'http://poptape-authy-api-1:8001/authy/checkaccess/10':
    #    return MockResponse({"public_id": "blah"}, 200)
    #elif args[0] == 'http://someotherurl.com/anothertest.json':
    #    return MockResponse({"key2": "value2"}, 200)

    #return MockResponse(None, 404)

# @urlmatch(path=r"(.*)authy/checkaccess/10$")
# @all_requests
# def auth_response_ok(url, request):
#    logger.debug("@@@@@@@@@@@@@@@@@@@@ auth_response_ok @@@@@@@@@@@@@@@@@@@@@@@")
#    headers = {'content-type': 'application/json'}
#    content = {'public_id': str(uuid.uuid4())}
#    logger.debug("URL is [%s]", url)
#    return response(200, content, headers, None, 5, request)


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
        #logger.debug("======================= setUpTestData ============================")
        cls.auction_id = create_auction(cls)
        #logger.debug("Auction id is [%s]", cls.auction_id)
        #logger.debug("==================================================================")

    # def setUp(self):
    #     auction_id = create_auction(self)
    #     logger.debug("Auction id is [%s]", self.auction_id)

    @mock.patch('auctionhouse.authentication', side_effect=mocked_auth_success)
    def test_get_auction_by_id(self, mock_get):
        c = RequestsClient()
        logger.debug("++++++++++++++++ test_get_auction_by_id ++++++++++++++++++")
        # with HTTMock(auth_response_ok):
        header = {'HTTP_X_ACCESS_TOKEN': 'sometoken', 'x-access-token': 'yarp'}
        r = c.get('http://localhost/auctionhouse/auction/'+self.auction_id, headers=header)
        logger.debug("Auction id is [%s]", self.auction_id)
        logger.debug("Status code is [%d]", r.status_code)
        logger.debug("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        assert r.status_code == 200
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
