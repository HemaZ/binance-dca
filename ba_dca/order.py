from datetime import datetime
from typing import Union
from ba_dca.frequency import Frequency, relativedelta


class Order:
    """Class to represent an recurring order."""

    def __init__(
        self,
        symbol: str,
        amount: float,
        freq: Union[Frequency, relativedelta] = Frequency.DAILY,
        start_date=datetime.now(),
    ) -> None:
        """Create a new Order.

        Args:
            symbol (str): Trading pair symbol. for example 'BTCUSDT'
            amount (float): Amount to buy in the base asset, for example if the pair is BTCUSDT,
            then this will be the amount in USDT.
            freq (Union[Frequency, relativedelta], optional): Trading frequency.
            Defaults to Frequency.DAILY.
            start_date (datetime, optional): When to start this trade. Defaults to datetime.now().
        """
        self._symbol = symbol
        self._amount = amount
        self._freq = (
            freq
            if isinstance(freq, relativedelta)
            else Frequency.freq_to_relative_delta(freq)
        )
        self._total_usd = 0
        self._total_qty = 0
        self._average = 0
        self._start_date = start_date
        self._next_order_t = self._start_date + self._freq
        self._last_order_t: datetime = None

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Order):
            return (
                (self.symbol == other.symbol)
                and (self.amount == other.amount)
                and (self.start_date == other.start_date)
                and (self.frequency == other.frequency)
            )
        return False

    def __str__(self) -> str:
        return (
            f"Symbol:{self.symbol} Amount:{self.amount}"
            f"Freq:{str(self.frequency)} Date:{str(self.start_date)}"
        )

    def execute(self, qty: float, price: float, order_time: datetime = datetime.now()):
        """Mark the order as executed."""
        self._total_qty += qty
        self._total_usd += qty * price
        self._average = self._total_usd / self._total_qty
        self._last_order_t = order_time
        self._next_order_t = self._last_order_t + self._freq

    @property
    def next_execution_time(self) -> datetime:
        """Return the time of the next order.

        Returns:
            datetime: Next order's time.
        """
        return self._next_order_t

    @property
    def last_executed_time(self) -> Union[datetime, None]:
        """Return the time of the last executed order.

        Returns:
            Union[datetime, None]: Last executed order time. None if no executed orders.
        """
        return self._last_order_t

    @property
    def symbol(self) -> str:
        """Return the order symbol.

        Returns:
            str: Return the order symbol.
        """
        return self._symbol

    @property
    def amount(self) -> float:
        """Return the order amount.

        Returns:
            float: order amount.
        """
        return self._amount

    @property
    def start_date(self) -> datetime:
        """Return the order amount.

        Returns:
            float: order amount.
        """
        return self._start_date

    @property
    def frequency(self) -> relativedelta:
        """Return the order frequency.

        Returns:
            relativedelta: order frequency.
        """
        return self._freq

    @property
    def average(self) -> float:
        return self._average
