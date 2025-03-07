# -*- coding: utf-8 -*-
"""
queue.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 6.09.2024, 16:43:41

Purpose: Queue for logs subsystem.
"""

from typing import Optional, Tuple, List, Any

from ..attribtool import NoDynamicAttributes
from ..basetool.classes import BClasses
from .keys import LogsLevelKeys
from ..raisetool import Raise


from inspect import currentframe
from typing import List


class LoggerQueue(BClasses, NoDynamicAttributes):
    """LoggerQueue simple class."""

    __queue: List[List[str]] = []

    def __init__(self) -> None:
        """Constructor."""
        self.__queue = []

    def get(self) -> Optional[tuple[str, ...]]:
        """Get item from queue.

        Returns queue tuple[log_level:str, message:str] or None if empty.
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
        """Put item to queue."""
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
