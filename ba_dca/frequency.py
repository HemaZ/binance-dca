from enum import Enum
from dateutil.relativedelta import relativedelta


class Frequency(Enum):
    """Trading frequency."""

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
