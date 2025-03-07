# -*- coding: UTF-8 -*-
"""
Author:  Jacek Kotlarski --<szumak@virthost.pl>
Created: 14.09.2023

Purpose: Word16 class for representing IPv6 word.
"""

from inspect import currentframe
from typing import Union, TypeVar

from ...attribtool import NoDynamicAttributes
from ...raisetool import Raise
from ...libs.interfaces.comparators import IComparators
from ...basetool.classes import BClasses

TWord16 = TypeVar("TWord16", bound="Word16")


class Word16(IComparators, BClasses, NoDynamicAttributes):
    """Class for representing ipv6 16-bits word.

    Constructor arguments:
    value [str|int|Word16] -- Value of word in proper range from 0x0000 to 0xffff

    Public property:
    value [int] -- Return integer representation of word.

    Public setters:
    value [str|int|Word16] -- Set value of word."""

    __value: int = 0

    def __init__(self, value: Union[str, int, TWord16]) -> None:
        """Constructor."""
        self.value = value

    def __eq__(self, arg: TWord16) -> bool:
        """Equal."""
        return self.value == arg.value

    def __ge__(self, arg: TWord16) -> bool:
        """Greater then or equal."""
        return self.value >= arg.value

    def __gt__(self, arg: TWord16) -> bool:
        """Greater then."""
        return self.value > arg.value

    def __le__(self, arg: TWord16) -> bool:
        """Less then or equal."""
        return self.value <= arg.value

    def __lt__(self, arg: TWord16) -> bool:
        """Less then."""
        return self.value < arg.value

    def __ne__(self, arg: TWord16) -> bool:
        """Negative."""
        return self.value != arg.value

    def __int__(self) -> int:
        """Return integer representation of word."""
        return self.value

    def __str__(self) -> str:
        """Return a hexadecimal string representing a word without the leading '0x'."""
        return hex(self.value)[2:]

    def __repr__(self) -> str:
        """Return representation of object."""
        return f"{self._c_name}({self.value})"

    @staticmethod
    def __check_range(value: int) -> bool:
        if value not in range(0, 65536):
            return False
        return True

    @staticmethod
    def __is_integer(value: str) -> bool:
        try:
            if value.find("0x") == 0:
                int(value, 16)
            else:
                int(value)
            return True
        except:
            return False

    @property
    def value(self) -> int:
        """Return value of Word16 as int."""
        return self.__value

    @value.setter
    def value(
        self,
        args: Union[str, int, TWord16],
    ) -> None:
        if isinstance(args, int):
            if Word16.__check_range(args):
                self.__value = args
                return
            else:
                raise Raise.error(
                    f"Received value '{args}' out of range(0-65535).",
                    ValueError,
                    self._c_name,
                    currentframe(),
                )
        elif isinstance(args, str):
            if Word16.__is_integer(args):
                if args.find("0x") == 0:
                    var = int(args, 16)
                else:
                    var = int(args)
                if Word16.__check_range(var):
                    self.__value = var
                    return
                else:
                    raise Raise.error(
                        f"Received value '{args}' out of range(0-65535).",
                        ValueError,
                        self._c_name,
                        currentframe(),
                    )
        elif isinstance(args, Word16):
            tmp: TWord16 = args
            self.__value = tmp.value
            return
        raise Raise.error(
            f"Expected Integer or String type, received: '{type(args)}'.",
            TypeError,
            self._c_name,
            currentframe(),
        )


# #[EOF]#######################################################################
