# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 23.06.2023

Purpose: Octet class for representing ipv4 octet.
"""

from inspect import currentframe
from typing import Union, TypeVar

from ...attribtool import NoDynamicAttributes
from ...raisetool import Raise
from ...libs.interfaces.comparators import IComparators
from ...basetool.classes import BClasses

TOctet = TypeVar("TOctet", bound="Octet")


class Octet(IComparators, BClasses, NoDynamicAttributes):
    """Class for representing ipv4 octet.

    Constructor arguments:
    value [str|int|Octet] -- Value of octet in proper range from 0 to 255

    Public property:
    value [int] -- Return integer representation of octet.

    Public setters:
    value [str|int|Octet] -- Set value of octet.
    """

    __value: int = 0

    def __init__(self, value: Union[str, int, TOctet]) -> None:
        """Constructor."""
        self.value = value

    def __eq__(self, arg: TOctet) -> bool:
        """Equal."""
        return int(self) == int(arg)

    def __ge__(self, arg: TOctet) -> bool:
        """Greater then or equal."""
        return int(self) >= int(arg)

    def __gt__(self, arg: TOctet) -> bool:
        """Greater then."""
        return int(self) > int(arg)

    def __le__(self, arg: TOctet) -> bool:
        """Less then or equal."""
        return int(self) <= int(arg)

    def __lt__(self, arg: TOctet) -> bool:
        """Less then."""
        return int(self) < int(arg)

    def __ne__(self, arg: TOctet) -> bool:
        """Negative."""
        return int(self) != int(arg)

    def __int__(self) -> int:
        """Return integer representation of octet."""
        return self.value

    def __str__(self) -> str:
        """Return string representation of octet."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return representation of object."""
        return f"{self._c_name}({self.value})"

    @staticmethod
    def __check_range(value: int) -> bool:
        if value not in range(0, 256):
            return False
        return True

    @staticmethod
    def __is_integer(value: str) -> bool:
        try:
            int(value)
            return True
        except:
            return False

    @property
    def value(self) -> int:
        """Return value of Octet as int."""
        return self.__value

    @value.setter
    def value(
        self,
        args: Union[str, int, TOctet],
    ) -> None:
        if isinstance(args, int):
            if Octet.__check_range(args):
                self.__value = args
                return
            else:
                raise Raise.error(
                    f"Received value '{args}' out of range(0-255).",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
        elif isinstance(args, str):
            if Octet.__is_integer(args):
                var = int(args)
                if Octet.__check_range(var):
                    self.__value = var
                    return
                else:
                    raise Raise.error(
                        f"Received value '{args}' out of range(0-255).",
                        ValueError,
                        self._c_name,
                        currentframe(),
                    )
        elif isinstance(args, Octet):
            tmp: TOctet = args
            self.__value = tmp.value
            return
        raise Raise.error(
            f"Expected Integer or String type, received: '{type(args)}'.",
            TypeError,
            self._c_name,
            currentframe(),
        )


# #[EOF]#######################################################################
