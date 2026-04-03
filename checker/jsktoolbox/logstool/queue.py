# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2024-09-06

Purpose: Provide a minimal FIFO queue implementation for the logging subsystem.

`LoggerQueue` stores log level/message pairs in memory when engines cannot
dispatch immediately.
"""

from typing import Optional, List

from ..attribtool import NoDynamicAttributes
from ..basetool.classes import BClasses
from .keys import LogsLevelKeys
from ..raisetool import Raise
from inspect import currentframe


class LoggerQueue(BClasses, NoDynamicAttributes):
    """In-memory FIFO storage for log messages."""

    __queue: List[List[str]] = []

    def __init__(self) -> None:
        """Initialise an empty queue."""
        self.__queue = []

    def get(self) -> Optional[tuple[str, ...]]:
        """Return and remove the next queued log entry.

        ### Returns:
        Optional[tuple[str, ...]] - Tuple in form `(level, message)` or None when empty.

        ### Raises:
        * Exception: Re-raised as `Raise.error` when unexpected errors occur.
        """
        try:
            return tuple(self.__queue.pop(0))
        except IndexError:
            return None
        except Exception as ex:
            raise Raise.error(
                f"Unexpected exception was thrown: {ex}",
                Exception,
                self._c_name,
                currentframe(),
            )

    def put(self, message: str, log_level: str = LogsLevelKeys.INFO) -> None:
        """Append a new log entry to the queue.

        ### Arguments:
        * message: str - Log message payload.
        * log_level: str - Log severity; defaults to `LogsLevelKeys.INFO`.

        ### Returns:
        None - The queue is mutated in place.

        ### Raises:
        * KeyError: When `log_level` is not part of `LogsLevelKeys.keys`.
        """
        if log_level not in LogsLevelKeys.keys:
            raise Raise.error(
                f"logs_level key not found, '{log_level}' received.",
                KeyError,
                self._c_name,
                currentframe(),
            )
        self.__queue.append(
            [
                log_level,
                message,
            ]
        )


# #[EOF]#######################################################################
