# -*- coding: UTF-8 -*-
"""
Created on 04 jan 2023.

@author: szumak@virthost.pl
"""


from queue import SimpleQueue, Queue
from threading import Thread
from typing import Union
from jsktoolbox.attribtool import NoDynamicAttributes

from checker_libs.system import LogClient, LogProcessor


class BLogProcessor(NoDynamicAttributes):
    """MLogProcessor metaclass.

    Container for logger processor methods.
    """

    __logger_queue: Union[Queue, SimpleQueue] = None  # type: ignore
    __log_processor_engine: LogProcessor = None  # type: ignore
    __thread_logger: Thread = None  # type: ignore

    @property
    def th_log(self) -> Thread:
        """Give me thread logger handler."""
        return self.__thread_logger

    @th_log.setter
    def th_log(self, value: Thread) -> None:
        self.__thread_logger = value

    @property
    def qlog(self) -> Union[Queue, SimpleQueue]:
        """Give me access to queue handler."""
        return self.__logger_queue

    @qlog.setter
    def qlog(self, value: Union[Queue, SimpleQueue]) -> None:
        """Setter for logging queue."""
        self.__logger_queue = value

    @property
    def log_processor(self) -> LogProcessor:
        """Give me handler for log processor."""
        return self.__log_processor_engine

    @log_processor.setter
    def log_processor(self, value: LogProcessor) -> None:
        """Setter for log processor instance."""
        self.__log_processor_engine = value


class BLogClient:
    """MLogClass metaclass.

    Container for logger methods.
    """

    __logger: LogClient = None  # type: ignore

    @property
    def logger(self) -> LogClient:
        """Give me logger handler."""
        return self.__logger

    @logger.setter
    def logger(self, arg: LogClient) -> None:
        """Set logger instance."""
        self.__logger = arg
