# -*- coding: utf-8 -*-
"""
keys.py
Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 6.09.2024, 16:45:42

Purpose: Keys definition classes for logs subsystem
"""

import syslog

from typing import Dict
from ..attribtool import ReadOnlyClass


class LogKeys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    BUFFERED: str = "__buffered__"
    CONF: str = "__conf__"
    DIR: str = "__dir__"
    FACILITY: str = "__facility__"
    FILE: str = "__file__"
    FORMATTER: str = "__formatter__"
    LEVEL: str = "__level__"
    NAME: str = "__name__"
    NO_CONF: str = "__no_conf__"
    QUEUE: str = "__queue__"
    SYSLOG: str = "__syslog__"


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

    ALERT: str = "ALERT"
    CRITICAL: str = "CRITICAL"
    DEBUG: str = "DEBUG"
    EMERGENCY: str = "EMERGENCY"
    ERROR: str = "ERROR"
    INFO: str = "INFO"
    NOTICE: str = "NOTICE"
    WARNING: str = "WARNING"

    @classmethod
    @property
    def keys(cls) -> tuple:
        """Return tuple of available keys."""
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


# #[EOF]#######################################################################
