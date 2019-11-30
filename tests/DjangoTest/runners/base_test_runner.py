import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))
ROOT_DIR = os.path.abspath(os.path.join(TESTS_DIR, os.pardir))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, TESTS_DIR)
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, "DjangoTest")))
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, "tests")))
