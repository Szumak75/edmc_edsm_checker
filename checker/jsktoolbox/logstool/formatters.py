# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 10.10.2023

Purpose: LogFormatter classes.
"""

from datetime import datetime

from ..basetool.logs import BLogFormatter
from ..datetool import Timestamp


class LogFormatterNull(BLogFormatter):
    """Log Formatter Null class."""

    def __init__(self) -> None:
        """Constructor."""
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")


class LogFormatterDateTime(BLogFormatter):
    """Log Formatter DateTime class."""

    def __init__(self) -> None:
        """Constructor."""
        self._forms_.append(self.__get_formatted_date__)
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")

    def __get_formatted_date__(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class LogFormatterTime(BLogFormatter):
    """Log Formatter Time class."""

    def __init__(self) -> None:
        """Constructor."""
        self._forms_.append(self.__get_formatted_time__)
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")

    def __get_formatted_time__(self) -> str:
        return datetime.now().strftime("%H:%M:%S")


class LogFormatterTimestamp(BLogFormatter):
    """Log Formatter Timestamp class."""

    def __init__(self) -> None:
        """Constructor."""
        self._forms_.append(Timestamp.now())
        self._forms_.append("{message}")
        self._forms_.append("[{name}]: {message}")


# #[EOF]#######################################################################
