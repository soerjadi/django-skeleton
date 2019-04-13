# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""

from rest_framework.status import HTTP_200_OK
from rest_framework.renderers import BaseRenderer
from rest_framework.utils import json
from typing import *


class ApiRenderer(BaseRenderer):
    media_type = 'application/json'
    format = 'json'

    def render(
        self, data: Any, accepted_media_type: Optional[str] = ..., renderer_context: Optional[Mapping[str, Any]] = ...
    ):
        response = {
            'code': HTTP_200_OK,
            'status': 'success',
            'description': '',
            'result': None
        }

        if data.get('status'):
            response['status'] = data.get('status')

        if data.get('code'):
            response['code'] = data.get('code')

        if data.get('description'):
            response['description'] = data.get('description')

        if data.get('result'):
            response['result'] = data.get('result')

        return json.dumps(response)
