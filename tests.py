import json
import unittest
from unittest.mock import patch, MagicMock

import seek_dev_nighters


class MidNightersTestCase(unittest.TestCase):

    def setUp(self):
        with open('fixtures/solution_attempts_fixture.json') as fixture_file:
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

    def test_is_midnighter_returns_true(self):
        test_inputs = [
            (1501362923.128152, 'Europe/Moscow'),  # 0 hours
            (1501464923.129152, 'Europe/Moscow'),  # 4 hours
            (1501210889.0, 'Europe/Moscow'),  # 6 hours
            (1501214889.0, 'UTC'),  # 7 in Moscow, 4 in UTC
        ]
        for test_input in test_inputs:
            output = seek_dev_nighters.is_midnighter(*test_input)
            self.assertTrue(output)

    def test_is_midnighter_returns_false(self):
        test_inputs = [
            (1501361923.129152, 'Europe/Moscow'),  # 23 hours
            (1501361923.129152, 'UTC'),  # 20 hours
            (1501214889.0, 'Europe/Moscow'),  # 7 hours
        ]
        for test_input in test_inputs:
            output = seek_dev_nighters.is_midnighter(*test_input)
            self.assertFalse(output)

    @patch.object(seek_dev_nighters, 'is_midnighter', side_effect=[True, False, True, True])
    def test_get_midnighter_usernames_returns_correct_usernames(self, patched_is_midnighter):
        test_input = [
            {'username': 1, 'timestamp': 1, 'timezone': 1},
            {'username': 2, 'timestamp': 1, 'timezone': 1},
            {'username': 3, 'timestamp': 1, 'timezone': 1},
            {'username': 4, 'timestamp': 1, 'timezone': 1},
            {'username': 5, 'timestamp': None, 'timezone': 1},
        ]
        expected_output = [1, 3, 4]
        output = seek_dev_nighters.get_midnighter_usernames(test_input)
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
