# auctionhouse/auctionhouse/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse
from rest_framework.views import APIView
from django.conf import settings

# get an instance of a logger
import logging
logger = logging.getLogger('auctionhouse')

# -----------------------------------------------------------------------------
# view to show status of auctionhouse microservice - no authentication needed
# -----------------------------------------------------------------------------


class StatusView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        # simply returns a 200 ok with a message 
        logger.info("auctionhouse/views/StatusView.get")
        message = { 'message': 'System running...', 'version': 0.5 }

        return Response(message, status=status.HTTP_200_OK)

