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
    """Raised when a FIFO queue is accessed while empty."""


class Fifo(BClasses):
    """Simple FIFO queue backed by an incrementing index map."""

    __in: int = None  # type: ignore
    __out: int = None  # type: ignore
    __data: Dict = None  # type: ignore

    def __init__(self, data_list: Optional[List[Any]] = None) -> None:
        """Initialise the FIFO queue, optionally preloading the buffer.

        ### Arguments:
        * data_list: Optional[List[Any]] - Optional iterable used to prefill the queue.

        ### Returns:
        None - Constructor.
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
        """Enqueue a new value.

        ### Arguments:
        * data: Any - Payload to store.

        ### Returns:
        None - Method updates internal state in place.
        """
        self.__in += 1
        self.__data[self.__in] = data

    def pop(self) -> Any:
        """Remove and return the oldest queued value.

        ### Returns:
        Any - The dequeued payload.

        ### Raises:
        * EmptyError: Raised when the queue is empty.
        """
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
