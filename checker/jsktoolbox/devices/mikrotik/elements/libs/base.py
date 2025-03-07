# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 04.12.2023

Purpose: Base classes for elements
"""


from typing import Dict, List

from .....basetool.data import BData
from .....attribtool import ReadOnlyClass


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ATTRIB: str = "__attrib__"
    LIST: str = "__list__"


class BElement(BData):
    """Base class for Element."""

    @property
    def attrib(self) -> Dict:
        """Returns attributes dict."""
        if _Keys.ATTRIB not in self._data:
            self._data[_Keys.ATTRIB] = {}
        return self._data[_Keys.ATTRIB]

    @property
    def list(self) -> List:
        """Returns lists od items."""
        if _Keys.LIST not in self._data:
            self._data[_Keys.LIST] = []
        return self._data[_Keys.LIST]


# #[EOF]#######################################################################
