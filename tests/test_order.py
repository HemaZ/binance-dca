import unittest
from ba_dca.order import Order, Frequency, relativedelta, datetime


class OrderUTests(unittest.TestCase):
    def test_ctor_relative_delta(self):
        start_t = datetime.now()
        order = Order("BTCUSDT", 10, relativedelta(years=+1), start_date=start_t)
        next_order_t = start_t + relativedelta(years=+1)
        self.assertEqual(order.next_execution_time, next_order_t)

    def test_ctor_freq(self):
        start_t = datetime.now()
        freq = Frequency.DAILY
        order = Order("BTCUSDT", 10, freq, start_date=start_t)
        next_order_t = start_t + relativedelta(days=+1)
        self.assertEqual(order.next_execution_time, next_order_t)
