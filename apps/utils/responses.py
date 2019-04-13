# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""

from django.template.response import HttpResponse


class JavascriptResponse:
    """
    This class help you return response on javascript mode. This will really useful
    when you need to return only specific attribute without refresh/ redirect page.
    """

    @staticmethod
    def refresh_page():
        return HttpResponse("window.location.reload();", content_type='text/javascript')

    @staticmethod
    def redirect_to(url):
        return HttpResponse("window.location.href = %s;" % url, content_type='text/javascript')
