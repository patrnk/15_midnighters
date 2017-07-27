import json
import unittest
from unittest.mock import patch, MagicMock

import seek_dev_nighters


class MidNightersTestCase(unittest.TestCase):

    def setUp(self):
        with open('solution_attempts_fixture.json') as fixture_file:
            self.fixture = json.load(fixture_file)

    @patch('seek_dev_nighters.requests.get')
    def test_load_attempts_loads_attempts_correctly(self, patched_get):
        response = MagicMock()
        response.json = MagicMock(side_effect=self.fixture)
        patched_get.return_value = response
        attempt_batches = seek_dev_nighters.load_attempts()
        for batch_number, batch in enumerate(attempt_batches):
            expected_output = self.fixture[batch_number]['records']
            self.assertEqual(batch, expected_output)


if __name__ == '__main__':
    unittest.main()
