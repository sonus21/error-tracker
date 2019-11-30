#!/bin/bash
set -e
python tests/DjangoTest/runners/common_runner.py
python tests/DjangoTest/runners/custom_masking_test_runner.py
python tests/DjangoTest/runners/masking_disabled_test_runner.py
python tests/DjangoTest/runners/model_test_runner.py
python tests/DjangoTest/runners/notification_test_runner.py
python tests/flask-test-runner.py