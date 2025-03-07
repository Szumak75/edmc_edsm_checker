# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 02.12.2023

Purpose: Sets of classes for various date/time operations.
"""

from time import time
from datetime import datetime, timezone, timedelta
from typing import Optional, Union
from inspect import currentframe

from .attribtool import NoNewAttributes
from .raisetool import Raise


class DateTime(NoNewAttributes):
    """DateTime class for generating various datetime structures."""

    @classmethod
    def now(cls, tz: Optional[timezone] = None) -> datetime:
        """Return datetime.datetime.now() object.

        ### Arguments:
        tz [datetime.timezone] - datetime.timezone.utc for UTC, default None for current set timezone.
        """
        return datetime.now(tz=tz)

    @classmethod
    def datetime_from_timestamp(
        cls,
        timestamp_seconds: Union[int, float],
        tz: Optional[timezone] = None,
    ) -> datetime:
        """Returns datetime from timestamp int."""
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
        """Convert given seconds to timedelta structure."""
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
        """Generate date/time timedelta with elapsed time, from given timestamp to now.

        ### WARNING:
        Returns the timedelta accurate to the second.
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
    """Timestamp class for getting current timestamp."""

    @classmethod
    def now(
        cls, returned_type: Union[type[int], type[float]] = int
    ) -> Union[int, float]:
        """Return current timestamp as int or float."""
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
        """Returns timestamp from string in strptime format.

        ### Arguments
        * date_string [str] - date/time string to parse,
        * format [str] - string with date/time format, for example: '%Y-%m-%d'
        * return_type [int or float] - type of returned timestamp.

        ### Returns
        timestamp as int or float
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
        except Exception as ex:
            raise ex

        if returned_type == int:
            return int(datetime.timestamp(element))
        return datetime.timestamp(element)


# #[EOF]#######################################################################
