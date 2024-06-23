# auctionhouse/authentication.py
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.contrib.auth.models import User
import base64
import ast
from requests import Request
import requests

# get an instance of a logger
import logging
logger = logging.getLogger('auctionhouse')


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return True

# -----------------------------------------------------------------------------


class AdminOnlyAuthentication(BaseAuthentication):

    def authenticate(self, request, token=None):

        # logger.critical("Why you here Diane?")

        if not request.META.get('HTTP_X_ACCESS_TOKEN'):
            # logger.critical("Returning nowt")
            return None

        # call authy with admin url
        authy_url = settings.AUTH_SERVER_ADMIN_URL

        headers = {'Content-type': 'application/json',
                   'x-access-token': request.META.get('HTTP_X_ACCESS_TOKEN')}

        resp = Request
        try:
            resp = requests.get(authy_url, headers=headers)
        except Exception as e:
            logger.error("Error calling auth server: [%s]", e)

        if resp.status_code == 200:

            token_parts = request.META.get('HTTP_X_ACCESS_TOKEN').split(".")
            # decoded_second_part = base64.b64decode(token_parts[1]+"===").decode("utf-8")
            try:
                decoded_second_part = base64.urlsafe_b64decode(token_parts[1]+"===").decode("UTF-8")
                py_dic = ast.literal_eval(decoded_second_part)
            except Exception as err:
                logger.error(err)
                raise AuthenticationFailed

            user = User(username=py_dic.get('public_id'), first_name=py_dic.get('username'))
            return user, None

        else:
            raise AuthenticationFailed

# -----------------------------------------------------------------------------    


class TokenAuth(BaseAuthentication):

    def authenticate(self, request, token=None):

        # logger.critical("Why you here Willis?")

        if not request.META.get('HTTP_X_ACCESS_TOKEN'):
            return None

        # call authy
        authy_url = settings.AUTH_SERVER_URL

        headers = {'Content-type': 'application/json',
                   'x-access-token': request.META.get('HTTP_X_ACCESS_TOKEN')}
        resp = Request
        try:
            resp = requests.get(authy_url, headers=headers)
        except Exception as e:
            logger.error("Error calling auth server: [%s]", e)

        if resp.status_code == 200:

            token_parts = request.META.get('HTTP_X_ACCESS_TOKEN').split(".")
            # decoded_second_part = base64.b64decode(token_parts[1]+"===").decode("utf-8")
            try:
                decoded_second_part = base64.urlsafe_b64decode(token_parts[1]+"===").decode("UTF-8")
                py_dic = ast.literal_eval(decoded_second_part) 
            except Exception as err:
                logger.error(err)
                raise AuthenticationFailed

            user = User(username=py_dic.get('public_id'), first_name=py_dic.get('username'))
            return user, None

        else:
            raise AuthenticationFailed
