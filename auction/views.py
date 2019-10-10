# auctionhouse/auction/views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse
from rest_framework.views import APIView
from auction.models import Auction, EnglishAuctionLot, BuyNowAuctionLot
from auction.models import AuctionLot, DutchAuctionLot
from auction.serializers import AuctionSerializer, EnglishAuctionLotSerializer
from auction.serializers import DutchAuctionLotSerializer, BuyNowAuctionLotSerializer
from rest_framework.exceptions import NotFound
from django.db.models import Q

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
        return serializer.get(auction.type)

    def get_lots(self, auctype, lots):

        auction_lots = None
        auction_lot_serializer = None
        # build query from array of Q objects
        queries = [Q(lot_id=lot) for lot in lots]
        query = queries.pop()
        for item in queries:
            query |= item

        if auctype == 'EN':
            auction_lots = EnglishAuctionLot.objects.filter(query)
            auction_lot_serializer = EnglishAuctionLotSerializer(auction_lots, many=True)
        elif auctype == 'BN':
            auction_lots = BuyNowAuctionLot.objects.filter(query)
            auction_lot_serializer = BuyNowAuctionLotSerializer(auction_lots, many=True)
        elif auctype == 'DU':
            auction_lots = DutchAuctionLot.objects.filter(query)
            auction_lot_serializer = DutchAuctionLotSerializer(auction_lots, many=True)

        return auction_lot_serializer

    def get(self, request, auction_id, format=None):
        auction = self.get_object(auction_id)
        auction_serializer = AuctionSerializer(auction)
        auction_lot_serializer = self.get_lots(auction.type, auction.lots)

        auc_stuff = auction_serializer.data
        auc_stuff['lots'] = auction_lot_serializer.data

        return Response({ 'auction': auc_stuff }, status=status.HTTP_200_OK)

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

class AuctionByItem(APIView):

    def get_object(self, item_id):
        try:
            return AuctionLot.objects.get(item_id=item_id)
        except AuctionLot.DoesNotExist:
            raise NotFound(detail="Nowt 'ere, item not in an auction", code=404)

    def get_auction(self, lot_id):
        try:
            # returns only one Auction object
            return Auction.objects.filter(lots__contains=[lot_id])[:1].get()
        except Auction.DoesNotExist:
            raise NotFound(detail="Nowt 'ere, auction lot not in auction", code=404)

    def get_lots(self, auctype, lots):
  
        auction_lots = None
        auction_lot_serializer = None 
        # build query from array of Q objects
        queries = [Q(lot_id=lot) for lot in lots]
        query = queries.pop()
        for item in queries:
            query |= item

        if auctype == 'EN':
            auction_lots = EnglishAuctionLot.objects.filter(query)
            auction_lot_serializer = EnglishAuctionLotSerializer(auction_lots, many=True)
        elif auctype == 'BN':
            auction_lots = BuyNowAuctionLot.objects.filter(query)
            auction_lot_serializer = BuyNowAuctionLotSerializer(auction_lots, many=True)
        elif auctype == 'DU':
            auction_lots = DutchAuctionLot.objects.filter(query)
            auction_lot_serializer = DutchAuctionLotSerializer(auction_lots, many=True)

        return auction_lot_serializer

    def get(self, request, item_id, format=None):
        auction_lot = self.get_object(item_id)
        auction = self.get_auction(auction_lot.lot_id)
        auction_serializer = AuctionSerializer(auction)
        auction_lot_serializer = self.get_lots(auction.type, auction.lots)
        
        auc_stuff = auction_serializer.data
        auc_stuff['lots'] = auction_lot_serializer.data

        return Response({ 'auction': auc_stuff }, status=status.HTTP_200_OK)

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

# -----------------------------------------------------------------------------

class AuctionTypes(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        # simply returns a 200 ok with a message 

        message = { 'valid_types': [ {'key': 'EN', 'label': 'English'},
                                     {'key': 'BN', 'label': 'Buy Now'},
                                     {'key': 'DU', 'label': 'Dutch'}] }

        return Response(message, status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------
# class for testing validity of auction data sent to auctioneer microservice
# the service only needs to know if the auction exists and the lot is from 
# that particular auction and that auction owner is not bidding on their own  
# auction. returns either 200 or 406

class AuctionValid(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, auction_id, lot_id, format=None):

        lot = auction = None

        try:
            auction = Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)

        # public id of requester is stored in the django User object
        if auction.public_id == request.user.get_username():
            # can't bid on your own auction so return a 406
            return Response(status=HTTP_406_NOT_ACCEPTABLE)

        lot_found = False
        for lot in auction.lots:
            if lot.lot_id == lot_id:
                lot_found = True
                break

        if not lot_found:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
        
        # successfully passed all tests
        return Response(status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------

class ComboAuctionCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, auction_type, format=None):

        if auction_type != 'multi' and auction_type != 'solo':
            return Response({ 'error': "Invalid auction type" }, status=status.HTTP_400_BAD_REQUEST)

        # we need to do additional checks on some fields that we require when 
        # creating an auction. these are allowed to be null in our data models
        # (and errors won't be captured by the serializer) but these fields 
        # are required when creating an auction using this class
        required_fields = ['type', 'start_time', 'end_time', 'currency', 'quantity']

        # for multi auctions we need to add a required field
        if auction_type == 'multi':
            required_fields.extend(['name'])

        missing = set(required_fields) - request.data.keys()
        if missing:
            return Response({ 'missing_fields': missing }, status=status.HTTP_400_BAD_REQUEST)

        # for multi auctions we need to remove the start and end times for auction lots
        start_time = end_time = name = None
        if auction_type == 'multi':        
            start_time = request.data['start_time']
            end_time = request.data['end_time']
            del request.data['start_time']
            del request.data['end_time']

        if 'name' in request.data.keys():
            name = request.data['name']
            del request.data['name']

        # add uuids to create request here 
        request.data['auction_id'] = str(uuid.uuid4())
        request.data['lot_id'] = str(uuid.uuid4())
        # public_id is stored in django User.username
        request.data['public_id'] = request.user.get_username()

        if request.data['type'] == "EN":
            lot_serializer = EnglishAuctionLotSerializer(data=request.data) 
        elif request.data['type'] == "BN":
            lot_serializer = BuyNowAuctionLotSerializer(data=request.data)
        elif request.data['type'] == "DU":
            lot_serializer = DutchAuctionLotSerializer(data=request.data)
        else:
            return Response({ 'error': 'Unrecognized auction type' }, status=status.HTTP_400_BAD_REQUEST)
        
        if not lot_serializer.is_valid():
            return Response(lot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        request.data['lots'] = [request.data['lot_id']]
        if auction_type == 'multi': 
            request.data['start_time'] = start_time
            request.data['end_time'] = end_time
            request.data['multiple'] = True
            request.data['name'] = name

        #TODO : set active flag to true if start time is now or in past

        # we now need to create an auction and add our auction lot to it
        auction_serializer = AuctionSerializer(data=request.data)
        if auction_serializer.is_valid():
            # only save when both are valid
            lot_serializer.save()
            auction_serializer.save()
            return Response({ 'auction_id': request.data['auction_id'] }, status=status.HTTP_201_CREATED)

        return Response(auction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request, format=None):

        #queryset = Auction.objects.all()
        #serializer = AuctionSerializer(queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({ 'meep': True }, status=status.HTTP_201_CREATED)
