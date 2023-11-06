from django.test import SimpleTestCase
from django.urls import resolve, reverse
from auctionhouse.views import StatusView


class TestURLS(SimpleTestCase):

    def test_api_status_route_is_resolved(self):
        url = reverse('status')
        self.assertEquals(resolve(url).url_name, 'status')
        self.assertEquals(resolve(url).route, 'auctionhouse/status/')
        self.assertEquals(resolve(url).func.__name__, StatusView.as_view().__name__)
        self.assertEquals(resolve(url).func.view_class,StatusView)
