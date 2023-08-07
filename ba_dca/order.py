from enum import Enum
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Union


class Frequency(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """

    HOURLY = 1
    DAILY = 2
    WEEKLY = 3
    MONTHLY = 4
    YEARLY = 5

    @classmethod
    def freq_to_relative_delta(cls, freq: "Frequency") -> relativedelta:
        """Convert the Frequency enum to dateutil.relativedelta.

        Args:
            freq (Frequency): Order frequency as time.

        Returns:
            relativedelta: dateutil.relativedelta to be used with datetime module.
        """
        if freq == Frequency.HOURLY:
            return relativedelta(hours=+1)
        if freq == Frequency.DAILY:
            return relativedelta(days=+1)
        if freq == Frequency.WEEKLY:
            return relativedelta(weeks=+1)
        if freq == Frequency.MONTHLY:
            return relativedelta(months=+1)
        if freq == Frequency.YEARLY:
            return relativedelta(years=+1)
        return relativedelta


class Order:
    """_summary_"""

    def __init__(
        self,
        symbol: str,
        amount: float,
        freq: Union[Frequency, relativedelta] = Frequency.DAILY,
        start_date=datetime.now(),
    ) -> None:
        self._symbol = symbol
        self._amount = amount
        self._freq = (
            freq
            if isinstance(freq, relativedelta)
            else Frequency.freq_to_relative_delta(freq)
        )
        self._start_date = start_date
        self._next_order_t = self._start_date + self._freq
        self._last_order_t: datetime = None

    def execute(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        self._last_order_t = datetime.now()
        self._next_order_t = datetime.now() + self._freq

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
