#!/bin/bash
set -e
for tst in tests/DjangoTest/runners/*.py; do
  python "$tst"
done

python tests/flask-test-runner.py