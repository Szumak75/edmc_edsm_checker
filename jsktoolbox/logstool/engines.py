# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 10.10.2023

  Purpose: logger engine classes.
"""

import os
import sys
import syslog

from inspect import currentframe
from typing import Optional, Union

from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.libs.system import PathChecker
from jsktoolbox.libs.base_logs import (
    BLoggerEngine,
    Keys,
    SysLogKeys,
)
from jsktoolbox.libs.interfaces.logger_engine import ILoggerEngine
from jsktoolbox.logstool.formatters import BLogFormatter

# https://www.geeksforgeeks.org/python-testing-output-to-stdout/


class LoggerEngineStdout(ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes):
    """STDOUT Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Constructor."""
        if name is not None:
            self.name = name
        self._data[Keys.BUFFERED] = buffered
        self._data[Keys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[Keys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"Expected LogFormatter type, received: '{type(formatter)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Send message to STDOUT."""
        if self._data[Keys.FORMATTER]:
            message = self._data[Keys.FORMATTER].format(message, self.name)
        sys.stdout.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stdout.write("\n")
        if not self._data[Keys.BUFFERED]:
            sys.stdout.flush()


class LoggerEngineStderr(ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes):
    """STDERR Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Constructor."""
        if name is not None:
            self.name = name
        self._data[Keys.BUFFERED] = buffered
        self._data[Keys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[Keys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"Expected LogFormatter type, received: '{type(formatter)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Send message to STDERR."""
        if self._data[Keys.FORMATTER]:
            message = self._data[Keys.FORMATTER].format(message, self.name)
        sys.stderr.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stderr.write("\n")
        if not self._data[Keys.BUFFERED]:
            sys.stderr.flush()


class LoggerEngineFile(ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes):
    """FILE Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Constructor."""
        if name is not None:
            self.name = name
        self._data[Keys.BUFFERED] = buffered
        self._data[Keys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[Keys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"Expected LogFormatter type, received: '{type(formatter)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Send message to file."""
        if self._data[Keys.FORMATTER]:
            message = self._data[Keys.FORMATTER].format(message, self.name)
            if self.logfile is None:
                raise Raise.error(
                    f"The {self._c_name} is not configured correctly.",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
            logdir: str = self.logdir if self.logdir else ""
            with open(os.path.join(logdir, self.logfile), "a") as file:
                if file.writable:
                    file.write(message)
                    file.write("\n")

    @property
    def logdir(self) -> Optional[str]:
        """Return log directory."""
        if Keys.DIR not in self._data:
            self._data[Keys.DIR] = None
        return self._data[Keys.DIR]

    @logdir.setter
    def logdir(self, dirname: str) -> None:
        """Set log directory."""
        if dirname[-1] != os.sep:
            dirname = f"{dirname}/"
        ld = PathChecker(dirname)
        if not ld.exists:
            ld.create()
        if ld.exists and ld.is_dir:
            self._data[Keys.DIR] = ld.path

    @property
    def logfile(self) -> Optional[str]:
        """Return log file name."""
        if Keys.FILE not in self._data:
            self._data[Keys.FILE] = None
        return self._data[Keys.FILE]

    @logfile.setter
    def logfile(self, filename: str) -> None:
        """Set log file name."""
        # TODO: check procedure
        fn = None
        if self.logdir is None:
            fn = filename
        else:
            fn = os.path.join(self.logdir, filename)
        ld = PathChecker(fn)
        if ld.exists:
            if not ld.is_file:
                raise Raise.error(
                    f"The 'filename' passed: '{filename}', is a directory.",
                    FileExistsError,
                    self._c_name,
                    currentframe(),
                )
        else:
            if not ld.create():
                raise Raise.error(
                    f"I cannot create a file: {ld.path}",
                    PermissionError,
                    self._c_name,
                    currentframe(),
                )
        self.logdir = ld.dirname if ld.dirname else ""
        self._data[Keys.FILE] = ld.filename


class LoggerEngineSyslog(ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes):
    """SYSLOG Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Constructor."""
        if name is not None:
            self.name = name
        self._data[Keys.BUFFERED] = buffered
        self._data[Keys.FORMATTER] = None
        self._data[Keys.LEVEL] = SysLogKeys.level.INFO
        self._data[Keys.FACILITY] = SysLogKeys.facility.USER
        self._data[Keys.SYSLOG] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[Keys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"Expected LogFormatter type, received: '{type(formatter)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    def __del__(self) -> None:
        try:
            self._data[Keys.SYSLOG].closelog()
        except:
            pass
        self._data[Keys.SYSLOG] = None

    @property
    def facility(self) -> int:
        """Return syslog facility."""
        return self._data[Keys.FACILITY]

    @facility.setter
    def facility(self, value: Union[int, str]) -> None:
        """Set syslog facility."""
        if isinstance(value, int):
            if value in tuple(SysLogKeys.facility_keys.values()):
                self._data[Keys.FACILITY] = value
            else:
                raise Raise.error(
                    f"Syslog facility: '{value}' not found.",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
        if isinstance(value, str):
            if value in SysLogKeys.facility_keys:
                self._data[Keys.FACILITY] = SysLogKeys.facility_keys[value]
            else:
                raise Raise.error(
                    f"Syslog facility name not found: '{value}'",
                    KeyError,
                    self._c_name,
                    currentframe(),
                )
        try:
            self._data[Keys.SYSLOG].closelog()
        except:
            pass
        self._data[Keys.SYSLOG] = None

    @property
    def level(self) -> int:
        """Return syslog level."""
        return self._data[Keys.LEVEL]

    @level.setter
    def level(self, value: Union[int, str]) -> None:
        """Set syslog level."""
        if isinstance(value, int):
            if value in tuple(SysLogKeys.level_keys.values()):
                self._data[Keys.LEVEL] = value
            else:
                raise Raise.error(
                    f"Syslog level: '{value}' not found.",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
        if isinstance(value, str):
            if value in SysLogKeys.level_keys:
                self._data[Keys.LEVEL] = SysLogKeys.level_keys[value]
            else:
                raise Raise.error(
                    f"Syslog level name not found: '{value}'",
                    KeyError,
                    self._c_name,
                    currentframe(),
                )
        try:
            self._data[Keys.SYSLOG].closelog()
        except:
            pass
        self._data[Keys.SYSLOG] = None

    def send(self, message: str) -> None:
        """Send message to SYSLOG."""
        if self._data[Keys.FORMATTER]:
            message = self._data[Keys.FORMATTER].format(message, self.name)
        if self._data[Keys.SYSLOG] is None:
            self._data[Keys.SYSLOG] = syslog
            self._data[Keys.SYSLOG].openlog(facility=self._data[Keys.FACILITY])
        self._data[Keys.SYSLOG].syslog(priority=self._data[Keys.LEVEL], message=message)


# #[EOF]#######################################################################
