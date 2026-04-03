# -*- coding: utf-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2024-01-15

Purpose: Provide foundational classes for the logging subsystem.

Defines base containers for logger queues, engine metadata, and formatting
behaviour leveraged by higher-level logging utilities.
"""


from typing import Optional, List, Any

from ..logstool.keys import LogKeys
from ..logstool.queue import LoggerQueue

from .data import BData
from ..attribtool import NoDynamicAttributes


class BLoggerQueue(BData):
    """Base container that exposes a lazily-created logging queue."""

    @property
    def logs_queue(self) -> Optional[LoggerQueue]:
        """Return the configured logging queue instance.

        ### Returns:
        [Optional[LoggerQueue]] - Logger queue or None when not set.
        """
        return self._get_data(
            key=LogKeys.QUEUE,
            default_value=None,
            set_default_type=Optional[LoggerQueue],
        )

    @logs_queue.setter
    def logs_queue(self, obj: Optional[LoggerQueue]) -> None:
        """Assign the logger queue instance.

        ### Arguments:
        * obj: Optional[LoggerQueue] - Queue instance or None.
        """
        self._set_data(
            key=LogKeys.QUEUE, value=obj, set_default_type=Optional[LoggerQueue]
        )


class BLoggerEngine(BData):
    """Base container for logger engine metadata."""

    @property
    def name(self) -> Optional[str]:
        """Return the configured application name.

        ### Returns:
        [Optional[str]] - Application name value or None.
        """
        return self._get_data(
            key=LogKeys.NAME,
            set_default_type=Optional[str],
            default_value=None,
        )

    @name.setter
    def name(self, value: str) -> None:
        """Assign the application name.

        ### Arguments:
        * value: str - Application name string.
        """
        self._set_data(key=LogKeys.NAME, value=value, set_default_type=Optional[str])


class BLogFormatter(NoDynamicAttributes):
    """Base class for log formatters leveraging simple templates."""

    __template: Optional[str] = None
    __forms: Optional[List] = None

    def format(self, message: str, name: Optional[str] = None) -> str:
        """Render a log message based on the configured forms list.

        ### Arguments:
        * message: str - Log string to include in the output.
        * name: Optional[str] - Optional application name.

        ### Returns:
        [str] - Formatted log payload.
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
        """Return the list of formatter components.

        ### Returns:
        [List] - Current forms definition list.
        """
        if self.__forms is None:
            self.__forms = []
        return self.__forms

    @_forms_.setter
    def _forms_(self, item: Any) -> None:
        """Append a formatter component to the forms list.

        ### Arguments:
        * item: Any - Callable or string template.
        """
        self._forms_.append(item)


# #[EOF]#######################################################################
