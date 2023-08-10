import unittest
from ba_dca.frequency import Frequency, relativedelta, str_to_relativedelta


class FreqUTests(unittest.TestCase):
    """Unit tests for the frequency module"""

    def test_str_to_relativedelta(self):
        """Test str_to_relativedelta function"""
        d_orig = relativedelta(years=+1, weeks=+1, days=+2)
        d_from_str = str_to_relativedelta(str(d_orig))
        self.assertEqual(d_orig, d_from_str)
