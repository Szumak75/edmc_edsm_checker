# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2023-10-10

Purpose: Implement logging engines targeting stdout, stderr, files, and syslog.

Each engine adheres to `ILoggerEngine`, providing consistent `send` semantics
while supporting optional formatters and buffering behaviour.
"""

import os
import sys
import syslog

from inspect import currentframe
from typing import Optional, Union

from .keys import LogKeys, SysLogKeys

from ..attribtool import NoDynamicAttributes
from ..raisetool import Raise
from ..basetool.data import BData
from ..systemtool import PathChecker
from ..basetool.logs import (
    BLoggerEngine,
)
from ..libs.interfaces.logger_engine import ILoggerEngine
from .formatters import BLogFormatter

# https://www.geeksforgeeks.org/python-testing-output-to-stdout/


class LoggerEngineStdout(ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes):
    """STDOUT Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Initialise stdout engine state.

        ### Arguments:
        * name: Optional[str] - Optional logger name injected into formatted messages.
        * formatter: Optional[BLogFormatter] - Formatter applied prior to emit.
        * buffered: bool - When False, flush after each message.

        ### Returns:
        None - Constructor.

        ### Raises:
        * TypeError: Raised when `formatter` does not inherit from `BLogFormatter`.
        """
        if name is not None:
            self.name = name
        self._data[LogKeys.BUFFERED] = buffered
        self._data[LogKeys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[LogKeys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"Expected LogFormatter type, received: '{type(formatter)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Write the message to stdout honoring buffering/formatting rules.

        ### Arguments:
        * message: str - Raw log payload.

        ### Returns:
        None - Output is written to stdout.
        """
        if self._data[LogKeys.FORMATTER]:
            message = self._data[LogKeys.FORMATTER].format(message, self.name)
        sys.stdout.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stdout.write("\n")
        if not self._data[LogKeys.BUFFERED]:
            sys.stdout.flush()


class LoggerEngineStderr(ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes):
    """STDERR Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Initialise stderr engine state.

        ### Arguments:
        * name: Optional[str]
        * formatter: Optional[BLogFormatter]
        * buffered: bool

        ### Returns:
        None

        ### Raises:
        * TypeError: Raised when `formatter` is not a `BLogFormatter` instance.
        """
        if name is not None:
            self.name = name
        self._data[LogKeys.BUFFERED] = buffered
        self._data[LogKeys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[LogKeys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"Expected LogFormatter type, received: '{type(formatter)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Write the message to stderr honoring buffering/formatting rules.

        ### Arguments:
        * message: str - Raw log payload.

        ### Returns:
        None - Output is written to stderr.
        """
        if self._data[LogKeys.FORMATTER]:
            message = self._data[LogKeys.FORMATTER].format(message, self.name)
        sys.stderr.write(f"{message}")
        if not f"{message}".endswith("\n"):
            sys.stderr.write("\n")
        if not self._data[LogKeys.BUFFERED]:
            sys.stderr.flush()


class LoggerEngineFile(ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes):
    """FILE Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Initialise file engine configuration.

        ### Arguments:
        * name: Optional[str]
        * formatter: Optional[BLogFormatter]
        * buffered: bool

        ### Returns:
        None

        ### Raises:
        * TypeError: Raised when `formatter` is not a `BLogFormatter` instance.
        """
        if name is not None:
            self.name = name
        self._data[LogKeys.BUFFERED] = buffered
        self._data[LogKeys.FORMATTER] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[LogKeys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"Expected LogFormatter type, received: '{type(formatter)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    def send(self, message: str) -> None:
        """Append the formatted message to the configured log file.

        ### Arguments:
        * message: str - Raw log payload.

        ### Returns:
        None - The file on disk is updated.

        ### Raises:
        * ValueError: Raised when `logfile` is not configured.
        """
        if self._data[LogKeys.FORMATTER]:
            message = self._data[LogKeys.FORMATTER].format(message, self.name)
            if self.logfile is None:
                raise Raise.error(
                    f"The {self._c_name} is not configured correctly.",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
            log_dir: str = self.logdir if self.logdir else ""
            with open(os.path.join(log_dir, self.logfile), "a") as file:
                if file.writable:
                    file.write(message)
                    file.write("\n")

    @property
    def logdir(self) -> Optional[str]:
        """Return configured log directory.

        ### Returns:
        Optional[str] - Directory path or None when unset.
        """
        if LogKeys.DIR not in self._data:
            self._data[LogKeys.DIR] = None
        return self._data[LogKeys.DIR]

    @logdir.setter
    def logdir(self, dirname: str) -> None:
        """Set or create the log directory as required.

        ### Arguments:
        * dirname: str - Directory path used for log files.

        ### Returns:
        None - Internal state updated.
        """
        if dirname[-1] != os.sep:
            dirname = f"{dirname}/"
        pc_ld = PathChecker(dirname)
        if not pc_ld.exists:
            pc_ld.create()
        if pc_ld.exists and pc_ld.is_dir:
            self._data[LogKeys.DIR] = pc_ld.path

    @property
    def logfile(self) -> Optional[str]:
        """Return configured log file name.

        ### Returns:
        Optional[str] - File name or None when unset.
        """
        if LogKeys.FILE not in self._data:
            self._data[LogKeys.FILE] = None
        return self._data[LogKeys.FILE]

    @logfile.setter
    def logfile(self, filename: str) -> None:
        """Set log file name and ensure the path exists.

        ### Arguments:
        * filename: str - Desired log file name.

        ### Returns:
        None - File path created if necessary.

        ### Raises:
        * FileExistsError: When the path exists and is a directory.
        * PermissionError: When the file cannot be created.
        """
        # TODO: check procedure
        fn = None
        if self.logdir is None:
            fn = filename
        else:
            fn = os.path.join(self.logdir, filename)
        pc_ld = PathChecker(fn)
        if pc_ld.exists:
            if not pc_ld.is_file:
                raise Raise.error(
                    f"The 'filename' passed: '{filename}', is a directory.",
                    FileExistsError,
                    self._c_name,
                    currentframe(),
                )
        else:
            if not pc_ld.create():
                raise Raise.error(
                    f"I cannot create a file: {pc_ld.path}",
                    PermissionError,
                    self._c_name,
                    currentframe(),
                )
        self.logdir = pc_ld.dirname if pc_ld.dirname else ""
        self._data[LogKeys.FILE] = pc_ld.filename


class LoggerEngineSyslog(ILoggerEngine, BLoggerEngine, BData, NoDynamicAttributes):
    """SYSLOG Logger engine."""

    def __init__(
        self,
        name: Optional[str] = None,
        formatter: Optional[BLogFormatter] = None,
        buffered: bool = False,
    ) -> None:
        """Initialise syslog engine configuration.

        ### Arguments:
        * name: Optional[str]
        * formatter: Optional[BLogFormatter]
        * buffered: bool

        ### Returns:
        None

        ### Raises:
        * TypeError: Raised when `formatter` is not a `BLogFormatter` instance.
        """
        if name is not None:
            self.name = name
        self._data[LogKeys.BUFFERED] = buffered
        self._data[LogKeys.FORMATTER] = None
        self._data[LogKeys.LEVEL] = SysLogKeys.level.INFO
        self._data[LogKeys.FACILITY] = SysLogKeys.facility.USER
        self._data[LogKeys.SYSLOG] = None
        if formatter is not None:
            if isinstance(formatter, BLogFormatter):
                self._data[LogKeys.FORMATTER] = formatter
            else:
                raise Raise.error(
                    f"Expected LogFormatter type, received: '{type(formatter)}'.",
                    TypeError,
                    self._c_name,
                    currentframe(),
                )

    def __del__(self) -> None:
        try:
            self._data[LogKeys.SYSLOG].closelog()
        except:
            pass
        self._data[LogKeys.SYSLOG] = None

    @property
    def facility(self) -> int:
        """Return active syslog facility.

        ### Returns:
        int - Syslog facility value.
        """
        return self._data[LogKeys.FACILITY]

    @facility.setter
    def facility(self, value: Union[int, str]) -> None:
        """Configure syslog facility.

        ### Arguments:
        * value: Union[int, str] - Facility constant or symbolic name.

        ### Returns:
        None - Resets the syslog handle to apply the new facility.

        ### Raises:
        * ValueError: When integer facility is not recognised.
        * KeyError: When facility name is unknown.
        """
        if isinstance(value, int):
            if value in tuple(SysLogKeys.facility_keys.values()):
                self._data[LogKeys.FACILITY] = value
            else:
                raise Raise.error(
                    f"Syslog facility: '{value}' not found.",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
        if isinstance(value, str):
            if value in SysLogKeys.facility_keys:
                self._data[LogKeys.FACILITY] = SysLogKeys.facility_keys[value]
            else:
                raise Raise.error(
                    f"Syslog facility name not found: '{value}'",
                    KeyError,
                    self._c_name,
                    currentframe(),
                )
        try:
            self._data[LogKeys.SYSLOG].closelog()
        except:
            pass
        self._data[LogKeys.SYSLOG] = None

    @property
    def level(self) -> int:
        """Return active syslog level.

        ### Returns:
        int - Syslog level value.
        """
        return self._data[LogKeys.LEVEL]

    @level.setter
    def level(self, value: Union[int, str]) -> None:
        """Configure syslog level.

        ### Arguments:
        * value: Union[int, str] - Level constant or symbolic name.

        ### Returns:
        None - Resets the syslog handle to apply the new level.

        ### Raises:
        * ValueError: When integer level is not recognised.
        * KeyError: When level name is unknown.
        """
        if isinstance(value, int):
            if value in tuple(SysLogKeys.level_keys.values()):
                self._data[LogKeys.LEVEL] = value
            else:
                raise Raise.error(
                    f"Syslog level: '{value}' not found.",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
        if isinstance(value, str):
            if value in SysLogKeys.level_keys:
                self._data[LogKeys.LEVEL] = SysLogKeys.level_keys[value]
            else:
                raise Raise.error(
                    f"Syslog level name not found: '{value}'",
                    KeyError,
                    self._c_name,
                    currentframe(),
                )
        try:
            self._data[LogKeys.SYSLOG].closelog()
        except:
            pass
        self._data[LogKeys.SYSLOG] = None

    def send(self, message: str) -> None:
        """Emit the message to syslog.

        ### Arguments:
        * message: str - Raw log payload.

        ### Returns:
        None - Message is forwarded to syslog with configured facility/level.
        """
        if self._data[LogKeys.FORMATTER]:
            message = self._data[LogKeys.FORMATTER].format(message, self.name)
        if self._data[LogKeys.SYSLOG] is None:
            self._data[LogKeys.SYSLOG] = syslog
            self._data[LogKeys.SYSLOG].openlog(facility=self._data[LogKeys.FACILITY])
        self._data[LogKeys.SYSLOG].syslog(
            priority=self._data[LogKeys.LEVEL], message=message
        )


# #[EOF]#######################################################################
