# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""
from typing import Optional, Tuple, Any, Type

from django.db.models import Model
from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.request import Request

from apps.models.access_tokens import AccessToken

AUTHORIZATION_HEADER = 'HTTP_X_ACCESS_TOKEN'


def get_authorization_header(request):
    """
    Return request's 'X-Access-Token:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get(AUTHORIZATION_HEADER, b'')

    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)

    return auth


class XAccessTokenAuthentication(TokenAuthentication):

    def authenticate(self, request: Request) -> Optional[Tuple[Any, Any]]:
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        if len(auth) == 0:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 1:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[0].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def get_model(self) -> Type[Model]:
        if self.model is not None:
            return self.model

        return AccessToken

    def authenticate_credentials(self, key: str) -> Tuple[Any, Any]:
        model = self.get_model()
        try:
            token = model.objects.get(token=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.is_valid:
            raise exceptions.AuthenticationFailed(_('Access token expired'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token
