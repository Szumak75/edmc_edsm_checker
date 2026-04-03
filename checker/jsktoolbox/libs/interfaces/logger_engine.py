# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 2023-11-04

Purpose: Declare the logging engine contract for the toolkit.

Implementations provide transport-specific handling of already formatted log
messages and are leveraged by higher-level logging utilities.
"""

from abc import ABC, abstractmethod


class ILoggerEngine(ABC):
    """Logger engine interface that dispatches log payloads."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Deliver a log message to the underlying transport.

        ### Arguments:
        * message: str - Serialised log record to be emitted.

        ### Returns:
        None - Implementations should not return a value.
        """


# #[EOF]#######################################################################
