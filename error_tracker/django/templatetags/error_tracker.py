# -*- coding: utf-8 -*-
#
#    Django error tracker template tags and filters
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

from django import template

register = template.Library()


@register.filter
def replace_new_line_with_br(value):
    return value.replace("\n", "<br/>")
