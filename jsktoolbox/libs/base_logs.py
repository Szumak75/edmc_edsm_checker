# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 04.09.2023

  Purpose: base class for log subsystem.
"""

import syslog

from inspect import currentframe
from typing import Optional, Tuple, List, Dict, Any

from jsktoolbox.libs.base_data import BData, BClasses
from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise


class Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    BUFFERED = "__buffered__"
    CONF = "__conf__"
    DIR = "__dir__"
    FACILITY = "__facility__"
    FILE = "__file__"
    FORMATTER = "__formatter__"
    LEVEL = "__level__"
    NAME = "__name__"
    NO_CONF = "__noconf__"
    QUEUE = "__queue__"
    SYSLOG = "__syslog__"


class SysLogKeys(object, metaclass=ReadOnlyClass):
    """SysLog keys definition container class."""

    class __Levels(object, metaclass=ReadOnlyClass):
        ALERT = syslog.LOG_ALERT
        CRITICAL = syslog.LOG_CRIT
        DEBUG = syslog.LOG_DEBUG
        EMERGENCY = syslog.LOG_EMERG
        ERROR = syslog.LOG_ERR
        INFO = syslog.LOG_INFO
        NOTICE = syslog.LOG_NOTICE
        WARNING = syslog.LOG_WARNING

    class __Facilities(object, metaclass=ReadOnlyClass):
        DAEMON = syslog.LOG_DAEMON
        LOCAL0 = syslog.LOG_LOCAL0
        LOCAL1 = syslog.LOG_LOCAL1
        LOCAL2 = syslog.LOG_LOCAL2
        LOCAL3 = syslog.LOG_LOCAL3
        LOCAL4 = syslog.LOG_LOCAL4
        LOCAL5 = syslog.LOG_LOCAL5
        LOCAL6 = syslog.LOG_LOCAL6
        LOCAL7 = syslog.LOG_LOCAL7
        MAIL = syslog.LOG_MAIL
        SYSLOG = syslog.LOG_SYSLOG
        USER = syslog.LOG_USER

    @classmethod
    @property
    def level(cls) -> type[__Levels]:
        """Returns Levels keys property."""
        return cls.__Levels

    @classmethod
    @property
    def facility(cls) -> type[__Facilities]:
        """Returns Facility keys property."""
        return cls.__Facilities

    @classmethod
    @property
    def level_keys(cls) -> Dict:
        """Returns level keys property."""
        return {
            "ALERT": SysLogKeys.level.ALERT,
            "CRITICAL": SysLogKeys.level.CRITICAL,
            "DEBUG": SysLogKeys.level.DEBUG,
            "EMERGENCY": SysLogKeys.level.EMERGENCY,
            "ERROR": SysLogKeys.level.ERROR,
            "INFO": SysLogKeys.level.INFO,
            "NOTICE": SysLogKeys.level.NOTICE,
            "WARNING": SysLogKeys.level.WARNING,
        }

    @classmethod
    @property
    def facility_keys(cls) -> Dict:
        """Returns Facility keys property."""
        return {
            "DAEMON": SysLogKeys.facility.DAEMON,
            "LOCAL0": SysLogKeys.facility.LOCAL0,
            "LOCAL1": SysLogKeys.facility.LOCAL1,
            "LOCAL2": SysLogKeys.facility.LOCAL2,
            "LOCAL3": SysLogKeys.facility.LOCAL3,
            "LOCAL4": SysLogKeys.facility.LOCAL4,
            "LOCAL5": SysLogKeys.facility.LOCAL5,
            "LOCAL6": SysLogKeys.facility.LOCAL6,
            "LOCAL7": SysLogKeys.facility.LOCAL7,
            "MAIL": SysLogKeys.facility.MAIL,
            "SYSLOG": SysLogKeys.facility.SYSLOG,
            "USER": SysLogKeys.facility.USER,
        }


class LogsLevelKeys(object, metaclass=ReadOnlyClass):
    """LogsLevelKeys container class."""

    ALERT = "ALERT"
    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"
    EMERGENCY = "EMERGENCY"
    ERROR = "ERROR"
    INFO = "INFO"
    NOTICE = "NOTICE"
    WARNING = "WARNING"

    @classmethod
    @property
    def keys(cls) -> tuple:
        """Return tuple of avaiable keys."""
        return tuple(
            [
                LogsLevelKeys.ALERT,
                LogsLevelKeys.CRITICAL,
                LogsLevelKeys.DEBUG,
                LogsLevelKeys.EMERGENCY,
                LogsLevelKeys.ERROR,
                LogsLevelKeys.INFO,
                LogsLevelKeys.NOTICE,
                LogsLevelKeys.WARNING,
            ]
        )


class LoggerQueue(BClasses, NoDynamicAttributes):
    """LoggerQueue simple class."""

    __queue: List[List[str]] = []

    def __init__(self) -> None:
        """Constructor."""
        self.__queue = []

    def get(self) -> Optional[tuple[str, ...]]:
        """Get item from queue.

        Returs queue tuple[log_level:str, message:str] or None if empty.
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


class BLoggerQueue(BData, NoDynamicAttributes):
    """Logger Queue base metaclass."""

    @property
    def logs_queue(self) -> Optional[LoggerQueue]:
        """Get LoggerQueue object."""
        if Keys.QUEUE not in self._data:
            return None
        return self._data[Keys.QUEUE]

    @logs_queue.setter
    def logs_queue(self, obj: LoggerQueue) -> None:
        """Set LoggerQueue object."""
        if not isinstance(obj, LoggerQueue):
            raise Raise.error(
                f"Expected LoggerQueue type, received: '{type(obj)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[Keys.QUEUE] = obj


class BLoggerEngine(BData, NoDynamicAttributes):
    """Base class for LoggerEngine classes."""

    @property
    def name(self) -> Optional[str]:
        """Return app name string."""
        if Keys.NAME not in self._data:
            self._data[Keys.NAME] = None
        return self._data[Keys.NAME]

    @name.setter
    def name(self, value: str) -> None:
        """Set app name string."""
        self._data[Keys.NAME] = value


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
