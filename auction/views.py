# auctionhouse/auction/views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse
from rest_framework.views import APIView
from auction.models import Auction, EnglishAuctionLot, BuyNowAuctionLot
from auction.models import AuctionLot, DutchAuctionLot, BidHistory
from auction.serializers import AuctionSerializer, EnglishAuctionLotSerializer
from auction.serializers import DutchAuctionLotSerializer, BuyNowAuctionLotSerializer
from auction.serializers import BidHistorySerializer
from rest_framework.exceptions import NotFound
from django.db.models import Q

from auction.bidhistory import LotQueueConsumer

import uuid
import requests
from datetime import datetime

# get an instance of a logger
import logging
logger = logging.getLogger('auctionhouse')

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

    def get_data_objects(self, auctype):
        return model.get(auctype), serializer.get(auctype)

    def get_lots(self, auctype, lots):

        # build query from array of Q objects
        queries = [Q(lot_id=lot) for lot in lots]
        query = queries.pop()
        for item in queries:
            query |= item

        model_obj, serializer_obj = self.get_data_objects(auctype)

        auction_lots = model_obj.objects.filter(query)
        return serializer_obj(auction_lots, many=True)

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
        _, serializer_obj = self.get_data_objects(auctype)
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
    permission_classes = (IsAuthenticatedOrReadOnly,)

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

    def get_data_objects(self, auctype):
        return model.get(auctype), serializer.get(auctype)

    def get_lots(self, auctype, lots):
  
        auction_lots = None
        auction_lot_serializer = None 
        # build query from array of Q objects
        queries = [Q(lot_id=lot) for lot in lots]
        query = queries.pop()
        for item in queries:
            query |= item

        model_obj, serializer_obj = self.get_data_objects(auctype)

        auction_lots = model_obj.objects.filter(query)
        return serializer_obj(auction_lots, many=True)

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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_auction(self, lot_id):
        try:
            # returns only one Auction object
            return Auction.objects.filter(lots__contains=[lot_id])[:1].get()
        except Auction.DoesNotExist:
            raise NotFound(detail="Nowt 'ere, auction lot not in auction", code=404)

    def get_data_objects(self, auctype):
        return model.get(auctype), serializer.get(auctype)

    def get(self, request, lot_uuid):
        lot_id = str(lot_uuid)

        # get rabbitmq messages (if any) and save to db
        consumer = LotQueueConsumer( lot_id = lot_id )        

        if consumer.connected_to_exchange():
            consumer.get_messages()
            saved, errored = consumer.save_messages_to_db()

        # gather and return bid history data
        auction = self.get_auction(lot_id)
        model_obj, serializer_obj = self.get_data_objects(auction.type)
        lot = model_obj.objects.get(lot_id = lot_id)

        bids = None
        try:
            bids = BidHistory.objects.filter(lot=lot)
        except Exception as e:
            logger.error("Bid history fail! [%s]",e)

        json_bid_data = []
        for bid in bids:
            bid_serializer = BidHistorySerializer(bid)
            json_bid_data.append(bid_serializer.data)

        # not using the serializer as we only want a subset of the lot data
        #TODO?: create more serializers for subsets of data??
        json_lot_data = {}
        json_lot_data['lot_id'] = lot_id
        json_lot_data['auction_id'] = auction.auction_id
        json_lot_data['public_id'] = auction.public_id
        json_lot_data['auction_type'] = auction.type
        json_lot_data['start_time'] = lot.start_time
        json_lot_data['end_time'] = lot.end_time
        json_lot_data['status'] = lot.status

        if auction.type == 'EN' or auction.type == 'BN' :
            json_lot_data['min_change'] = lot.min_increment
            json_lot_data['start_price'] = lot.start_price
        elif auction.type == 'DU':
            json_lot_data['min_change'] = lot.min_decrement
            json_lot_data['start_price'] = lot.start_price
        
        json_lot_data['bids'] = json_bid_data

        return Response(json_lot_data, status=status.HTTP_200_OK)

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
    permission_classes = (AllowAny,)
    #permission_classes = (IsAuthenticated,)
    

    def get(self, request, *args, **kwargs):
        # simply returns a 200 ok with a message 

        message = { 'valid_types': [ {'key': 'EN', 'label': 'English'},
                                     {'key': 'BN', 'label': 'Buy Now'},
                                     {'key': 'DU', 'label': 'Dutch'}] }

        return Response(message, status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------
# class for testing validity of auction data sent to auctioneer microservice
# the service only needs to know if the auction exists and the lot is from 
# that particular auction and that the user trying to use the auction service
# is the valid user to do this
# we also check if there is any bid history because if there is then the user
# is attempting to create this auction instance twice (i.e. deleted and trying
# to recreate) which we do not allow.
# returns either 200 or 406 along with a subset of auction/lot data
# TODO: decide which data to return

class AuctionValid(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, auction_id, lot_id, format=None):

        lot = auction = None

        try:
            auction = Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        # auction has already started so can't create again
        # TODO: not sure about this
        #if auction.active:
        #    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        # public id of requester is stored in the django User object
        if auction.public_id != request.user.get_username():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        lot_found = False
        for lotty in auction.lots:
            if lotty == str(lot_id):
                model_obj =  model.get(auction.type)
                try:
                    lot = model_obj.objects.get(lot_id=lot_id)
                except model_obj.DoesNotExist:
                    lot_found = False
                    break
                lot_found = True
                break

        if not lot_found:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        # look for bid history
        #TODO: need to change as it's possible that bids may exist
        # and auction still be active but auctioneer service went
        # down.
        try:
            BidHistory.objects.filter(lot=lot)[:1].get()
        except BidHistory.DoesNotExist:
            start_time = end_time = None
            if lot.start_time:
                start_time = lot.start_time.timestamp() * 1000
            if lot.end_time:
                end_time = lot.end_time.timestamp() * 1000

            auction_data = { 'auction_id': auction.auction_id,
                             'auction_type': auction.type,
                             'lot_id': lot.lot_id,
                             'start_price': lot.start_price or 0,
                             'reserve_price': lot.reserve_price or 0,
                             'end_time': end_time,
                             'start_time': start_time or 0,
                             'username': request.user.get_short_name(),
                             'public_id' : auction.public_id }
            # need to add minimum increase or decrease (change)
            if auction.type == 'EN' or auction.type == 'BN':
                auction_data['min_change'] = lot.min_increment
            elif auction.type == 'DU':
                auction_data['min_change'] = lot.min_decrement

            # successfully passed all tests
            return Response(auction_data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

# -----------------------------------------------------------------------------

class ComboAuctionCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, auction_type, format=None):
        #TODO: refactor for when we accept multiple lot auctions - currently only half done 

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

        auctype = request.data['type'].upper()
        serializer_obj = None
        if auctype in serializer:
            _, serializer_obj = self.get_data_objects(auctype)
        else:
            return Response({ 'error': 'Unrecognized auction type' }, status=status.HTTP_400_BAD_REQUEST)
    
        lot_serializer = serializer_obj(data=request.data) 
       
        #TODO: multi lots 
        if not lot_serializer.is_valid():
            return Response(lot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #request.data['lots'] = [request.data['lot_id']]

        if auction_type == 'multi': 
            request.data['start_time'] = start_time
            request.data['end_time'] = end_time
            request.data['multiple'] = True
            request.data['name'] = name
            
        else: 
            # just add a single id to lots array
            request.data['lots'] = [request.data['lot_id']]

        #TODO : set active flag to true if start time is now or in past

        # we now need to create an auction and add our auction lot to it
        auction_serializer = AuctionSerializer(data=request.data)
        if auction_serializer.is_valid():
            # only save when both are valid
            try:
                auction_serializer.save()
                lot_serializer.save()
            except Exception as err:
                logger.error(err)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({ 'auction_id': request.data['auction_id'],
                              'lot_id': request.data['lot_id'] }, 
                            status=status.HTTP_201_CREATED)

        return Response(auction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def get_data_objects(self, auctype):
        return model.get(auctype), serializer.get(auctype) 

    def get(self, request, format=None):
        #queryset = Auction.objects.all()
        #serializer = AuctionSerializer(queryset, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({ 'meep': True }, status=status.HTTP_201_CREATED)

    def create_message_queues(input_data):

        return True
