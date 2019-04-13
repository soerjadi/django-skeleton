# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""

import asyncio


def asynchronous(func):
    """
    This is decorator for asynchronous using asyncio
    use example: @see[[apps.mailer.Mailer.send]]

    @asynchronous
    def method_name(parameters):
        return
    """
    def wrapped(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop()

        return loop.run_in_executor(None, func, *args, *kwargs)

    return wrapped
