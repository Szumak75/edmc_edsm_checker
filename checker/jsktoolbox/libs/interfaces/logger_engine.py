# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 04.11.2023

Purpose: Logger Engine interface class.
"""

from abc import ABC, abstractmethod


class ILoggerEngine(ABC):
    """Logger engine interface class."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Send message method."""


# #[EOF]#######################################################################
