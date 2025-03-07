# -*- coding: utf-8 -*-
"""
logs.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 15.01.2024, 10:24:15

Purpose: Base classes for log subsystem.
"""


from typing import Optional, List, Any

from ..logstool.keys import LogKeys
from ..logstool.queue import LoggerQueue

from .data import BData
from ..attribtool import NoDynamicAttributes


class BLoggerQueue(BData):
    """Logger Queue base metaclass."""

    @property
    def logs_queue(self) -> Optional[LoggerQueue]:
        """Get LoggerQueue object."""
        return self._get_data(
            key=LogKeys.QUEUE,
            default_value=None,
            set_default_type=Optional[LoggerQueue],
        )

    @logs_queue.setter
    def logs_queue(self, obj: Optional[LoggerQueue]) -> None:
        """Set LoggerQueue object."""
        self._set_data(
            key=LogKeys.QUEUE, value=obj, set_default_type=Optional[LoggerQueue]
        )


class BLoggerEngine(BData):
    """Base class for LoggerEngine classes."""

    @property
    def name(self) -> Optional[str]:
        """Return app name string."""
        return self._get_data(
            key=LogKeys.NAME,
            set_default_type=Optional[str],
            default_value=None,
        )

    @name.setter
    def name(self, value: str) -> None:
        """Set app name string."""
        self._set_data(key=LogKeys.NAME, value=value, set_default_type=Optional[str])


class BLogFormatter(NoDynamicAttributes):
    """Log formatter base class."""

    __template: Optional[str] = None
    __forms: Optional[List] = None

    def format(self, message: str, name: Optional[str] = None) -> str:
        """Method for format message string.

        Arguments:
        message [str]: log string to send
        name [str]: optional name of apps,
        """
        out: str = ""
        for item in self._forms_:
            if callable(item):
                out += f"{item()} "
            elif isinstance(item, str):
                if name is None:
                    if item.find("name") == -1:
                        out += item.format(message=f"{message}")
                else:
                    if item.find("name") > 0:
                        out += item.format(
                            name=f"{name}",
                            message=f"{message}",
                        )
        return out

    @property
    def _forms_(self) -> List:
        """Get forms list."""
        if self.__forms is None:
            self.__forms = []
        return self.__forms

    @_forms_.setter
    def _forms_(self, item: Any) -> None:
        """Set forms list."""
        self._forms_.append(item)


# #[EOF]#######################################################################
