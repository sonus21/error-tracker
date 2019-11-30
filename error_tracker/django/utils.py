# -*- coding: utf-8 -*-
#
#    Django error tracker utils classes
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

import re

from django.http import RawPostDataException

from error_tracker.libs.mixins import ContextBuilderMixin, NotificationMixin
from django.core.mail import send_mail


# noinspection PyMethodMayBeStatic
class DefaultDjangoContextBuilder(ContextBuilderMixin):
    """
    Default request builder, this records, form data, header and URL parameters and mask them if necessary
    """

    def _get_form_data(self, request):
        form = {}
        post = request.POST
        if post is None or len(post) == 0:
            body = None
            try:
                body = request.data
            except AttributeError:
                try:
                    body = request.body
                except RawPostDataException:
                    pass
            if body is not None and len(body) > 0:
                import json
                try:
                    form = json.loads(body, "UTF-8")
                except Exception:
                    form = {'data': body}
        else:
            form = post.dict()
        return form

    def _get_headers(self, request):
        try:
            headers = request.headers.dict()
        except AttributeError:
            regex = re.compile('^HTTP_')
            headers = dict((regex.sub('', header), value) for (header, value)
                           in request.META.items() if header.startswith('HTTP_'))
        return headers

    def get_context(self, request, masking=None):
        if request is None:
            return {}
        form = self._get_form_data(request)
        headers = self._get_headers(request)
        if masking:
            for key in form:
                masked, value = masking(key)
                if masked:
                    form[key] = value
            for key in headers:
                masked, value = masking(key)
                if masked:
                    headers[key] = value

        request_data = str({
            'headers': headers,
            'args': request.GET.dict(),
            'form': form
        })
        return request_data


class DjangoNotification(NotificationMixin):
    """
    Send emails to the configured users
    """

    def notify(self, request, exception,
               email_subject=None,
               email_body=None,
               from_email=None,
               recipient_list=None):
        if recipient_list is not None and from_email is not None:
            send_mail(email_subject, email_body, from_email, recipient_list, fail_silently=True)
