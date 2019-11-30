from base_test_runner import *

os.environ['DJANGO_SETTINGS_MODULE'] = 'DjangoTest.custom_model_settings'
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(["test_db_model"])
sys.exit(bool(failures))
