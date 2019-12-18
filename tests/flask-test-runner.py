import unittest
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from FlaskTest.test_basic import BasicTest
from FlaskTest.test_db_model import CustomModelClassTest
from FlaskTest.test_end_point import ViewTest
from FlaskTest.test_init_later import InitLaterTest
from FlaskTest.test_manager_crud import AppErrorTrackerCrudTest
from FlaskTest.test_mask_rule import DefaultMaskingRuleTest, NoMaskingTest, CustomMaskingClassTest, \
    CustomMaskingRuleTest
from FlaskTest.test_notification import NotificationDisabledTest, NotificationEnabledByAppInstanceTest, \
    NotificationEnabledTest
from FlaskTest.test_ticketing import TicketingTest
from FlaskTest.test_url_prefix import UrlPrefixTest
from FlaskTest.test_manual_error_tracking import RecordErrorTest
from FlaskTest.test_401_views import View401Test

loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(BasicTest)
suite.addTests(loader.loadTestsFromTestCase(CustomModelClassTest))
suite.addTests(loader.loadTestsFromTestCase(ViewTest))
suite.addTests(loader.loadTestsFromTestCase(InitLaterTest))
suite.addTests(loader.loadTestsFromTestCase(AppErrorTrackerCrudTest))
suite.addTests(loader.loadTestsFromTestCase(RecordErrorTest))
suite.addTests(loader.loadTestsFromTestCase(CustomMaskingClassTest))
suite.addTests(loader.loadTestsFromTestCase(CustomMaskingRuleTest))
suite.addTests(loader.loadTestsFromTestCase(NoMaskingTest))
suite.addTests(loader.loadTestsFromTestCase(DefaultMaskingRuleTest))
suite.addTests(loader.loadTestsFromTestCase(NotificationEnabledTest))
suite.addTests(loader.loadTestsFromTestCase(NotificationEnabledByAppInstanceTest))
suite.addTests(loader.loadTestsFromTestCase(NotificationDisabledTest))
suite.addTests(loader.loadTestsFromTestCase(TicketingTest))
suite.addTests(loader.loadTestsFromTestCase(UrlPrefixTest))
suite.addTests(loader.loadTestsFromTestCase(View401Test))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
sys.exit(bool(result.failures))
