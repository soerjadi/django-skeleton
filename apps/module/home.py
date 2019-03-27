# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""

from django.template.response import TemplateResponse
from django.views.generic import TemplateView


class HomePageView(TemplateView):

    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, "index.html")
