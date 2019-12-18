from base_test_runner import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoTest.django_rest_framework_settings'
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(["test_drf"])
