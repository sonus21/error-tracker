from base_test_runner import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoTest.settings'
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(["test_basic",
                                  "test_end_point",
                                  "test_mask_rule",
                                  "test_ticketing",
                                  "test_notification_disabled",
                                  'test_manual_error_tracking'])
sys.exit(bool(failures))
