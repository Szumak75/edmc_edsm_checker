# -*- coding: UTF-8 -*-
"""
Created on 04 jan 2023.

@author: szumak@virthost.pl
"""


from queue import SimpleQueue, Queue
from threading import Thread
from typing import Union

from checker.jsktoolbox.basetool.data import BData

from checker.system import LogClient, LogProcessor
from checker.keys import CheckerKeys


class BLogProcessor(BData):
    """BLogProcessor base class.

    Container for logger processor methods.
    """

    @property
    def th_log(self) -> Thread:
        """Give me thread logger handler."""
        return self._get_data(
            key=CheckerKeys.TH_LOGGER, default_value=None
        )  # type: ignore

    @th_log.setter
    def th_log(self, value: Thread) -> None:
        self._set_data(key=CheckerKeys.TH_LOGGER, value=value, set_default_type=Thread)

    @property
    def qlog(self) -> Union[Queue, SimpleQueue]:
        """Give me access to queue handler."""
        return self._get_data(
            key=CheckerKeys.LOG_QUEUE, default_value=None
        )  # type: ignore

    @qlog.setter
    def qlog(self, value: Union[Queue, SimpleQueue]) -> None:
        """Setter for logging queue."""
        self._set_data(
            key=CheckerKeys.LOG_QUEUE,
            value=value,
            set_default_type=Union[Queue, SimpleQueue],
        )

    @property
    def log_processor(self) -> LogProcessor:
        """Give me handler for log processor."""
        return self._get_data(
            key=CheckerKeys.LOG_PROCESSOR, default_value=None
        )  # type: ignore

    @log_processor.setter
    def log_processor(self, value: LogProcessor) -> None:
        """Setter for log processor instance."""
        self._set_data(
            key=CheckerKeys.LOG_PROCESSOR, value=value, set_default_type=LogProcessor
        )


class BLogClient(BData):
    """BLogClass base class.

    Container for logger methods.
    """

    @property
    def logger(self) -> LogClient:
        """Give me logger handler."""
        return self._get_data(
            key=CheckerKeys.LOGGER, default_value=None
        )  # type: ignore

    @logger.setter
    def logger(self, arg: LogClient) -> None:
        """Set logger instance."""
        self._set_data(key=CheckerKeys.LOGGER, value=arg, set_default_type=LogClient)
