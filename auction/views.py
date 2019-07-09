# auctionhouse/auction/views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from auction.models import Auction, EnglishAuctionLot, BuyNowAuctionLot
from auction.serializers import AuctionSerializer, EnglishAuctionLotSerializer
from auction.serializers import BuyNowAuctionLotSerializer
from rest_framework.exceptions import NotFound

import uuid

# get an instance of a logger
import logging
logger = logging.getLogger('auctionhouse')

serializer = {
    "EN": EnglishAuctionLotSerializer,
    "BN": BuyNowAuctionLotSerializer
}

# -----------------------------------------------------------------------------
# views
# -----------------------------------------------------------------------------

class AuctionDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, auction_id):
        try:
            return Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            raise NotFound(detail="Nowt 'ere, resource not found", code=404)

    def get_serializer_object(self, auction):
        logger.info("Auc type is [%s]",auction.type)
        return serializer.get(auction.type)

    def get(self, request, auction_id, format=None):
        auction = self.get_object(auction_id)
        serializer = AuctionSerializer(auction)
        return Response(serializer.data)

    def put(self, request, auction_id, format=None):
        auction = self.get_object(auction_id)
        # don't want to let user change auction id so make sure they can't 
        # overwrite it in the json by overwriting it ourselves
        request.data['auction_id'] = auction_id
        serializer = AuctionSerializer(auction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, auction_id, format=None):
        auction = self.get_object(auction_id)
        auction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # posting to this url actually creates a child resource
    def post(self, request, auction_id, format=None):
        # add a uuid to create request here
        request.data['lot_id'] = str(uuid.uuid4())
        auction = self.get_object(auction_id)
        serializer_obj = self.get_serializer_object(auction)
        serializer = serializer_obj(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------

class AuctionListCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # add a uuid to create request here 
        request.data['auction_id'] = str(uuid.uuid4())
        serializer = AuctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):

        queryset = Auction.objects.all()
        serializer = AuctionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------

class AuctionLotDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, lot_id):
        try:
            return Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            raise NotFound(detail="Nowt 'ere, resource not found", code=404)

    def get(self, request, auction_id, format=None):
        auction = self.get_object(auction_id)
        serializer = AuctionSerializer(auction)
        return Response(serializer.data)

    def put(self, request, auction_id, format=None):
        auction = self.get_object(auction_id)
        # don't want to let user change auction id so make sure they can't
        # overwrite it in the json by overwriting it ourselves
        request.data['auction_id'] = auction_id
        serializer = AuctionSerializer(auction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, auction_id, format=None):
        auction = self.get_object(auction_id)
        auction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------

class AuctionLotListCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def get_lot_serializer(auction_type):
        return serializer.get(auction_lot.type)

    def get_auction(auction_id):
        try:
            return Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            raise NotFound(detail="Nowt 'ere, resource not found", code=404)


