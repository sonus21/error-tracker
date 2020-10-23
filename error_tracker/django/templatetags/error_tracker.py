# -*- coding: utf-8 -*-
#
#    Django error tracker template tags and filters
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

from django import template
import json
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def replace_new_line_with_br(value):
    return value.replace("\n", "<br/>")


@register.filter("to_pretty")
def to_pretty(x):
    html = x
    try:
        x = json.loads(x)
    except Exception as e:
        try:
            x = x.replace("'", '"').replace("\\\\", "\\")
            x = json.loads(x)
        except Exception as e:
            pass
        pass
    
    try:
        html = "<pre>{}</pre>".format(
            json.dumps(x, indent=4, sort_keys=True))
    except Exception as e:
        pass

    return mark_safe(html)
