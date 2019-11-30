from base_test_runner import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoTest.notification_settings'
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(["test_notification"])
sys.exit(bool(failures))
