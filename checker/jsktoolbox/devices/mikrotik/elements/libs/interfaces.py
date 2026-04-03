# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 04.12.2023

Purpose: interface classes for RouterBoard
"""

from abc import ABC, abstractmethod


class IElement(ABC):
    """Define the contract required for RouterOS element adapters.

    Implementations are expected to expose the same public operations as
    concrete element classes (loading, mutating, and committing data). The
    abstract methods intentionally stay open for future work outlined in the
    repository TODO list.
    """

    # @abstractmethod
    # def load(self) -> bool:
    # """"""


# #[EOF]#######################################################################
