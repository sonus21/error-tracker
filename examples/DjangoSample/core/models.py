from collections import namedtuple
from traceback import print_exc

from django.core.paginator import Paginator, EmptyPage
from django.db import models

# Create your models here.
from django.utils.timezone import now

from error_tracker.django.models import AbstractErrorModel

Page = namedtuple("Page", "has_next, next_num, has_prev, prev_num, items ")


class TestErrorModel(AbstractErrorModel):
    class Meta(AbstractErrorModel.Meta):
        db_table = 'test_exceptions'
