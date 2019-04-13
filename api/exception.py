# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""

from rest_framework.views import set_rollback
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions as core_exceptions

import logging
import sys


class InternalServerErrorException(Exception):
    pass


class InvalidException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class NotFoundException(Exception):
    pass


class ValidationException(Exception):
    pass


class NotAuthenticated(exceptions.APIException):
    status_code = HTTP_401_UNAUTHORIZED
    default_detail = _('Unauthorized')
    default_code = 'not_authenticated'


def exception_handler(exc, context):
    """
        Returns the response that should be used for any given exception.

        By default we handle the REST framework `APIException`, and also
        Django's built-in `Http404` and `PermissionDenied` exceptions.

        Any unhandled exceptions may return `None`, which will cause a 500 error
        to be raised.
        """
    if isinstance(exc, NotFoundException):
        exc = exceptions.NotFound()
    elif isinstance(exc, UnauthorizedException):
        exc = exceptions.PermissionDenied()
    elif isinstance(exc, exceptions.NotAuthenticated):
        exc = NotAuthenticated()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None


def api_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data['code'] = response.status_code
        response.data['description'] = response.data['detail']
        response.data['status'] = 'error'
        del response.data['detail']

    return response


def handler(f):
    logger = logging.getLogger('apps')

    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except InternalServerErrorException as e:
            traceback = sys.exc_info()[2]
            logger.error(e.with_traceback(traceback))
            return Response({"code": HTTP_500_INTERNAL_SERVER_ERROR, "status": "error", "description": str(e)})

        except InvalidException as e:
            traceback = sys.exc_info()[2]
            logger.error(e.with_traceback(traceback))
            return Response({"code": HTTP_400_BAD_REQUEST, "status": "error", "description": str(e)})

        except exceptions.NotAuthenticated:
            return Response({"code": HTTP_401_UNAUTHORIZED, "status": "error", "description": "unauthorized"})

        except exceptions.PermissionDenied:
            return Response({"code": HTTP_401_UNAUTHORIZED, "status": "error", "description": "unauthorized"})

        except UnauthorizedException:
            return Response({"code": HTTP_401_UNAUTHORIZED, "status": "error", "description": "unauthorized"})

        except NotFoundException as e:
            traceback = sys.exc_info()[2]
            logger.error(e.with_traceback(traceback))
            return Response({"code": HTTP_404_NOT_FOUND, "status": "error", "description": str(e)})

        except ValidationException as e:
            traceback = sys.exc_info()[2]
            logger.error(e.with_traceback(traceback))
            return Response({"code": HTTP_400_BAD_REQUEST, "status": "error", "description": str(e)})

        except core_exceptions.ObjectDoesNotExist:
            return Response({"code": HTTP_404_NOT_FOUND, "status": "error", "description": "not found"})

        except exceptions.ValidationError as e:
            traceback = sys.exc_info()[2]
            logger.error(e.with_traceback(traceback))
            _error = next(iter(e.detail.values()))[0]
            return Response({"code": HTTP_400_BAD_REQUEST, "status": "error", "description": _error})

        except Exception as e:
            traceback = sys.exc_info()[2]
            logger.error(e.with_traceback(traceback))
            return Response({"code": HTTP_400_BAD_REQUEST, "status": "error", "description": str(e)})

    return wrapped
