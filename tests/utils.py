import datetime
from collections import namedtuple

import six

from error_tracker import ModelMixin, TicketingMixin, NotificationMixin, MaskingMixin

Error = namedtuple("Error", "hash, host, path, method, request_data, exception_name,"
                            " traceback, count, created_on, last_seen")
paginator = namedtuple("Paginator", "has_next, has_prev, next_num, prev_num, items")


class TestErrorModel(ModelMixin):
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

    @classmethod
    def delete_all(cls):
        cls.objects = {}


class TestNotification(NotificationMixin):
    def __init__(self, *args, **kwargs):
        super(TestNotification, self).__init__(*args, **kwargs)
        self.emails = []

    def notify(self, request, exception,
               email_subject=None,
               email_body=None,
               from_email=None,
               recipient_list=None):
        self.emails.append((email_subject, email_body))

    def clear(self):
        self.emails = []

    def get_notifications(self):
        return self.emails


class TicketingSystem(TicketingMixin):
    tickets = []

    def raise_ticket(self, object, request=None):
        self.tickets.append(object)

    def get_tickets(self):
        return self.tickets

    def clear(self):
        self.tickets = []


class Masking(MaskingMixin):
    def __call__(self, key):
        if isinstance(key, six.string_types):
            tmp_key = key.lower()
            for k in self.mask_key_has:
                if k in tmp_key:
                    return True, "'%s'" % self.mask_with
        return False, None
