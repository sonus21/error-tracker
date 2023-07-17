# -*- coding: utf-8 -*-
#
#    Django error tracker default model
#
#    :copyright: 2023 Sonu Kumar
#    :license: BSD-3-Clause
#
from django.core.paginator import Paginator, EmptyPage
from django.db import models
from error_tracker.libs.mixins import ModelMixin
from django.utils.timezone import now
from traceback import print_exc
from .settings import EXCEPTION_APP_DEFAULT_LIST_SIZE
from collections import namedtuple

Page = namedtuple("Page", "has_next, next_num, has_prev, prev_num, items ")


class AbstractErrorModel(models.Model, ModelMixin):
    """
       Base Model to track exceptions
    """
    hash = models.CharField(max_length=64, primary_key=True)
    host = models.CharField(max_length=1024)
    path = models.CharField(max_length=4096)
    method = models.CharField(max_length=64)
    request_data = models.TextField()
    exception_name = models.CharField(max_length=256)
    traceback = models.TextField()
    count = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(auto_now=True, db_index=True)
    notification_sent = models.BooleanField(default=False)
    ticket_raised = models.BooleanField(default=False)

    @classmethod
    def get_exceptions_per_page(cls, page_number=1, **query):
        if query:
            if 'page' in query:
                page_number = query['page']
                del query['page']
            query = {"{}__icontains".format(k): v for k, v in query.items()}
        
        if not query:
            records = cls.objects.all().order_by('last_seen')
        else:
            records = cls.objects.filter(**query).order_by('last_seen')

        paginator = Paginator(records, EXCEPTION_APP_DEFAULT_LIST_SIZE)
        try:
            page = paginator.page(page_number)
            return Page(page.has_next(),
                        page.next_page_number() if page.has_next() else None,
                        page.has_previous(),
                        page.previous_page_number() if page.has_previous() else None,
                        page.object_list)
        except EmptyPage:
            return Page(False, None, True, paginator.num_pages, [])

    @classmethod
    def get_entity(cls, rhash):
        return cls.objects.get(hash=rhash)

    @classmethod
    def create_or_update_entity(cls, rhash, host, path, method, request_data, exception_name, traceback):
        try:
            obj, created = cls.objects.get_or_create(hash=rhash)
            if created:
                obj.host, obj.path, obj.method, obj.request_data, obj.exception_name, obj.traceback = \
                    host, path, method, request_data, exception_name, traceback
                obj.count = 1
                obj.save()
            else:
                obj.count += 1
                obj.last_seen = now()
                obj.save(update_fields=['count', 'last_seen'])

            return obj
        except Exception:
            print_exc()

    @classmethod
    def delete_entity(cls, rhash):
        return cls.objects.filter(hash=rhash).delete()

    class Meta:
        abstract = True


class ErrorModel(AbstractErrorModel):
    """
    Default Model to track exceptions
    """

    class Meta(AbstractErrorModel.Meta):
        swappable = 'APP_ERROR_DB_MODEL'
        db_table = 'exceptions'
