# -*- coding: utf-8 -*-
"""
  base_data.py
  Author : Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 20.01.2024, 23:29:14
  
  Purpose: 
"""

import tkinter as tk

from inspect import currentframe
from typing import Optional

from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.libs.base_data import BData
from jsktoolbox.raisetool import Raise

from checker_libs.stars import StarsSystem
from checker_libs.th import ThSearchSystem


class _Keys(object, metaclass=ReadOnlyClass):
    """Private Keys class."""

    PLUGINNAME: str = "_pn_"
    VERSION: str = "_ver_"
    SHUTTINGDOWN: str = "_shut_d_"
    JUMPSYSTEM: str = "_js_"
    THSEARCH: str = "__search__"
    STATUS: str = "__status__"


class BCheckerData(BData):
    """docstring for BData."""

    @property
    def jumpsystem(self) -> StarsSystem:
        if _Keys.JUMPSYSTEM not in self._data:
            self._data[_Keys.JUMPSYSTEM] = StarsSystem()
        return self._data[_Keys.JUMPSYSTEM]

    @jumpsystem.setter
    def jumpsystem(self, value: Optional[StarsSystem]) -> None:
        if value is None:
            self._data[_Keys.JUMPSYSTEM] = StarsSystem()
            return
        if not isinstance(value, StarsSystem):
            raise Raise.error(
                "Expected StarsSystem type", TypeError, self._c_name, currentframe()
            )
        self._data[_Keys.JUMPSYSTEM] = value

    @property
    def pluginname(self) -> str:
        if _Keys.PLUGINNAME not in self._data:
            self._data[_Keys.PLUGINNAME] = ""
        return self._data[_Keys.PLUGINNAME]

    @pluginname.setter
    def pluginname(self, value: str) -> None:
        if not isinstance(value, str):
            raise Raise.error(
                "Expected String type", TypeError, self._c_name, currentframe()
            )
        self._data[_Keys.PLUGINNAME] = value

    @property
    def _search(self) -> Optional[ThSearchSystem]:
        if _Keys.THSEARCH not in self._data:
            self._data[_Keys.THSEARCH] = None
        return self._data[_Keys.THSEARCH]

    @_search.setter
    def _search(self, value: ThSearchSystem) -> None:
        if not isinstance(value, ThSearchSystem):
            raise Raise.error(
                "Expected ThSearchSystem type", TypeError, self._c_name, currentframe()
            )
        self._data[_Keys.THSEARCH] = value

    @property
    def shutting_down(self) -> bool:
        if _Keys.SHUTTINGDOWN not in self._data:
            self._data[_Keys.SHUTTINGDOWN] = False
        return self._data[_Keys.SHUTTINGDOWN]

    @shutting_down.setter
    def shutting_down(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise Raise.error(
                "Expected boolean type", TypeError, self._c_name, currentframe()
            )
        self._data[_Keys.SHUTTINGDOWN] = value

    @property
    def status(self) -> tk.StringVar:
        if _Keys.STATUS not in self._data:
            self._data[_Keys.STATUS] = False
        return self._data[_Keys.STATUS]

    @status.setter
    def status(self, value: tk.StringVar) -> None:
        if not isinstance(value, tk.StringVar):
            raise Raise.error(
                "Expected tk.StringVar type", TypeError, self._c_name, currentframe()
            )
        self._data[_Keys.STATUS] = value

    @property
    def version(self) -> str:
        if _Keys.VERSION not in self._data:
            self._data[_Keys.VERSION] = ""
        return self._data[_Keys.VERSION]

    @version.setter
    def version(self, value: str) -> None:
        if not isinstance(value, str):
            raise Raise.error(
                "Expected String type", TypeError, self._c_name, currentframe()
            )
        self._data[_Keys.VERSION] = value


# #[EOF]#######################################################################
