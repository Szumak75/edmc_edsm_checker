# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 02.12.2023

Purpose: Sets of classes for various date/time operations.
"""

import calendar
from time import time
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, Union
from inspect import currentframe

from .attribtool import NoNewAttributes
from .raisetool import Raise


class DateTime(NoNewAttributes):
    """A utility class for generating various datetime structures."""

    @classmethod
    def now(cls, tz: Optional[timezone] = None) -> datetime:
        """Return a datetime object for the current time.

        ### Arguments:
        * tz: Optional[timezone] - The timezone for the object. Defaults to None (local time).

        ### Returns:
        datetime - The current datetime object.
        """
        return datetime.now(tz=tz)

    @classmethod
    def datetime_from_timestamp(
        cls,
        timestamp_seconds: Union[int, float],
        tz: Optional[timezone] = None,
    ) -> datetime:
        """Create a datetime object from a Unix timestamp.

        ### Arguments:
        * timestamp_seconds: Union[int, float] - The Unix timestamp in seconds.
        * tz: Optional[timezone] - The timezone for the object. Defaults to None.

        ### Returns:
        datetime - The datetime object corresponding to the timestamp.

        ### Raises:
        * TypeError: If `timestamp_seconds` is not an int or float.
        """
        if not isinstance(timestamp_seconds, (int, float)):
            raise Raise.error(
                f"Expected int or float type, received: '{type(timestamp_seconds)}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return datetime.fromtimestamp(timestamp_seconds, tz=tz)

    @classmethod
    def elapsed_time_from_seconds(cls, seconds: Union[int, float]) -> timedelta:
        """Convert a duration in seconds into a timedelta object.

        ### Arguments:
        * seconds: Union[int, float] - The duration in seconds.

        ### Returns:
        timedelta - The timedelta object representing the duration.

        ### Raises:
        * TypeError: If `seconds` is not an int or float.
        """
        if not isinstance(seconds, (int, float)):
            raise Raise.error(
                f"Expected int or float type, received: '{type(seconds)}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        return timedelta(seconds=seconds)

    @classmethod
    def elapsed_time_from_timestamp(
        cls, seconds: Union[int, float], tz: Optional[timezone] = None
    ) -> timedelta:
        """Calculate the elapsed time from a given timestamp to now.

        ### Arguments:
        * seconds: Union[int, float] - The starting Unix timestamp in seconds.
        * tz: Optional[timezone] - The timezone for the calculation. Defaults to None.

        ### Returns:
        timedelta - The timedelta object for the elapsed time, accurate to the second.

        ### Raises:
        * TypeError: If `seconds` is not an int or float.
        """
        if not isinstance(seconds, (int, float)):
            raise Raise.error(
                f"Expected int or float type, received: '{type(seconds)}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        out: timedelta = cls.now(tz=tz) - datetime.fromtimestamp(seconds, tz=tz)
        return timedelta(days=out.days, seconds=out.seconds)


class Timestamp(NoNewAttributes):
    """A utility class for generating Unix timestamps."""

    @classmethod
    def now(
        cls, returned_type: Union[type[int], type[float]] = int
    ) -> Union[int, float]:
        """Get the current Unix timestamp.

        ### Arguments:
        * returned_type: Union[type[int], type[float]] - The desired type, `int` (default) or `float`.

        ### Returns:
        Union[int, float] - The current Unix timestamp.

        ### Raises:
        * TypeError: If `returned_type` is not `int` or `float`.
        """
        if returned_type not in (int, float):
            raise Raise.error(
                f"Expected int or float type, received: '{returned_type}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        if returned_type == int:
            return int(time())
        return time()

    @classmethod
    def from_string(
        cls,
        date_string: str,
        format: str,
        returned_type: Union[type[int], type[float]] = int,
    ) -> Union[int, float]:
        """Create a Unix timestamp from a string representation of a date.

        ### Arguments:
        * date_string: str - The string containing the date and/or time.
        * format: str - The `strptime` format code used to parse the `date_string`.
        * returned_type: Union[type[int], type[float]] - The desired type, `int` (default) or `float`.

        ### Returns:
        Union[int, float] - The Unix timestamp derived from the string.

        ### Raises:
        * TypeError: If `returned_type` is not `int` or `float`.
        * ValueError: If `date_string` cannot be parsed with the given `format`.
        """
        if returned_type not in (int, float):
            raise Raise.error(
                f"Expected int or float type, received: '{returned_type}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )

        try:
            element: datetime = datetime.strptime(date_string, format)
        except ValueError as ex:
            raise Raise.error(f"{ex}", ValueError, cls.__qualname__, currentframe())

        if returned_type == int:
            return int(datetime.timestamp(element))
        return datetime.timestamp(element)

    @classmethod
    def month_timestamp_tuple(
        cls,
        query_date: Optional[Union[float, int, datetime]] = None,
        tz: Optional[timezone] = timezone.utc,
    ) -> Tuple[float, float]:
        """Get the start and end Unix timestamps for a given month.

        If `query_date` is not provided, the current month is used.

        ### Arguments:
        * query_date: Optional[Union[float, int, datetime]] - The date to determine the month (timestamp or datetime object). Defaults to None.
        * tz: Optional[timezone] - The timezone for the calculation. Defaults to `timezone.utc`.

        ### Returns:
        Tuple[float, float] - A tuple with the start and end timestamps of the month.

        ### Raises:
        * TypeError: If `tz` or `query_date` is an unsupported type.
        """

        q_date: datetime = DateTime.now(tz)

        # check types
        if tz and not isinstance(tz, timezone):
            raise Raise.error(
                f"Expected tzinfo as datetime.timezone type, received: '{type(tz)}'.",
                TypeError,
                cls.__qualname__,
                currentframe(),
            )
        if query_date:
            if isinstance(query_date, (int, float)):
                # receive timestamp number
                q_date = DateTime.datetime_from_timestamp(
                    timestamp_seconds=query_date, tz=tz
                )
            elif isinstance(query_date, datetime):
                # receive datetime format
                q_date = query_date
            else:
                raise Raise.error(
                    f"Excepted date as timestamp or datetime.datetime format, received: '{type(query_date)}'.",
                    TypeError,
                    cls.__qualname__,
                    currentframe(),
                )

        # Call the helper method with the determined year and month
        return cls._get_month_timestamp(q_date.year, q_date.month, tz=tz)

    @classmethod
    def _get_month_timestamp(
        cls, year: int, month: int, tz: Optional[timezone] = timezone.utc
    ) -> Tuple[float, float]:
        """Generate the start and end Unix timestamps for a specific month and year.

        This is a private helper method.

        ### Arguments:
        * year: int - The target year.
        * month: int - The target month (1-12).
        * tz: Optional[timezone] - The timezone for the calculation. Defaults to `timezone.utc`.

        ### Returns:
        Tuple[float, float] - A tuple with the start and end timestamps of the month.

        ### Raises:
        * ValueError: If the month is not between 1 and 12.
        """
        # Validate month input
        if not 1 <= month <= 12:
            raise Raise.error(
                "Month must be between 1 and 12.",
                ValueError,
                cls.__qualname__,
                currentframe(),
            )

        # The first moment of the month in UTC
        start_dt = datetime(year, month, 1, 0, 0, 0, tzinfo=tz)

        # Find the number of days in the month
        _, num_days = calendar.monthrange(year, month)

        # The very last moment of the month in UTC
        end_dt = datetime(year, month, num_days, 23, 59, 59, 999999, tzinfo=tz)

        # Convert datetime objects to Unix timestamps
        start_timestamp: float = start_dt.timestamp()
        end_timestamp: float = end_dt.timestamp()

        return (start_timestamp, end_timestamp)


# #[EOF]#######################################################################
