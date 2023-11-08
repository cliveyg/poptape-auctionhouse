from mock import patch
from auction.models import Auction, AuctionType, AuctionLot
from auction.views import AuctionDetail
import uuid
import json
from datetime import datetime, timedelta
from django.urls import reverse
from auction.serializers import AuctionSerializer, AuctionLotSerializer
from rest_framework.response import Response
from httmock import urlmatch, response, HTTMock
from rest_framework import status


# @all_requests
@urlmatch(netloc='https://poptape.club/authy/checkaccess/10')
def response_content(_, request):
    headers = {'content-type': 'application/json',
               'Set-Cookie': 'foo=bar;'}
    content = {'public_id': 'blah'}
    return response(200, content, headers, None, 5, request)


def mock_access_token():
    return "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZleSIsImV4cCI6MTY5OTQxMzY2M30.ShZndWJU_X2Z8sUgJvOQF2ZXqD2quZloY7QqvFKLEWAoEg7HwT2tJhJk194o6nul_zTfV-p5QU2kZXV_qeGbdQ"


def create_auction_data():

    auction = Auction(auction_id = str(uuid.uuid4()),
                      public_id = str(uuid.uuid4()),
                      lots = [],
                      type = AuctionType.EN,
                      name = 'My first auction',
                      multiple = False,
                      start_time = datetime.utcnow(),
                      end_time = datetime.utcnow() + timedelta(days=10),
                      status = 'created',
                      active = True
                      )
    auction_serializer = AuctionSerializer(auction)
    auc_stuff = auction_serializer.data

    auction_lot = AuctionLot(lot_id = str(uuid.uuid4()),
                             item_id = str(uuid.uuid4()),
                             status = 'created',
                             active = True,
                             start_time = datetime.utcnow(),
                             end_time = datetime.utcnow() + timedelta(days=10),
                             quantity = 1,
                             created = datetime.utcnow(),
                             modified = datetime.utcnow()
                             )
    auction_lot_serializer = AuctionLotSerializer(auction_lot)

    auc_stuff['lots'] = auction_lot_serializer.data

    return auc_stuff


def test_detail_view(client):

    """
    Not sure this is actually all that useful as a test as I had to mock so many things
    """
    auction_data = create_auction_data()
    response_from_get = Response({ 'auction': auction_data }, status=status.HTTP_200_OK)

    with patch.object(AuctionDetail, 'get', return_value=response_from_get):
        with HTTMock(response_content):
            url = reverse('auctiondetail', kwargs={'auction_id': auction_data['auction_id']})
            headers = { 'Content-type': 'application/json', 'X_ACCESS_TOKEN': mock_access_token() }
            resp = client.get(url, headers=headers)
            content = resp.content.decode()
            json_object = json.loads(content)
            assert resp.status_code == 200
            # auction = json_object['auction']
            assert json_object['auction']['auction_id'] == auction_data['auction_id']

