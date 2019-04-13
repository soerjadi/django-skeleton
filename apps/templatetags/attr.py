# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""

from django import template

register = template.Library()


@register.filter(name='attr')
def attr(field, attribute):
    """
    This tag is for add attribute to django form when that cannot handled on python code.
    Only work when you use django form.
    """
    attrs = {}
    definition = attribute.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            key, val = d.split(':')
            attrs[key] = val

    return field.as_widget(attrs=attrs)

