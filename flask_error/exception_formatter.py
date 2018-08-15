# -*- coding: utf-8 -*-

import __builtin__
import cStringIO
import itertools
import sys
import traceback

import re
import types
from werkzeug.datastructures import ImmutableMultiDict


def format_frame(x, max_elements, max_string, max_recursion, maskable=None):
    """
    Return a formatted frame for storing in the database.
    :param x: frame key/value pair
    :param max_elements: Maximum number of elements to be formatted
    :param max_string: Maximum length for string data types in output
    :param max_recursion: Maximum recursion depth used in structure like dict
    :param maskable: Used to mask a key/value
    :return: string of formatted value
    """

    def _per_element(i):
        return format_frame(i, max_elements, max_string, max_recursion - 1, maskable=maskable)

    def _per_dict_element(i):
        masked = False
        val = None
        if maskable:
            masked, val = maskable(i[0])
        return "%r : %s" % (i[0], val if masked else _per_element(i[1]))

    def _it_to_string(fmt, it, per_element=_per_element):
        if max_recursion <= 0:
            return fmt % "..."

        it = iter(it)

        s = ', '.join(per_element(i) for i in itertools.islice(it, max_elements))
        try:
            it.next()
        except StopIteration:
            return fmt % s

        # Add ellipsis indicating truncation.
        # Correctly handle the corner case of max_elements == 0.
        return fmt % (s + ", ..." if s else "...")

    if x is __builtin__.__dict__:
        return "<builtins>"
    elif type(x) == dict:
        return _it_to_string("{%s}", sorted(x.iteritems()), per_element=_per_dict_element)
    elif type(x) == list:
        return _it_to_string("[%s]", x)
    elif type(x) == tuple:
        return _it_to_string("(%s)" if len(x) != 1
                                       or max_recursion <= 0
                                       or max_elements <= 0
                             else "(%s,)", x)
    elif type(x) == set:
        return _it_to_string("set([%s])", sorted(x))
    elif type(x) == frozenset:
        return _it_to_string("frozenset([%s])", sorted(x))
    elif type(x) in types.StringTypes and max_string < len(x):
        return repr(x[:max_string] + "...")
    elif type(x) == ImmutableMultiDict:
        x = x.to_dict(flat=False)
        return _it_to_string("ImmutableMultiDict({%s})", sorted(x.iteritems()),
                             per_element=_per_dict_element)
    else:
        try:
            if issubclass(x, dict):
                x = dict(x)
                return _it_to_string("Dict({%s})", sorted(x.iteritems()),
                                     per_element=_per_dict_element)
        except TypeError:
            pass
        return repr(x)


def can_be_skipped(key, value):
    # Identifiers that are all uppercase are almost always constants.
    if re.match('[A-Z0-9_]+$', key):
        return True
    # dunder functions.
    if re.match('__.*__$', key):
        return True
    if callable(value):
        return True
    if isinstance(value, types.ModuleType):
        return True
    return False


def format_exception(ty, val, tb, max_elements=1000,
                     max_string=10000, max_recursion=100,
                     maskable=None):
    """
    :param ty:
    :param val:
    :param tb:
    :param max_elements:  Maximum number of elements to be printed
    :param max_string: Max string length in print
    :param max_recursion: Recursive printing in case of dict or other items
    :param maskable: Masking rule for key/value pair
    :return: a formatted string

    Walk over all the frames and get the local variables from the frame and format them using format function and
    write to the stringIO based file.
    """
    stack = []
    t = tb
    while t:
        stack.append(t.tb_frame)
        t = t.tb_next
    buf = cStringIO.StringIO()
    w = buf.write
    # Go through each frame and format them to get final string
    for frame in stack:
        w('\n  File "%s", line %s, in %s\n' % (frame.f_code.co_filename,
                                               frame.f_lineno,
                                               frame.f_code.co_name))
        local_vars = frame.f_locals.items()
        local_vars.sort()
        for key, value in local_vars:
            if can_be_skipped(key, value):
                continue

            w("    %20s = " % key)
            masked = False
            if maskable:
                masked, val = maskable(key)
                if masked:
                    w(val)
            if not masked:
                # try:
                w(format_frame(value, max_elements, max_string, max_recursion,
                               maskable=maskable))
                # except Exception:
                #     exc_class = sys.exc_info()[0]
                #     w("<%s raised while printing value>" % exc_class)
            w("\n")
    w("\n")
    w(''.join(traceback.format_tb(tb)))
    op = buf.getvalue()
    buf.close()
    return op


def print_exception():
    ty, val, tb = sys.exc_info()
    string = format_exception(ty, val, tb)
    print string
    traceback.print_tb(tb)
