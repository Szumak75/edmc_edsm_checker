# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 03.12.2023

Purpose: Sets of container classes with FIFO queue functionality.
"""
from inspect import currentframe
from typing import List, Dict, Any, Optional

from ..basetool.classes import BClasses
from ..raisetool import Raise


class EmptyError(Exception):
    """Empty exception class."""


class Fifo(BClasses):
    """Fifo class."""

    __in: int = None  # type: ignore
    __out: int = None  # type: ignore
    __data: Dict = None  # type: ignore

    def __init__(self, data_list: Optional[List[Any]] = None) -> None:
        """Constructor.

        ### Arguments
        * data_list [Optional[List[Any]]] - optional list of initial dataset.
        """
        self.__in = 0
        self.__out = 0
        self.__data = dict()

        # optional dataset init
        if data_list:
            for item in data_list:
                self.put(item)

    def __repr__(self) -> str:
        return f"{self._c_name}({list(self.__data.values())})"

    def put(self, data: Any) -> None:
        """Put data to queue."""
        self.__in += 1
        self.__data[self.__in] = data

    def pop(self) -> Any:
        """Pop first item from queue."""
        self.__out += 1
        try:
            out: Any = self.__data.pop(self.__out)
        except KeyError:
            raise Raise.error(
                f"{self._c_name} is empty.",
                EmptyError,
                self._c_name,
                currentframe(),
            )
        return out


# #[EOF]#######################################################################
