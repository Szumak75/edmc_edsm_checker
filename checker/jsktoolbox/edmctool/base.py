# -*- coding: utf-8 -*-
"""
logs.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 7.10.2024, 13:39:19

Purpose: EDMC plugins individual logging subsystem base classes.
"""

from queue import SimpleQueue, Queue
from threading import Thread
from typing import Union

from ..basetool.data import BData
from ..attribtool import ReadOnlyClass

from .logs import LogClient, LogProcessor


class _Keys(object, metaclass=ReadOnlyClass):
    """Internal Keys container class."""

    # base logs
    LOGGER: str = "__logger__"
    LOG_PROCESSOR: str = "__logs_processor__"
    LOG_QUEUE: str = "__logger_queue__"
    TH_LOGGER: str = "__th_logger__"


class BLogProcessor(BData):
    """BLogProcessor base class.

    Container for logger processor methods.
    """

    @property
    def th_log(self) -> Thread:
        """Give me thread logger handler."""
        return self._get_data(key=_Keys.TH_LOGGER, default_value=None)  # type: ignore

    @th_log.setter
    def th_log(self, value: Thread) -> None:
        self._set_data(key=_Keys.TH_LOGGER, value=value, set_default_type=Thread)

    @property
    def qlog(self) -> Union[Queue, SimpleQueue]:
        """Give me access to queue handler."""
        return self._get_data(key=_Keys.LOG_QUEUE, default_value=None)  # type: ignore

    @qlog.setter
    def qlog(self, value: Union[Queue, SimpleQueue]) -> None:
        """Setter for logging queue."""
        self._set_data(
            key=_Keys.LOG_QUEUE,
            value=value,
            set_default_type=Union[Queue, SimpleQueue],
        )

    @property
    def log_processor(self) -> LogProcessor:
        """Give me handler for log processor."""
        return self._get_data(
            key=_Keys.LOG_PROCESSOR, default_value=None
        )  # type: ignore

    @log_processor.setter
    def log_processor(self, value: LogProcessor) -> None:
        """Setter for log processor instance."""
        self._set_data(
            key=_Keys.LOG_PROCESSOR, value=value, set_default_type=LogProcessor
        )


class BLogClient(BData):
    """BLogClass base class.

    Container for logger methods.
    """

    @property
    def logger(self) -> LogClient:
        """Give me logger handler."""
        return self._get_data(key=_Keys.LOGGER, default_value=None)  # type: ignore

    @logger.setter
    def logger(self, arg: LogClient) -> None:
        """Set logger instance."""
        self._set_data(key=_Keys.LOGGER, value=arg, set_default_type=LogClient)


# #[EOF]#######################################################################
