# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 2023-06-24

Purpose: Define abstract comparator interfaces used across numeric and
address-related helpers.
"""

from abc import ABC, abstractmethod


class ILt(ABC):
    """Less than.

    x < y
    """

    @abstractmethod
    def __lt__(self, value: object) -> bool:
        pass


class ILe(ABC):
    """Less than or equal.

    x <= y
    """

    @abstractmethod
    def __le__(self, value: object) -> bool:
        pass


class IEq(ABC):
    """Equal.

    x == y
    """

    @abstractmethod
    def __eq__(self, value: object) -> bool:
        pass


class INe(ABC):
    """Negative.

    x != y
    """

    @abstractmethod
    def __ne__(self, value: object) -> bool:
        pass


class IGt(ABC):
    """Greater than.

    x > y
    """

    @abstractmethod
    def __gt__(self, value: object) -> bool:
        pass


class IGe(ABC):
    """Greater than or equal to.

    x >= y
    """

    @abstractmethod
    def __ge__(self, value: object) -> bool:
        pass


class IComparators(IEq, IGe, IGt, ILe, ILt, INe):
    """Aggregate interface grouping all comparison operators."""

    pass


# #[EOF]#######################################################################
