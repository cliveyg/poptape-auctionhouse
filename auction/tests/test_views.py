from mock import patch
from auction.views import AuctionDetail, AuctionByItem
import uuid
import json
from datetime import datetime, timedelta
from django.urls import reverse
from httmock import all_requests, response, HTTMock
from rest_framework import status
from rest_framework.response import Response
from auction.serializers import AuctionSerializer, AuctionLotSerializer
from auction.serializers import EnglishAuctionLotSerializer
from auction.serializers import DutchAuctionLotSerializer, BuyNowAuctionLotSerializer
from auction.models import EnglishAuctionLot, BuyNowAuctionLot, DutchAuctionLot
from auction.models import Auction, AuctionType, AuctionLot

serializer = {
    "EN": EnglishAuctionLotSerializer,
    "BN": BuyNowAuctionLotSerializer,
    "DU": DutchAuctionLotSerializer,
}

model = {
    "EN": EnglishAuctionLot,
    "BN": BuyNowAuctionLot,
    "DU": DutchAuctionLot,
}

NOW = datetime.utcnow()
NOW_PLUS_TEN = NOW + timedelta(days=10)


# @urlmatch(netloc='https://poptape.club/authy/checkaccess/10')
@all_requests
def response_content(_, request):
    headers = {'content-type': 'application/json'}
    content = {'public_id': 'blah'}
    return response(200, content, headers, None, 5, request)


def mock_access_token():
    return "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJwdWJsaWNfaWQiOiJmMzhiYTM" \
           "5YS0zNjgyLTQ4MDMtYTQ5OC02NTlmMGJmMDUzMDQiLCJ1c2VybmFtZSI6ImNsaXZ" \
           "leSIsImV4cCI6MTY5OTQxMzY2M30.ShZndWJU_X2Z8sUgJvOQF2ZXqD2quZloY7Q" \
           "qvFKLEWAoEg7HwT2tJhJk194o6nul_zTfV-p5QU2kZXV_qeGbdQ"


def create_auction_data():

    auction = Auction(auction_id = str(uuid.uuid4()),
                      public_id = str(uuid.uuid4()),
                      lots = [],
                      type = AuctionType.EN,
                      name = 'My first auction',
                      multiple = False,
                      start_time = NOW,
                      end_time = NOW_PLUS_TEN,
                      status = 'created',
                      active = True
                      )
    auction_serializer = AuctionSerializer(auction)
    auc_stuff = auction_serializer.data

    auction_lot = AuctionLot(lot_id = str(uuid.uuid4()),
                             item_id = str(uuid.uuid4()),
                             status = 'created',
                             active = True,
                             start_time = NOW,
                             end_time = NOW_PLUS_TEN,
                             quantity = 1,
                             created = NOW,
                             modified = NOW
                             )
    auction_lot_serializer = AuctionLotSerializer(auction_lot)

    auc_stuff['lots'] = auction_lot_serializer.data

    return auc_stuff


def return_a_test_model(auc_type, lot_id):

    model_obj = model.get(auc_type)
    model_obj.lot_id = lot_id
    model_obj.item_id = str(uuid.uuid4())
    model_obj.status = "created"
    model_obj.active = True
    model_obj.start_time = NOW
    model_obj.end_time = NOW_PLUS_TEN
    model_obj.quantity = 1
    model_obj.created = NOW
    model_obj.modified = NOW
    model_obj.start_price = 99.50
    model_obj.reserve_price = 145.80
    model_obj.min_increment = 0.50

    return model_obj


def create_auction_obj(auction_type):

    lot_id = uuid.uuid4()
    auction = Auction(auction_id = str(uuid.uuid4()),
                      public_id = str(uuid.uuid4()),
                      lots = [str(lot_id)],
                      type = auction_type,
                      name = 'My first auction',
                      multiple = False,
                      start_time = NOW,
                      end_time = NOW_PLUS_TEN,
                      status = 'created',
                      active = True
                      )
    return auction


def test_detail_view(client):

    auction_obj = create_auction_obj(AuctionType.EN)

    serializer_obj = serializer.get(auction_obj.type)
    model_obj = return_a_test_model(auction_obj.type, auction_obj.lots[0])
    auction_lots = [model_obj]

    """ Need to mock both these methods to avoid db calls"""
    with patch.object(AuctionDetail, 'get_object', return_value=auction_obj):
        with patch.object(AuctionDetail, 'get_lots', return_value=serializer_obj(auction_lots, many=True)):
            with HTTMock(response_content):
                url = reverse('auctiondetail', kwargs={'auction_id': auction_obj.auction_id})
                headers = {'Content-type': 'application/json', 'X_ACCESS_TOKEN': mock_access_token()}
                resp = client.get(url, headers=headers)
                content = resp.content.decode()
                json_object = json.loads(content)
                assert resp.status_code == 200
                assert json_object['auction']['auction_id'] == auction_obj.auction_id
                assert json_object['auction']['name'] == auction_obj.name
                assert json_object['auction']['type'] == AuctionType.EN


def test_detail_view_not_found(client):

    response_from_get = Response({}, status=status.HTTP_404_NOT_FOUND)

    with patch.object(AuctionDetail, 'get', return_value=response_from_get):
        with HTTMock(response_content):
            url = reverse('auctiondetail', kwargs={'auction_id': str(uuid.uuid4())})
            headers = {'Content-type': 'application/json', 'X_ACCESS_TOKEN': mock_access_token()}
            resp = client.get(url, headers=headers)
            assert resp.status_code == 404

def test_get_auction_by_item_view_not_found(client):

    response_from_get = Response({}, status=status.HTTP_404_NOT_FOUND)

    with patch.object(AuctionByItem, 'get', return_value=response_from_get):
        with HTTMock(response_content):
            url = reverse('auctionbyitem', kwargs={'item_id': str(uuid.uuid4())})
            headers = {'Content-type': 'application/json', 'X_ACCESS_TOKEN': mock_access_token()}
            resp = client.get(url, headers=headers)
            assert resp.status_code == 404