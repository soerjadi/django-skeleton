# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""

from rest_framework import generics
from rest_framework.response import Response


class InfoView(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        return Response({'result': 'success'})
