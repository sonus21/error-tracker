# -*- coding: utf-8 -*-
#     Utils modules for flask plugin
#
#     :copyright: 2019 Sonu Kumar
#     :license: BSD-3-Clause
#

from error_tracker import ContextBuilderMixin


class DefaultFlaskContextBuilder(ContextBuilderMixin):
    """
    Default request builder, this records, form data, header and URL parameters and mask them if necessary
    """

    def get_context(self, request, masking=None):
        if request is None:
            return {}
        form = dict(request.form)
        headers = dict(request.headers)
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
            'args': dict(request.args),
            'form': form
        })
        return request_data
