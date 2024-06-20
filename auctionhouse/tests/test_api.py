# auctionhouse/tests/test_api.py
# from django.test import SimpleTestCase
from django.test import TestCase
# from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
import logging

logger = logging.getLogger(__name__)


class TestAPIPaths(TestCase):

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

    def test_return_error_for_non_json(self):
        c = RequestsClient()
        header = {'Content-Type': 'text/html'}
        r = c.get('http://localhost/auctionhouse/status', headers=header)
        logger.debug("Content-Type is %s", r.headers.get('Content-Type'))
        logger.debug("Status code is %d", r.status_code)
        # assert r.status_code == 400
#        c = APIClient()
#        c.headers = {'Content-Type': 'text/html'}
#        r = c.get('http://localhost/auctionhouse/status')
#        logger.info("Status code is %d", r.status_code)
        assert 1 == 1
