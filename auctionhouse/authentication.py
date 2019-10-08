# auctionhouse/authentication.py
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from django.contrib.auth.models import User
import base64
import ast

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

            # now we know we're valid we can get the public_id from the token
            # and store it in the django User for use everywhere 
            token_parts = token.split(".")
            decoded_second_part = base64.b64decode(token_parts[1]).decode("utf-8")  
            py_dic = ast.literal_eval(decoded_second_part) 

            user = User(username = py_dic.get('public_id'))
            return (user, None)

        return None




