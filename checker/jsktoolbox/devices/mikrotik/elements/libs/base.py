# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 04.12.2023

Purpose: Base classes for elements
"""


from typing import Dict, List, Any

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
    def attrib(self) -> Dict[str, Any]:
        """Returns attributes dict."""
        if self._get_data(key=_Keys.ATTRIB) is None:
            self._set_data(key=_Keys.ATTRIB, set_default_type=Dict, value={})
        return self._get_data(key=_Keys.ATTRIB)  # type: ignore

    @property
    def list(self) -> List[str]:
        """Returns lists od items."""
        if self._get_data(key=_Keys.LIST) is None:
            self._set_data(key=_Keys.LIST, set_default_type=List, value=[])
        return self._get_data(key=_Keys.LIST)  # type: ignore


# #[EOF]#######################################################################
