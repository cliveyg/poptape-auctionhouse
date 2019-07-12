# auctionhouse/authentication.py
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from django.contrib.auth.models import User

# get an instance of a logger
import logging
logger = logging.getLogger('auctionhouse')

import requests

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return True
    

class TokenAuth(BaseAuthentication):

    def authenticate(self, request):

        token = request.META.get('HTTP_X_ACCESS_TOKEN')
        if not token:
            return None

        # call authy
        authy_url = settings.AUTH_SERVER_URL

        headers = { 'Content-type': 'application/json',
                    'x-access-token': request.META.get('HTTP_X_ACCESS_TOKEN') }
        resp = requests.get(authy_url ,headers=headers)

        if resp.status_code == 200:
            user = User()
            return (user, None)

        return None




