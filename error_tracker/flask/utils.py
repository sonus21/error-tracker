# -*- coding: utf-8 -*-
#     Utils modules for flask plugin
#
#     :copyright: 2020 Sonu Kumar
#     :license: BSD-3-Clause
#
from error_tracker import ContextBuilderMixin, ViewPermissionMixin


class DefaultFlaskContextBuilder(ContextBuilderMixin):
    """
    Default request builder, this records, form data, header and URL parameters and mask them if necessary
    """

    def get_context(self, request, masking=None, additional_context=None):
        request_data = dict()
        if additional_context is not None and len(additional_context) != 0:
            request_data['context'] = additional_context

        if request is not None:
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
            request_data.update({
                'headers': headers,
                'args': dict(request.args),
                'form': form
            })
        return str(request_data)


class DefaultFlaskViewPermission(ViewPermissionMixin):

    def __call__(self, request):
        return False


class configure_scope(object):
    """
    Use this class to work with context manager where more context can be added on the fly

    usage
    with configure_scope() as scope:
        scope.set_extra("id", 1234)
    """

    def __init__(self, error_manager, context=None, handle_exception=True):
        """
        Initialize class with error_manager instance.
        :param error_manager: AppErrorTracker instance
        :param handle_exception:  whether raised exception is ignored or not, post exception capture
        :param context: initial context detail, dictionary of key value pairs
        """
        self.context = context or {}
        self.error_manager = error_manager
        self.handle_exception = handle_exception

    def set_extra(self, key, value):
        self.context[key] = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.error_manager.capture_exception(additional_context=self.context)
        return self.handle_exception
