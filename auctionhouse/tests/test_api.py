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
from rest_framework.test import APIClient

class TestAPIPaths(TestCase):

    #def test_status_ok_no_auth(self):
    #    c = APIClient()
    #    r = c.get('auctionhouse/status')
    #    assert r.status_code == 200
