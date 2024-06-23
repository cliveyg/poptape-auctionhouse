# auctionhouse/auction/views.py
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.permissions import AllowAny
from auctionhouse.authentication import AdminOnlyAuthentication
from auctionhouse.validators import validate_uuid_from_model
from rest_framework import status
from rest_framework import renderers
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.core.exceptions import ValidationError

from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from auction.models import Auction, EnglishAuctionLot, BuyNowAuctionLot
from auction.models import AuctionLot, DutchAuctionLot, BidHistory
from auction.models import DeliveryOptions, PaymentOptions
from auction.serializers import AuctionSerializer, EnglishAuctionLotSerializer
from auction.serializers import DutchAuctionLotSerializer, BuyNowAuctionLotSerializer
from auction.serializers import BidHistorySerializer
from auction.serializers import PaymentOptionsSerializer, DeliveryOptionsSerializer

from rest_framework.exceptions import NotFound
from django.db.models import Q

from auction.bidhistory import LotQueueConsumer
from auction.janitor import process_finished_single_auctions


import uuid

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


class AuctionJanitor(APIView):
    authentication_classes = (AdminOnlyAuthentication,)

    def get(self, request):
        logger.info("IN AuctionJanitor_GET")
        logger.info("before process_finished_auctions")
        process_finished_single_auctions()
        logger.info("after process_finished_auctions")

        return Response({ 'woopy': 'doo' }, status=status.HTTP_202_ACCEPTED)

# -----------------------------------------------------------------------------


class AuctionDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, auction_id):
        try:
            return Auction.objects.get(auction_id=auction_id)
        except Exception as e:
            logger.error("BAD JUJU [%s]", e)
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

        auction = self.get_object(str(auction_id))
        auction_serializer = AuctionSerializer(auction)
        auction_lot_serializer = self.get_lots(auction.type, auction.lots)

        auc_stuff = auction_serializer.data
        auc_stuff['lots'] = auction_lot_serializer.data

        return Response({ 'auction': auc_stuff }, status=status.HTTP_200_OK)

    def put(self, request, auction_id, format=None):
        auction = self.get_object(auction_id)
        # don't want to let user change auction id so make sure they can't 
        # overwrite it in the json by overwriting it ourselves
        put_data = JSONParser().parse(request)
        put_data['auction_id'] = auction_id
        serializer = AuctionSerializer(auction, data=put_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
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
        _, serializer_obj = self.get_data_objects(auction.type)
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
        logger.info("IN AuctionListCreate_GET")
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

    def get_payments(self, auction_id):
        try:
            return PaymentOptions.objects.get(auction_id=auction_id)
        except PaymentOptions.DoesNotExist:
            raise NotFound(detail="Nowt 'ere, missing payment options for auction", code=404)        

    def get_delivery_options(self, auction_id):
        try:
            return DeliveryOptions.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            raise NotFound(detail="Nowt 'ere, delivery options are missing", code=404)

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

        logger.info("IN AuctionByItem_GET")
        auction_lot = self.get_object(item_id)
        auction = self.get_auction(auction_lot.lot_id)
        auction_serializer = AuctionSerializer(auction)
        auction_lot_serializer = self.get_lots(auction.type, auction.lots)

        payment_options = self.get_payments(auction.auction_id)
        pay_options_serializer = PaymentOptionsSerializer(payment_options)

        delivery_options = self.get_delivery_options(auction.auction_id)
        deliv_opts_serializer = DeliveryOptionsSerializer(delivery_options)
        
        auc_stuff = auction_serializer.data
        auc_stuff['lots'] = auction_lot_serializer.data
        auc_stuff['payment_options'] = pay_options_serializer.data
        auc_stuff['delivery_options'] = deliv_opts_serializer.data

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
        logger.info("IN AuctionLotDetail_GET")
        lot_id = str(lot_uuid)

        # get rabbitmq messages (if any) and save to db
        consumer = LotQueueConsumer( lot_id = lot_id )        

        if consumer.connected_to_exchange():
            consumer.get_messages()
            consumer.save_messages_to_db()

        # gather and return bid history data
        auction = self.get_auction(lot_id)
        model_obj, serializer_obj = self.get_data_objects(auction.type)
        lot = model_obj.objects.get(lot_id = lot_id)

        bids = None
        try:
            bids = BidHistory.objects.filter(lot=lot).order_by('-unixtime')
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
        json_lot_data['status'] = lot.status

        start_time = end_time = None
        if lot.start_time:
            start_time = lot.start_time.timestamp() * 1000
        if lot.end_time:
            end_time = lot.end_time.timestamp() * 1000
        json_lot_data['start_time'] = start_time
        json_lot_data['end_time'] = end_time

        if auction.type == 'EN' or auction.type == 'BN' :
            json_lot_data['min_increment'] = lot.min_increment
            json_lot_data['start_price'] = lot.start_price or 0
            json_lot_data['reserve_price'] = lot.reserve_price or 0
        elif auction.type == 'DU':
            json_lot_data['min_decrement'] = lot.min_decrement
            json_lot_data['start_price'] = lot.start_price or 0
            json_lot_data['reserve_price'] = lot.reserve_price or 0

        json_lot_data['bids'] = json_bid_data

        return Response(json_lot_data, status=status.HTTP_200_OK)

# -----------------------------------------------------------------------------


class AuctionLotListCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def get_lot_serializer(auction_type):
        return serializer.get(auction_type)

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
class Return404(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        # simply returns a 404
        logger.info("In Return404.get")
        message = {'message': 'Not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

# -----------------------------------------------------------------------------
# class for testing validity of auction data sent to auctioneer microservice.
# the service only needs to know if the auction exists and the lot is from
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

        logger.info("IN AuctionValid_GET")

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
        # TODO: need to change as it's possible that bids may exist
        # and auction still be active but auctioneer service went
        # down.
        # NOTE: Changed this but still not 100% sure if this is right way to go
        start_time = end_time = None
        if lot.start_time:
            start_time = lot.start_time.timestamp() * 1000
        if lot.end_time:
            end_time = lot.end_time.timestamp() * 1000

        auction_data = { 'auction_id': auction.auction_id,
                         'auction_type': auction.type,
                         'lot_id': lot.lot_id,
                         'reserve_price': lot.reserve_price or 0,
                         'end_time': end_time,
                         'start_time': start_time or 0,
                         'public_id' : auction.public_id}

        # need to add minimum increase or decrease (change)
        if auction.type == 'EN' or auction.type == 'BN':
            auction_data['min_change'] = lot.min_increment
        elif auction.type == 'DU':
            auction_data['min_change'] = lot.min_decrement

        try:
            bid_history = BidHistory.objects.filter(lot=lot).latest('created')
        except BidHistory.DoesNotExist:

            auction_data['start_price'] = lot.start_price or 0
            auction_data['username'] = request.user.get_short_name()
            auction_data['bid_history_exists'] = False

            # successfully passed all tests
            return Response(auction_data, status=status.HTTP_200_OK)

        # if we reach here we have bids and a history and bid_history var
        # should contain latest bid data
        auction_data['start_price'] = bid_history.bid_amount
        auction_data['username'] = bid_history.username
        auction_data['bid_history_exists'] = True

        return Response(auction_data, status=status.HTTP_200_OK)
        #return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

# -----------------------------------------------------------------------------


class ComboAuctionCreate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, auction_type, format=None):
        # TODO: refactor for when we accept multiple lot auctions - currently only half done

        if auction_type != 'multi' and auction_type != 'solo':
            return Response({ 'error': "Invalid auction type" }, status=status.HTTP_400_BAD_REQUEST)


        if auction_type == 'multi':
            return self.process_multi(request)
        else:
            return self.process_single(request) 


    def process_multi(self, request):

        return Response({ 'message': 'multi-lot auctions not available yet' }, 
                        status=status.HTTP_100_CONTINUE)

        # we need to do additional checks on some fields that we require when
        # creating an auction. these are allowed to be null in our data models
        # (and errors won't be captured by the serializer) but these fields 
        # are required when creating an auction using this class

        required_fields = ['name', 'type', 'start_time', 'end_time', 'currency', 'quantity']

        missing = set(required_fields) - request.data.keys()
        if missing:
            return Response({ 'missing_fields': missing }, status=status.HTTP_400_BAD_REQUEST)

        # for multi auctions we need to remove the start and end times for auction lots
        start_time = end_time = None
        start_time = request.data['start_time']
        end_time = request.data['end_time']
        del request.data['start_time']
        del request.data['end_time']

        # add uuids to create request here 
        request.data['auction_id'] = str(uuid.uuid4())
        # public_id is stored in django User.username
        request.data['public_id'] = request.user.get_username()

        auctype = request.data['type'].upper()
        serializer_obj = None
        if auctype in serializer:
            _, serializer_obj = self.get_data_objects(auctype)
        else:
            return Response({ 'error': 'Unrecognized auction type' }, status=status.HTTP_400_BAD_REQUEST)

        # need to deal with multiple lots here
        lot_serializer = serializer_obj(data=request.data)

        # TODO: multi lots
        if not lot_serializer.is_valid():
            return Response(lot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # add back in data for auction
        request.data['start_time'] = start_time
        request.data['end_time'] = end_time
        request.data['multiple'] = True
        request.data['name'] = name

        # TODO: multi lots
        request.data['lots'] = [request.data['lot_id']]

        # TODO : set active flag to true if start time is now or in past

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

            # we know we have successfully saved both lots and auction at this 
            # point so we can create the delivery and payment records

            return Response({ 'auction_id': request.data['auction_id'],
                              'lot_id': request.data['lot_id'] },
                            status=status.HTTP_201_CREATED)

        return Response(auction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def process_single(self, request):
        
        # we need to do additional checks on some fields that we require when 
        # creating an auction. these are allowed to be null in our data models
        # (and errors won't be captured by the serializer) but these fields 
        # are required when creating an auction using this class

        required_fields = ['type', 'start_time', 'end_time', 'currency', 'quantity']

        missing = set(required_fields) - request.data.keys()
        if missing:
            return Response({ 'missing_fields': missing }, status=status.HTTP_400_BAD_REQUEST)

        # check if at least one payment type is included
        # TODO: put this list in either .env or a table
        payment_methods = { 'pay_visa', 'pay_mastercard', 'pay_amex', 'pay_bank_transfer', 
                            'pay_venmo', 'pay_paypal', 'pay_cash', 'pay_cheque', 'pay_bitcoin' }

        input_set = set(request.data.keys()) 
        chosen_payment_options = payment_methods.intersection(input_set)

        if len(chosen_payment_options) == 0: 
            return Response({ 'message': 'missing payment types' }, status=status.HTTP_400_BAD_REQUEST)

        delivery_methods = {'postage', 'delivery', 'collection'}
        chosen_delivery_options = delivery_methods.intersection(input_set)

        if len(chosen_delivery_options) == 0:
            return Response({ 'message': 'missing delivery options' }, status=status.HTTP_400_BAD_REQUEST)

        if 'name' in request.data.keys():
            del request.data['name']

        # add uuids to create request here 
        request.data['auction_id'] = str(uuid.uuid4())
        request.data['lot_id'] = str(uuid.uuid4())
        # public_id is stored in django User.username
        request.data['public_id'] = request.user.get_username()
        request.data['multiple'] = False

        auctype = request.data['type'].upper()
        serializer_obj = None
        if auctype in serializer:
            _, serializer_obj = self.get_data_objects(auctype)
        else:
            return Response({ 'error': 'Unrecognized auction type' }, status=status.HTTP_400_BAD_REQUEST)
    
        lot_serializer = serializer_obj(data=request.data) 

        if not lot_serializer.is_valid():
            return Response(lot_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # just add a single id to lots array
        request.data['lots'] = [request.data['lot_id']]

        # TODO : set active flag to true if start time is now or in past
          
        delivery_options = DeliveryOptions(auction_id = request.data['auction_id'],
                                           collection = 'collection' in request.data,
                                           delivery = 'delivery' in request.data,
                                           postage = 'postage' in request.data)

        payment_options = PaymentOptions(auction_id = request.data['auction_id'],
                                         visa = 'pay_visa' in request.data,
                                         mastercard = 'pay_mastercard' in request.data,
                                         bank_transfer = 'pay_bank_transfer' in request.data,
                                         bitcoin = 'pay_bitcoin' in request.data,
                                         amex = 'pay_amex' in request.data,
                                         cash = 'pay_cash' in request.data,
                                         cheque = 'pay_cheque' in request.data,
                                         venmo = 'pay_venmo' in request.data,
                                         paypal = 'pay_paypal' in request.data)

        # we now need to create an auction and add our auction lot to it
        auction_serializer = AuctionSerializer(data=request.data)

        if auction_serializer.is_valid():

            # only save everything together
            try:
                auction_serializer.save()
                lot_serializer.save()
                delivery_options.save()
                payment_options.save()
            except Exception as err:
                logger.error(err)
                return Response({ 'message': 'ooh err, it didn\'t like that, check ya logs'}, 
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            aid = auction_serializer.Meta.model.auction_id

            if self.is_valid_uuid(request.data['lot_id']) is False:
                return Response({ 'message': 'bad input data'},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({ 'auction_id': aid,
                              'lot_id': request.data['lot_id'] }, 
                            status=status.HTTP_201_CREATED)

        return Response(auction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def get_data_objects(self, auctype):
        return model.get(auctype), serializer.get(auctype) 

    def get(self, request, format=None):
        # queryset = Auction.objects.all()
        # serializer = AuctionSerializer(queryset, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        logger.info("IN COMBO_AUCTION_CREATE_GET")
        return Response({ 'meep': True }, status=status.HTTP_201_CREATED)

    def create_message_queues(input_data):

        return True


    def is_valid_uuid(value):
        try:
            uuid.UUID(str(value))
            return True
        except ValueError:
            return False

def custom404(request, exception=None):
    return JsonResponse({'message': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
