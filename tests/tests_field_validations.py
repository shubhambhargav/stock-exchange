import os
import json
import inspect
import unittest
from executor import MarketRunner

from conf import settings
from utils import Utilities

PROJECT_ROOT = settings.PROJECT_ROOT
INPUT_FIELDS = settings.INPUT_FIELDS


class StockMarketFieldsTest(unittest.TestCase):

    """
    Validation check for every field given in 'settings' file as INPUT_FIELDS.
    """

    @classmethod
    def setUpClass(cls):
        # Extract expected input/output details from the following fixture
        fixtures_loc = os.path.join(PROJECT_ROOT, 'tests', 'fixtures', 'field_validations.json')
        cls.testing_data = json.load(open(fixtures_loc))

    def test_field_validation(self):
        for f in INPUT_FIELDS:
            # Fetch test configuration from fixtures
            function_name = inspect.stack()[0][3].replace('field', f)
            try:
                test_conf = self.testing_data[function_name]
            except KeyError:
                raise Exception("Tests not configured for field: '%s'" % f)

            runner_obj = MarketRunner()

            for inp in test_conf['input']:
                try:
                    runner_obj.execute(inp)
                except Exception as ex:
                    if inp.get(f):
                        if f == 'action':
                            self.assertEqual(type(ex), ValueError) # Choice Field will give ValueError
                        else:
                            self.assertEqual(type(ex), TypeError)
                    else:
                        self.assertEqual(type(ex), ValueError)
