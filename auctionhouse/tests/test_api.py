## auctionhouse/tests/test_api.py
#from rest_framework import status
#from auctionhouse.tests.test_setup import TestMyModelSetup

#class TestMyModelLogAPIs(TestMyModelSetup):
#    def test_get_all_my_model(self):
#        response = self.client.get('/api/v1/my_model/')
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#from django.test import SimpleTestCase
from django.test import TestCase
#from django.urls import resolve, reverse
#from auctionhouse.views import StatusView
#from rest_framework.test import APIClient
from rest_framework.test import RequestsClient

class TestAPIPaths(TestCase):

    def test_status_ok_no_auth(self):
        c = RequestsClient()
        r = c.get('http://localhost/auctionhouse/status')
        assert r.status_code == 200

    def test_return_404(self):
        c = RequestsClient()
        r = c.get('http://localhost/auctionhouse/some404')
        assert r.status_code == 404

    def test_return_error_for_non_json(self):
        c = RequestsClient()
        header = {'Content-Type': 'application/html'}
        r = c.get('http://localhost/auctionhouse/status', headers=header)
        assert r.status_code == 400