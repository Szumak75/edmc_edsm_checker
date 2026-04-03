# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2023-10-10

Purpose: Provide reusable log formatter implementations.

Each formatter composes a list of format segments consumed by `BLogFormatter`
to render message payloads consistently across engines.
"""

from datetime import datetime

from ..basetool.logs import BLogFormatter
from ..datetool import Timestamp


class LogFormatterNull(BLogFormatter):
    """Log Formatter Null class."""

    def __init__(self) -> None:
        """Initialise null formatter templates."""
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")


class LogFormatterDateTime(BLogFormatter):
    """Log Formatter DateTime class."""

    def __init__(self) -> None:
        """Initialise date-time formatter templates."""
        self._forms_.append(self.__get_formatted_date__)
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")

    def __get_formatted_date__(self) -> str:
        """Return the current local datetime string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class LogFormatterTime(BLogFormatter):
    """Log Formatter Time class."""

    def __init__(self) -> None:
        """Initialise time-only formatter templates."""
        self._forms_.append(self.__get_formatted_time__)
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")

    def __get_formatted_time__(self) -> str:
        """Return the current local time string."""
        return datetime.now().strftime("%H:%M:%S")


class LogFormatterTimestamp(BLogFormatter):
    """Log Formatter Timestamp class."""

    def __init__(self) -> None:
        """Initialise timestamp formatter templates."""
        self._forms_.append(Timestamp.now())
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")


# #[EOF]#######################################################################
