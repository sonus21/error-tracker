import datetime
from collections import namedtuple

from error_tracker import ModelMixin, MaskingMixin

Error = namedtuple("Error", "hash, host, path, method, request_data, exception_name,"
                            " traceback, count, created_on, last_seen")
paginator = namedtuple("Paginator", "has_next, has_prev, next_num, prev_num, items")


class ErrorModel(ModelMixin):
    objects = {}

    @classmethod
    def delete_entity(cls, rhash):
        cls.objects.pop(rhash)

    @classmethod
    def create_or_update_entity(cls, rhash, host, path, method, request_data,
                                exception_name, traceback):
        count = 1
        now = datetime.datetime.now()
        created_on = now
        traceback = traceback

        if rhash in cls.objects:
            error = cls.objects[rhash]
            created_on = error.created_on
            exception_name = error.exception_name
            traceback = error.traceback
            count = error.count + 1
        error = Error(rhash, host, path, method, str(request_data),
                      exception_name, traceback, count, created_on, now)
        cls.objects[rhash] = error
        return error

    @classmethod
    def get_exceptions_per_page(cls, page_number=1):
        return paginator(False, False, None, None, list(cls.objects.values()))

    @classmethod
    def get_entity(cls, rhash):
        error = cls.objects.get(rhash, None)
        return error


class Masking(MaskingMixin):
    pass
